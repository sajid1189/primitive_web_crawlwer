# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup


class Soup:
    def __init__(self, url):
        self.url = url
        # print 'scrapping: ', url

        try:
            response = requests.get(url)
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print 'exception thrown at :{}'.format(url)
            self.soup = None
        self.external_links = set()
        self.internal_links = set()
        self.absolute_internal_links = set()
        self.links = set()

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
        if not self.external_links:
            for link in self.get_all_links():
                if 'http' in link.get('href'):
                    self.external_links.add(link.get('href'))
        return self.external_links

    def get_internal_links(self):
        if not self.internal_links:
            for link in self.get_all_links():
                if 'http' not in link.get('href'):
                    self.internal_links.add(link.get('href'))
        return self.internal_links

    def get_all_links(self):
        if self.soup:
            if not self.links:
                self.links = set(self.soup.find_all('a', href=True))
        return self.links

    def get_absolute_internal_links(self):
        if not self.absolute_internal_links:
            for link in self.get_internal_links():
                self.absolute_internal_links.add(urljoin(self.url, link))
        return self.absolute_internal_links
