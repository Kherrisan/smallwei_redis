# -*- coding: utf-8 -*-
# 核心文件，RedisProcessor类。定义了结构逻辑的主要流程。


import threading
from ModuleList import ProcessList
from RemoteTerminalModule import *
from Message import *
from DuplicateRemoval import DuplicateRemoval
import traceback
from RedisSession import *
from config import *



# 该函数判断该模块是否被启动，在运行中。
def run_flag_wrapper(module, message):
    """
    如果模块在运行，返回模块的处理结果。否则返回。。。。。。
    :param module: 模块类（模块的处理都是静态方法）。
    :param message: 需要用模块处理的message对象。
    :param qq:
    :return: 三个参数分别代表：返回的message对象，是否需要将message对象发送出去的标志位，是否需要拒绝后续模块处理的标志位。
    """
    if module.check(message.getTargetQQ()):
        return module.process(message)
    else:
        return 0, False, False


def switchoutqueue(qq):
    """

    :param qq: 根据message对象的targetQQ判断在py到cq的过程中，应该选择哪条队列。大微和小微2016的qq号在config中定义。
    :return: 队列名称，在config中定义。
    """
    print "SWITCHINGINGINGING    "+str(qq)
    if qq == SMALLWEI_QQ:
        return REDIS_OUT_QUEUE_NAME_BIG
    elif qq == SMALLWEI2016_QQ:
        return REDIS_OUT_QUEUE_NAME_2016
    else:
        return ""


class Precessor(threading.Thread):
    """核心核心类。继承自threading.Thread，有需要可以多线程运行。

    """

    def __init__(self, name):
        super(Precessor, self).__init__(name=name)
        self.runFlag = True
        self.isError = False
        self.redisConnection = redis.Redis(connection_pool=redisPool)

    def hasError(self):
        return self.isError

    def stop(self):
        self.runFlag = False

    def run(self):
        """
        该线程的死循环执行函数。从redis中取出消息，按照模块列表的顺序将message进行处理，再将需要发送出去的message放入队列中。
        如果出现了异常，如redis的blpop和rpush异常，则返回，停止该线程的运行。其他的在模块中发生的异常应有模块捕获，不能传播到这个函数体中。
        :return:
        """
        while True:
            try:
                print "[start]" + self.name
                while self.runFlag:
                    print "[waiting]"
                    dataStream = self.redisConnection.blpop(REDIS_IN_QUEUE_NAME)
                    print "[received]" + dataStream[1][:-1].decode("gbk")
                    message = Message.produceMessege(dataStream)  # 将原始字符串转换成message对象。
                    if not DuplicateRemoval.check_depulicate(message):
                        for itrProcessor in ProcessList.processList:  # 遍历模块列表中的每个模块，把message对象传进去。
                            rtnmessage, sendFlag, blockFlag = run_flag_wrapper(itrProcessor, message)
                            if sendFlag:
                                print "[send]" + rtnmessage.getJsonStr()
                                self.redisConnection.rpush(switchoutqueue(rtnmessage.getTargetQQ()), rtnmessage.getDataStream())
                            if blockFlag:  # 如果这个模块要求后面的模块不处理这条message。
                                break
            except Exception as e:
                self.isError = True
                traceback.print_exc()


if __name__ == "__main__":
    # 在测试阶段，默认启动所有的模块。
    for i in ProcessList.processList:
        i.start(SMALLWEI2016_QQ)
        i.start(SMALLWEI_QQ)
    p = Precessor("ppp")
    p.start()
    while True:
        pass
