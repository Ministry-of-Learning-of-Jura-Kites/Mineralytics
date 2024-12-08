import asyncio
import os
from typing import Iterable, List, Tuple
from urllib.request import Request, urlopen
import aiohttp
from bs4 import BeautifulSoup, PageElement
from bs4 import Tag
import re
from kafka import KafkaProducer

stored = set()

ARTICLE_URLS = [
    "https://www.nature.com/nature/articles?type=article&year=2024",
    "https://www.nature.com/nphys/research-articles?type=article&year=2024",
]


def get_article_link(tag: Tag):
    id = re.match("^/articles/(.*)$", tag.attrs["href"]).group(1)
    return id


async def scrape(ARTICLE_URL, session, page: int) -> Tuple[Iterable[str], bool]:
    url = ARTICLE_URL + "&page=" + str(page)
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.content.read(), "lxml")
        article_titles = soup.select("a.c-card__link.u-link-inherit")
        article_links = map(get_article_link, article_titles)

        # page_button = soup.select("li.c-pagination__item")
        # print(page_button[-2])
        # number_of_pages: PageElement = page_button[-2].contents[-1]

        disabled_link = soup.select(
            "span.c-pagination__link.c-pagination__link--disabled > span"
        )
        if len(disabled_link) == 0:
            has_next = True
        else:
            next_link = disabled_link.pop()
            has_next = not "Next" in next(next_link.children)
        return (article_links, has_next)


def relative_to_abs(relative_path: List[any]) -> str:
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(
        os.path.join(dirname, "..", "..", "..", "..", *map(str, relative_path))
    )


def _is_stored(file_name):
    return os.path.isfile("/data/scraped/{}.json".format(file_name))


def is_stored(file_name):
    if file_name in stored:
        return True
    found = _is_stored(file_name)
    if found:
        stored.add(file_name)
    return found


async def scrape_all_of_url(
    ARTICLE_URL, session, send_kafka: bool, stop_if_exists: bool
):
    host = "broker:9092"
    # host = "localhost:9094"
    if send_kafka:
        producer = KafkaProducer(bootstrap_servers=host)

    page = 1
    has_next = True
    while has_next:
        print("url: {}, page: {}".format(ARTICLE_URL, page))
        ids, has_next = await scrape(ARTICLE_URL, session, page)
        if not has_next:
            print("last page")
        for id in ids:
            if stop_if_exists and is_stored(id):
                print(id, "already exist")
                has_next = False
                break
            if send_kafka:
                producer.send("article", str.encode(id))
            else:
                print(id)
        page += 1


async def scrape_all_async(send_kafka: bool, stop_if_exists: bool):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *map(
                lambda url: scrape_all_of_url(url, session, send_kafka, stop_if_exists),
                ARTICLE_URLS,
            )
        )


def scrape_all(send_kafka: bool, **kwargs):
    print(kwargs.get("params"))
    asyncio.run(
        scrape_all_async(
            send_kafka, kwargs.get("params")["stop_if_exists"]
        )
    )


# asyncio.run(scrape_all(False))
