from utils import get_page
from bs4 import BeautifulSoup

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
            print('成功获取代理', proxy)
        return proxies

    def crawler_cizi(self, page_count=4):
        base_url = 'https://www.xicidaili.com/nn/{}'
        urls = [base_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = get_page(url)
            soup = BeautifulSoup(html, 'lxml')
            table = soup.table
            for tr in table.select('tr'):
                td = tr.select('td')
                if td:
                    ip = td[1].text
                    port = td[2].text
                    yield ':'.join([ip,port])

    def crawler_89ip(self, page_count=10):
        base_url = 'http://www.89ip.cn/index_{}.html'
        urls = [base_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = get_page(url)
            soup = BeautifulSoup(html, 'lxml')
            table = soup.table
            for tr in table.select('tr'):
                td = tr.select('td')
                if td:
                    ip = td[0].text.strip()
                    port = td[1].text.strip()
                    yield ':'.join([ip, port])