import unicodedata
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime

def get_first_child(node):
  return unicodedata.normalize("NFKD", node.text)

def scrape_paper(url):
  req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
  html_page = urlopen(req).read()
  soup = BeautifulSoup(html_page,'html.parser')

  title = next(soup.select_one(".c-article-title").children)
  # print(title)

  authors_node = map(get_first_child,soup.select("li.c-article-author-list__item a[data-test='author-name']"))
  # print(list(authors_node))
  
  published_date = soup.select_one("li.c-article-identifiers__item:nth-child(2) time").decode_contents()
  published_date = datetime.strptime(published_date, '%d %B %Y').date()
  # print(published_date)

  references = map(get_first_child,soup.select("p.c-article-references__text"))
  # print(list(references))

  organizations = map(get_first_child,soup.select("ol.c-article-author-affiliation__list li p:nth-child(1)"))
  organizations = map(lambda organizations: organizations.split(", ")[:3],organizations)
  organizations_authors = map(get_first_child,soup.select("ol.c-article-author-affiliation__list li p:nth-child(2)"))
  print(list(zip(organizations,organizations_authors)))
  
scrape_paper(
    "https://www.nature.com/articles/nphys2615"
)
