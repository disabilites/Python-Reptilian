from db import MysqlClient
from aiohttp import ClientError
import aiohttp
import asyncio
import time
from constants import *

class Tester(object):
    def __init__(self):
        self.mysql = MysqlClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.mysql.max(proxy)
                        print('代理可用', proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.mysql.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        print('开始测试')
        try:
            proxies = self.mysql.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
                asyncio.open_connection()
        except Exception as e:
            print('测试发生错误', e.args)
        self.mysql.close()