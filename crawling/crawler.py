import thread
import time

from data_structures.arrays import Queue, ThreadSafeQueue
from scrapping.scrapper import Soup
from Queue import Queue as SysQueue


class Crawler:

    def __init__(self, seed):
        self.seed = seed
        self.queue = Queue()
        self.queue.enqueue(seed)
        self.visited = set()
        self.content = []

    def crawl_bfs(self, limit=0):
        counter = 0
        start = time.time()
        while not self.queue.is_empty():
            # print 'counter ', counter
            if limit and counter > limit:
                break
            counter += 1
            url = self.queue.dequeue()
            soup = Soup(url)
            # print 'queue size: ', self.queue.size()
            self.visited.add(url)
            print str(len(self.visited)) + 'in' + str(time.time()-start)
            if soup is not None:
                text = soup.get_all_p_text()
                self.content.append({'content': text, 'url': url})
                for link in soup.get_absolute_internal_links():
                    if (link not in self.visited) and (not self.is_media_file(link)):
                        self.queue.enqueue(link)
        return self.content

    @staticmethod
    def is_media_file(url):
        media_identifier_tokens = ['.jpg', '.png', 'jpeg', '.js', '.css', '.gif']
        for token in media_identifier_tokens:
            if token in url.lower():
                return True
        return False


class CrawlerManager:

    def __init__(self, seed, workers=4, seeds=[]):
        self.seed = seed
        self.visited = set()
        self.queue = Queue()
        self.outlinks_queue = SysQueue()  # to be consumed by manger and produced by spider
        self.links_queue = SysQueue()  # opposite to outlinks_queue
        if seeds:
            for seed in seeds:
                self.links_queue.put(seed)
                self.visited.add(seed)
        else:
            self.queue.enqueue(seed)
        self.content = []
        self.max_workers = 100

    def crawl_bfs(self, limit=0):

        counter = 0
        for i in range(self.max_workers):
            thread.start_new_thread(spider, (i, self.links_queue, self.outlinks_queue, self.visited))
        time.sleep(5)
        start = time.time()
        while True:

            outlinks = self.outlinks_queue.get()
            for link in outlinks:
                if link not in self.visited:
                    self.queue.enqueue(link)
            for item in self.queue.queue:
                self.links_queue.put(item)
            print str(len(self.visited))+ ' in '+ str(time.time()-start)+'   xxxxxxxxxxxxxxxxxxxx '
        return self.content

    @staticmethod
    def is_media_file(url):
        media_identifier_tokens = ['.jpg', '.png', 'jpeg', '.js', '.css', '.gif']
        for token in media_identifier_tokens:
            if url.lower().endswith(token):
                return True
        return False


def spider(id, links_queue, outlinks_queue, visited):
    while True:
        url = links_queue.get()
        soup = Soup(url)
        visited.add(url)
        # print str(id) + " is downloading " + str(url)
        # print 'queue size: ', self.queue.size()
        if soup is not None:
            text = soup.get_all_p_text()
            absolute_internal_links = soup.get_absolute_internal_links()
            external_links = soup.get_external_links()
            outlinks_queue.put(list(absolute_internal_links) + list(external_links))

