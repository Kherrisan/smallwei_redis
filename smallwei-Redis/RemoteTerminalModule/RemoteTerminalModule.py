# -*- coding: utf-8 -*-
# 远程操作的类。目前还有bug。
# 目前只实现了启动，重启，停止某个模块的命令。

# 命令格式为"@微[命令]:[模块名称]"不包含中括号。

from ModuleList import *
from BaseProcessModule import *
from Sender import *
from Logger import log


class RemoteTerminalModule(BaseProcessModule):
    name = "RemoteTerminalModule"

    @staticmethod
    def process(message):
        try:
            content = message.getContent()[:]
            if content and len(content) > 2 and content[0] == "@" and content[1] == u"微":
                log(moduleName=RemoteTerminalModule.name,content=content)
                tempList = content[2:].split(":")
                call, arg = globals()[tempList[0]](), globals()[tempList[1]]  # 这一行是坠吼的，用到了反射。
                if call(arg):
                    message.setContent("[" + call.name + "]" + arg.name)
                    send(message, True)
        except TypeError as e:
            if isinstance(e,Block):
                raise Block()
            log(moduleName=RemoteTerminalModule.name,level="error",content=e.message)
            return


class restart:
    def __init__(self):
        self.name = "restart"

    def __call__(self, *args, **kwargs):
        args[0].stop()
        args[0].start()
        log(moduleName=RemoteTerminalModule.name,content="[stop]" + args[0].name)
        log(moduleName=RemoteTerminalModule.name,content="[start]" + args[0].name)
        return True


class stop:
    def __init__(self):
        self.name = "stop"

    def __call__(self, *args, **kwargs):
        args[0].stop()
        log(moduleName=RemoteTerminalModule.name,content="[stop]" + args[0].name)
        return True


class start:
    def __init__(self):
        self.name = "start"

    def __call__(self, *args, **kwargs):
        args[0].start()
        log(moduleName=RemoteTerminalModule.name,content="[start]" + args[0].name)
        return True


class InstructionException(Exception):
    def __init__(self, strInstruction):
        Exception().__init__(self)
        self.instruction = strInstruction

    def parse(self):
        tempList = self.instruction.split(":")
        return globals()[tempList[0]], globals()[tempList[1]]
