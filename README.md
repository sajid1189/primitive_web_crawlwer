# primitive_web_crawlwer

How to use:
instanitalte the Crawler instance with the staring web page as an argument. Then call the bfs metho of the instance e.g.,

from crawling.crawler import Crawler
cr = Crawler('https://google.de/')
c = cr.bfs()
