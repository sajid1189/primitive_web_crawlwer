import re

import requests
from bs4 import BeautifulSoup


class WebPage:
    def __init__(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            self.soup = None
        self.all_external_links = []
        self.all_internal_links = []
        self.all_links = []

    def get_pretty_soup(self):
        if self.soup:
            return self.soup.prettify()
        else:
            return 'Sorry! The soup was nasty.'

    def get_all_p(self):
        if self.soup:
            return self.soup.find_all('p')

    def get_all_p_text(self):
        p_contents = []
        if self.soup:
            for p in self.get_all_p():
                p_contents.append(p.get_text())
        return p_contents

    def get_external_links(self):
        if not self.all_external_links:
            for link in self.get_all_links():
                if 'http' in link.get('href'):
                    self.all_external_links.append(link.get('href'))
        return self.all_external_links

    def get_internal_links(self):
        return

    def get_all_links(self):
        if self.soup:
            if not self.all_links:
                self.all_links = self.soup.find_all('a', href=True)
        return self.all_links
