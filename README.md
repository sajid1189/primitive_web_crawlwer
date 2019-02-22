# primitive_web_crawlwer

How to use:
instanitalte the Crawler instance with the initial url (seed) as an argument. Then call the bfs metho of the instance e.g.,

from crawling.crawler import Crawler <br>
cr = Crawler('https://google.de/') <br> 
c = cr.bfs()
