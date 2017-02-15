# -*- coding: utf-8 -*-
# 这是python端的配置文件，有些内容需要和cpp端保持一致，再将来将提高配置文件的内聚。

DATABASE_URL = 'mysql+mysqlconnector://root:459861@localhost:3306/'  # mysql数据库的url
DATABASE_NAME = 'testsmallwei'  # 数据库的名字
DATABASE_CONNECTION_POOL_SIZE = 10  # 数据库连接池的尺寸

MESSAGE_TABLE_NAME = 'messagelist'  # 消息记录的数据表的表名

REDIS_IN_QUEUE_NAME = "smallwei:in"  # 从cq到py的任务队列的名字。需要和cpp中的一致。
SMALLWEI_QQ = 896153878  #
SMALLWEI2016_QQ = 459861669  #
# SMALLWEI_QQ = 1368994461  # 大微的qq号。
# SMALLWEI2016_QQ = 2762968041  # 小微2016的qq号。
REDIS_OUT_QUEUE_NAME_BIG = "smallweiout:" + str(SMALLWEI_QQ)  # 从py到大微的cq的任务队列的名字，需要和cpp中的一致。
REDIS_OUT_QUEUE_NAME_2016 = "smallweiout:" + str(SMALLWEI2016_QQ)  # 从py到小微2016的cq的任务队列的名字，需要和cpp中的一致。

REDIS_CONNECTION_HOST = "localhost"  # redis连接的主机名。
REDIS_CONNECTION_PORT = 6379  # redis连接的端口
REDIS_QUEUE_DB = 0  # redis连接的数据库的号码，默认为0。
REDIS_CONTEXT_CACHE_HASH_NAME = "smallwei:context"

SIGNIN_RECORDS_TABLE_NAME = 'signin_records'  # 签到记录的数据表的表名。
SIGNIN_USER_TABLE_NAME = "signin_user"  # 签到功能的用户表的表名。

TREEHOLE_TABLE_NAME = 'treehole'     # 树洞功能的数据表的表名。
YUNYINGQQ=588694674   #运营群群号

TURING_API_URL = "http://www.tuling123.com/openapi/api"  # 图灵机器人的api
TURING_KEY = "8a489e57bb34bc5295aaa695ec727122"  # 图灵机器人的key

BLESSING_TABLE_NAME = "blessings"
REDIS_BLESSING_WAITING_QUEUE = "blessqueue"

MAX_THREAD_NUM = 10


