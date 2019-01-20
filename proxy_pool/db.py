MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
MYSQL_HOST = 'localhost'
MYSQL_USER = 'username'
MYSQL_PASSWORD = 'password'
MYSQL_TABLE = 'tablename'

import pymysql
from random import choice

class MysqlClient(object):
    def __init__(self, host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, table=MYSQL_TABLE):
        self.db = pymysql.connect(host, user, password, table)
        self.cursor = self.db.cursor()

    def add(self, proxy, score=INITIAL_SCORE):
        select_sql = "select * from agent_pool where agent = '%s'" % (proxy)
        insert_sql = "insert into agent_pool values('%s', '%s')" % (proxy, score)
        if not self.cursor.execute(select_sql):
            self.cursor.execute(insert_sql)
            return self.db.commit()

    def random(self):
        select_sql = "select agent from agent_pool where score = 100"
        self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        if len(result):
            return choice(result)[0]
        else:
            select_sql = "select agent from agent_pool where score < 100 and score > 0 limit 50"
            self.cursor.execute(select_sql)
            result = self.cursor.fetchall()
            if len(result):
                return choice(result)[0]
            else:
                return None

    def decrease(self, proxy):
        select_sql = "select score from agent_pool where agent = '%s'" % (proxy)
        update_sql = "update agent_pool set score = score + 1 where agent = '%s'" % (proxy)
        delete_sql = "delete from agent_pool where agent = '%s'" % (proxy)
        self.cursor.execute(select_sql)
        score = self.cursor.fetchone()[0]
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            self.cursor.execute(update_sql)
            self.db.commit()
        else:
            print('代理', proxy, '当前分数', score, '移除')
            self.cursor.execute(delete_sql)
            self.db.commit()

    def exists(self, proxy):
        select_sql = "select * from agent_pool where agent = '%s'" % (proxy)
        self.cursor.execute(select_sql)

    def max(self, proxy):
        update_sql = "update agent_pool set score = '%s' where agent = '%s'" % (MAX_SCORE, proxy)
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        self.cursor.execute(update_sql)
        self.db.commit()

    def count(self):
        select_sql = "select * from agent_pool"
        return self.cursor.execute(select_sql)

    def all(self):
        select_sql = "select agent from agent_pool"
        self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        proxies = []
        for proxy in result:
            proxies.append(proxy[0])
        return proxies
    def close(self):
        self.db.close()