# -*- coding: utf-8 -*-
# 模块列表类，需要包含所有的模块。
# 这个文件需要被RedisProcessor类包含。

from BindCardModule.BindCardModule import BindCardModule
from MessageStoreDBModule.MessageStoreDBModule import MessageStoreDBModule
from NewYearBlessing.NewYearBlessing import SendBlessingModule, ReceiveBlessingModule
from RateAppearanceModule.RateAppearanceModule import RateAppearanceModule
from SignInModule.SignInModule import SignInModule, RegisterModule
from TuringRobotModule.TuringRobotModule import TuringRobotModule
from FriendAddRequest.FriendAddRequest import FriendAddRequest
from GroupAddRequest.GroupAddRequest import GroupAddRequest
from StudentInfoModule.StudentInfoModule import StudentInfoModule

class ProcessList:
    """封装了一个列表，这个列表定义了RedisProcessor调用哪些模块处理消息，已经处理消息的顺序。越往前的优先级越高。
    """
    processList = [MessageStoreDBModule, SendBlessingModule, ReceiveBlessingModule, SignInModule,StudentInfoModule,
                   RateAppearanceModule, RegisterModule, BindCardModule, TuringRobotModule, FriendAddRequest,
                   GroupAddRequest, ]
