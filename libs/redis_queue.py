#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/7/30 11:30 
# @Author : mingyang.liang
# @Site :  
# @File : redis_queue.py 
# @Software: PyCharm
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis

REDIS_HOST = '120.79.155.209'
REDIS_PORT = 6379
REDIS_PASSWORD = 'Root123$'
REDIS_DB = 5


class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwargs):
        # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义选择哪个redis数据库,默认是0号数据库
        self.__db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
        self.key = '%s_%s' % (name, namespace)

    def qsize(self):
        return self.__db.scard(self.key)  # 返回队列里面集合元素的数量

    def put(self, item):
        self.__db.sadd(self.key, item)  # 添加新元素到队列最右方

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.spop(self.key)
        return item


if __name__ == '__main__':
    queue = RedisQueue('UNIQLO')
    print(queue.qsize())
    print(queue.get_nowait())


# zara统计
"""
河北 15020

"""

