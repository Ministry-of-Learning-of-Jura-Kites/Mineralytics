import bs4 as BeatifulSoup
from urllib.request import Request, urlopen

def scrape_paper(url):
  # from academic.oup.com
  req = Request(url)
  html_page = urlopen(req).read()
  soup = BeatifulSoup(html_page,'html.parser')
  
  title = soup.find("html.no-js.firefox body.off-canvas.pg_Article.pg_article div.master-container.js-master-container div#main.content-main.js-main.ui-base section.master-main.row div.center-inner-row.no-overflow div.page-column-wrap div#ContentColumn.page-column.page-column--center div.content-inner-wrap div.widget.widget-ArticleTopInfo.widget-instance-OUP_Abstract_ArticleTop_Info_Widget div.module-widget.article-top-widget div.widget-items div.title-wrap h1.wi-article-title.article-title-main.accessible-content-title.at-articleTitle").decode_contents()
  print(title)
  pass

scrape_paper("https://academic.oup.com/biomet/article-abstract/45/1-2/229/264691?login=false")