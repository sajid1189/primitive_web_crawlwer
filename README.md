# primitive_web_crawlwer

How to use:
instanitalte the Crawler instance with the staring web page as an argument. Then call the bfs metho of the instance e.g.,

from crawling.crawler import Crawler \n
cr = Crawler('https://google.de/') \n
c = cr.bfs()
