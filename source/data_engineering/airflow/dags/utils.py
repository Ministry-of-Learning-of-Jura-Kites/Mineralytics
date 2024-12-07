import os
from typing import Iterable, List, Tuple
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from bs4 import Tag
import re
from kafka import KafkaProducer

stored = set()

ARTICLE_URL = "https://www.nature.com/nature/articles?type=article&year=2024"


def get_article_link(tag: Tag):
    id = re.match("^/articles/(.*)$", tag.attrs["href"]).group(1)
    return id


def scrape(page: int) -> Tuple[Iterable[str], bool]:
    url = ARTICLE_URL + "&page=" + str(page)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page, "html.parser")
    article_titles = soup.select("a.c-card__link.u-link-inherit")
    article_links = map(get_article_link, article_titles)
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
    if os.path.isfile(relative_to_abs(["data", "scraped", file_name])):
        return True


def is_stored(file_name):
    if file_name in stored:
        return True
    found = _is_stored(file_name)
    if found:
        stored.add(file_name)
    return stored


def scrape_all(send_kafka: bool):
    if send_kafka:
        producer = KafkaProducer(bootstrap_servers="broker:9092")

    page = 1
    has_next = True
    while has_next:
        ids, has_next = scrape(page)
        for id in ids:
            if is_stored(id):
                has_next = False
                break
            if send_kafka:
                producer.send("article", str.encode(id))
            else:
                print(id)


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers="localhost:9094",
        api_version=(3, 10, 0),
    )
    print("connected")
    # producer.send("article", str.encode(next(scrape(1)[0])))
    producer.send("article", b"ggggg")
    print("finished")
    producer.flush()
