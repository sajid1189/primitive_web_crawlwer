from data_structures.arrays import Queue, ThreadSafeQueue
from scrapping.scrapper import Soup


class Crawler:

    def __init__(self, seed):
        self.seed = seed
        self.queue = Queue()
        self.queue.enqueue(seed)
        self.visited = set()
        self.content = []

    def crawl_bfs(self, limit=0):
        counter = 0
        while not self.queue.is_empty():
            # print 'counter ', counter
            if limit and counter > limit:
                break
            counter += 1
            url = self.queue.dequeue()
            soup = Soup(url)
            # print 'queue size: ', self.queue.size()
            self.visited.add(url)
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


class MultiCrawler:

    def __init__(self, seed, workers=4):
        self.seed = seed
        self.queue = ThreadSafeQueue()
        self.queue.put(seed)
        self.visited = set()
        self.content = []
        self.workers = workers

    def crawl_bfs(self, limit=0):
        counter = 0
        while not self.queue.empty():
            # print 'counter ', counter
            if limit and counter > limit:
                break
            counter += 1
            url = self.queue.get()
            self.queue.task_done()
            soup = Soup(url)
            # print 'queue size: ', self.queue.size()
            self.visited.add(url)
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
