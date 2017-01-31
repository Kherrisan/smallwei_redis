# -*- coding: utf-8 -*-
# 模块列表类，需要包含所有的模块。
# 这个文件需要被RedisProcessor类包含。

from MessageStoreDBModule import MessageStoreDBModule
from TuringRobotModule import TuringRobotModule
from SignInModule import SignInModule, RegisterModule
from RemoteTerminalModule import RemoteTerminalModule
from NewYearBlessing import SendBlessingModule, ReceiveBlessingModule
from BindCardModule import BindCardModule
from RateAppearanceModule import RateAppearanceModule


class ProcessList:
    """封装了一个列表，这个列表定义了RedisProcessor调用哪些模块处理消息，已经处理消息的顺序。越往前的优先级越高。
    """
    processList = [MessageStoreDBModule, SendBlessingModule, ReceiveBlessingModule,
                   RateAppearanceModule, RegisterModule, BindCardModule, TuringRobotModule, ]
