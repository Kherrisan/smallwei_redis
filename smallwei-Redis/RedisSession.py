# -*- coding: utf-8 -*-
import redis
from config import *

redisPool = redis.ConnectionPool(host=REDIS_CONNECTION_HOST, port=REDIS_CONNECTION_PORT,
                                 db=REDIS_QUEUE_DB)  # 连接到Redis数据库。Redis连接是线程安全的。