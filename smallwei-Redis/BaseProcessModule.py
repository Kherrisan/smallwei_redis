# -*- coding: utf-8 -*-
import traceback
from config import *


class BaseProcessModule:
    """自定义模块的基类，所有的模块都要继承这个类。

    Attributes:
        runFlag:该模块的开关。
        hasError:该模块在运行过程中是否有错误的标识符，暂时还没有用。
    """
    runFlag = dict()
    runFlag[str(SMALLWEI_QQ)] = False
    runFlag[str(SMALLWEI2016_QQ)] = False
    hasError = False

    @classmethod
    def check(cls, qq):
        return cls.runFlag[str(qq)]

    @classmethod
    def start(cls, qq):
        """启动该模块的运作。"""
        cls.runFlag[str(qq)] = True

    @classmethod
    def stop(cls, qq):
        """停止该模块运作。"""
        cls.runFlag[str(qq)] = False
