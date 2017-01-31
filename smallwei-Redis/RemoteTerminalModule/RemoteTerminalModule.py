# -*- coding: utf-8 -*-
# 远程操作的类。目前还有bug。
# 目前只实现了启动，重启，停止某个模块的命令。

# 命令格式为"@微[命令]:[模块名称]"不包含中括号。

from ModuleList import *
from BaseProcessModule import *
from Sender import *


class RemoteTerminalModule(BaseProcessModule):
    name = "RemoteTerminalModule"

    @staticmethod
    def process(message):
        try:
            content = message.getContent()[:]
            if content and len(content) > 2 and content[0] == "@" and content[1] == u"微":
                tempList = content[2:].split(":")
                call, arg = globals()[tempList[0]](), globals()[tempList[1]]  # 这一行是坠吼的，用到了反射。
                if call(arg):
                    print "[" + RemoteTerminalModule.name + "][info]" + content
                    message.setContent("[" + call.name + "]" + arg.name)
                    send(message, True)
        except TypeError as e:
            if isinstance(e,Block):
                raise Block()
            print "[" + RemoteTerminalModule.name + "][error]" + e.message
            traceback.print_exc()
            return


class restart:
    def __init__(self):
        self.name = "restart"

    def __call__(self, *args, **kwargs):
        args[0].stop()
        args[0].start()
        print "[stop]" + args[0].name
        print "[start]" + args[0].name
        return True


class stop:
    def __init__(self):
        self.name = "stop"

    def __call__(self, *args, **kwargs):
        args[0].stop()
        print "[stop]" + args[0].name
        return True


class start:
    def __init__(self):
        self.name = "start"

    def __call__(self, *args, **kwargs):
        args[0].start()
        print "[start]" + args[0].name
        return True


class InstructionException(Exception):
    def __init__(self, strInstruction):
        Exception().__init__(self)
        self.instruction = strInstruction

    def parse(self):
        tempList = self.instruction.split(":")
        return globals()[tempList[0]], globals()[tempList[1]]
