# -*- coding: utf-8 -*-

from facebook_crawler import FacebookCrawler

class MainCrawler():

    def __init__(self):
        self.minions = []
        self.minions.append(FacebookCrawler())


    def start(self):
        for minion in self.minions:
            minion.write_to_file()



crawler = MainCrawler()
crawler.start()