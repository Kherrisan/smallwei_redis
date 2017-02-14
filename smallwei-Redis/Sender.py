# -*- coding: utf-8 -*-
from RedisSession import *
import redis
from config import *
from Logger import log

redisConnection = redis.Redis(connection_pool=redisPool)


def switchoutqueue(qq):
    """

    :param qq: 根据message对象的targetQQ判断在py到cq的过程中，应该选择哪条队列。大微和小微2016的qq号在config中定义。
    :return: 队列名称，在config中定义。
    """
    if qq == SMALLWEI_QQ:
        return REDIS_OUT_QUEUE_NAME_BIG
    elif qq == SMALLWEI2016_QQ:
        return REDIS_OUT_QUEUE_NAME_2016
    else:
        return ""


class Block(Exception):
    pass


REQUEST_ALLOW = 1
REQUEST_DENY = 2

REQUEST_GROUP_ADD = 1
REQUEST_GROUP_INVITE = 2


def set_friend_add_request(message, responseoperation):
    raw = message.getContent()
    index = raw.indexOf("#")
    raw[index + 1:] = str(responseoperation)
    message.setContent(raw)
    send(message, True)


def set_group_add_request(message, responseoperation):
    raw = message.getContent()
    index = raw.indexOf("#")
    raw[index + 1:] = responseoperation
    message.setContent(raw)
    send(message, True)


def send(message, blocked):
    log(moduleName="Sender", content=message.getJsonStr())
    redisConnection.rpush(switchoutqueue(
        message.getTargetQQ()), message.getDataStream())
    if blocked:
        raise Block()
    else:
        return
