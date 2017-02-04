# -*- coding: utf-8 -*-
# 核心文件，RedisProcessor类。定义了结构逻辑的主要流程。


import threading
import traceback
# from RemoteTerminalModule import *
from RedisSession import *
from DuplicateRemoval import DuplicateRemoval
from Message import *
from config import *
from ModuleList import ProcessList
from Logger import log

redisConn = redis.Redis(connection_pool=redisPool)


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
        return


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
        log(moduleName="Thread",content="start")
        while True:
            try:
                while self.runFlag:
                    log(moduleName="Thread",content="waiting")
                    dataStream = self.redisConnection.blpop(REDIS_IN_QUEUE_NAME)
                    log(moduleName="Thread",content=dataStream[1][:-1].decode("gbk"))
                    message = Message.produceMessege(dataStream)  # 将原始字符串转换成message对象。
                    if not DuplicateRemoval.check_depulicate(message):
                        for itrProcessor in ProcessList.processList:  # 遍历模块列表中的每个模块，把message对象传进去。
                            run_flag_wrapper(itrProcessor, message)
            except Exception as e:
                pass


if __name__ == "__main__":
    # 在测试阶段，默认启动所有的模块。
    threadList = []
    try:
        for i in ProcessList.processList:
            i.start(SMALLWEI2016_QQ)
            i.start(SMALLWEI_QQ)

        for i in range(0, MAX_THREAD_NUM):
            p = Precessor("thread" + str(i))
            p.start()
            threadList.append(p)

        for it in threadList:
            it.join()

    except KeyboardInterrupt as e:
        print "exit...ByeBye........."
        pass
