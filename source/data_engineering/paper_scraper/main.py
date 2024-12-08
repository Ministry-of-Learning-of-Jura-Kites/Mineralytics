from time import sleep
import json
import logging
import traceback
import unicodedata
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import groupby
from kafka import KafkaConsumer
import aiohttp
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio


def get_first_child(node):
    return unicodedata.normalize("NFKD", node.text)


async def scrape_paper(session, article_id):
    url = "https://www.nature.com/articles/{}".format(article_id)
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.content.read(), "lxml")

        title = next(soup.select_one(".c-article-title").children)
        # print(title)

        authors_node = map(
            get_first_child,
            soup.select("li.c-article-author-list__item a[data-test='author-name']"),
        )
        # print(list(authors_node))

        published_date = soup.select_one(
            "li.c-article-identifiers__item time"
        ).decode_contents()
        published_date = datetime.strptime(published_date, "%d %B %Y").date()
        # print(published_date)

        references = map(get_first_child, soup.select("p.c-article-references__text"))
        # print(list(references))

        organizations = map(
            get_first_child,
            soup.select("ol.c-article-author-affiliation__list li p:nth-child(1)"),
        )

        organizations = list(
            map(
                lambda organizations: organizations.split(", ")[:3],
                organizations,
            )
        )
        organizations_authors = list(
            map(
                get_first_child,
                soup.select("ol.c-article-author-affiliation__list li p:nth-child(2)"),
            )
        )
        # print(list(zip(organizations, organizations_authors)))

        # journal_title = map(
        #     get_first_child,
        #     soup.select("i[data-test='journal-title']"),
        # )
        # print(list(journal_title))

        subjects = map(
            get_first_child, soup.select("li.c-article-subject-list__subject")
        )
        # print(list(subjects))

        def to_author_group(organization_and_authors):
            organization = organization_and_authors[0]
            authors = map(lambda x: x[1], organization_and_authors[1])
            # print(organization, authors)
            return {
                "affiliation": {
                    "organization": list(map(lambda x: {"$": x}, organization))
                },
                "author": list(
                    map(lambda x: {"preferred-name": {"ce:indexed-name": x}}, authors)
                ),
            }

        author_groups = list(
            map(
                to_author_group,
                groupby(zip(organizations, organizations_authors), lambda x: x[0]),
            )
        )

        result = {}
        result["abstracts-retrieval-response"] = {
            "item": {
                "ait:date-sort": {
                    "@day": str(published_date.day),
                    "@year": str(published_date.year),
                    "@month": str(published_date.month),
                }
            },
            "bibrecord": {"head": {"author-group": author_groups}},
            "coredata": {"dc:title": title},
            "authors": {
                "author": list(map(lambda x: {"ce:indexed-name": x}, authors_node))
            },
            "subject-areas": {
                "subject-area": list(map(lambda subject: {"$": subject}, subjects))
            },
        }

        return result


async def scrape_and_save_paper(session, article_id: str):
    with open("/data/scraped/{}.json".format(article_id), "w") as f:
        f.write(json.dumps(await scrape_paper(session, article_id)))


async def main():
    host = "broker:9092"
    # host = "localhost:9094"
    consumer = AIOKafkaConsumer("article", bootstrap_servers=host)
    await consumer.start()
    print("connected")
    async with aiohttp.ClientSession() as session:
        async for message in consumer:
            article_id = message.value.decode("utf-8")
            print("receive", article_id)
            asyncio.create_task(scrape_and_save_paper(session, article_id))


asyncio.run(main())