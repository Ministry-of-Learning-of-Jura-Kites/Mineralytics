from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime

def scrape_paper(url):
  is_successful = False
  while not is_successful:
    # from academic.oup.com
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html_page = urlopen(req).read()
    soup = BeautifulSoup(html_page,'html.parser')

    if "Loading..." in soup.select_one("body").decode_contents():
      continue
    
    is_successful=True
    
    title = next(soup.select_one("h1.wi-article-title.article-title-main.accessible-content-title.at-articleTitle").children).removeprefix("\r\n").removesuffix("\r\n").strip()
    # print(title)

    authors_node = map(lambda node: next(node.children),soup.select(".al-authors-list span button"))
    # print(list(authors_node))

    # print(soup.select_one("span.al-author-name-more:nth-child(1) > span:nth-child(3)"))

    published_date = soup.select_one(".citation-date").decode_contents()
    published_date = datetime.strptime(published_date, '%d %B, %Y').date()

scrape_paper(
    "https://academic.oup.com/ehjcimaging/advance-article-abstract/doi/10.1093/ehjci/jeae298/7903254"
)
