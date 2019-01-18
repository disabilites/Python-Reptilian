from db import MysqlClient
from spider import Spider

MAX_POOL_COUNT = 10000

class Getter():
    def __init__(self):
        self.mysql = MysqlClient()
        self.spider = Spider()

    def is_over_max(self):
        if self.spider.count >= MAX_POOL_COUNT:
            return True
        else:
            return False

    def run(self):
        print('爬虫程序开始执行')
        if not self.is_over_max():
            for callback_lable in range(self.spider.__SpiderFuncCount__):
                callback = self.spider.__SpiderFunc__[callback_lable]
                proxies = self.spider.get_proxies(callback)
                for proxy in proxies:
                    self.mysql.add(proxy)