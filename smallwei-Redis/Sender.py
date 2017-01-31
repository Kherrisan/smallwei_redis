# -*- coding: utf-8 -*-
from RedisSession import *
import redis
from config import *

redisConnnection = redis.Redis(connection_pool=redisPool)


def switchoutqueue(qq):
    """

    :param qq: 根据message对象的targetQQ判断在py到cq的过程中，应该选择哪条队列。大微和小微2016的qq号在config中定义。
    :return: 队列名称，在config中定义。
    """
    print "SWITCHINGINGINGING    " + str(qq)
    if qq == SMALLWEI_QQ:
        return REDIS_OUT_QUEUE_NAME_BIG
    elif qq == SMALLWEI2016_QQ:
        return REDIS_OUT_QUEUE_NAME_2016
    else:
        return ""


class Block(Exception):
    pass


def send(message, blocked):
    print "[send]" + message.getJsonStr()
    redisConnection.rpush(switchoutqueue(message.getTargetQQ()), message.getDataStream())
    if blocked:
        raise Block()
    else:
        return
