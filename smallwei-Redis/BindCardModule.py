# -*- coding:utf-8 -*-
# 一卡通绑定模块

from BaseProcessModule import *
from GetInfoFromIni import *
from Message import *


class BindCardModule(BaseProcessModule):
    '''绑定信息模块

    主要功能实现：
    1.用户回复“绑定+一卡通号”将其QQ信息以及校内信息写入文件QQ_SEU.ini中

    '''
    name = "BindCardModule"
    @staticmethod
    def process(message):
        try:
            temp = message.getContent()
            #判断第一个字是否是“绑”
            if temp[0] == u"绑":
                fromQQ = str(message.getPersonQQ())
                #msg为一卡通账号
                msg = temp[2:]
                #判断当前QQ账号是否已经绑定过
                if getinfo(fromQQ)[0] == 0:
                    #判断当前一卡通是否在all_info.txt内
                    if insertinfo(fromQQ,msg):
                        message.setContent(u"绑定成功！")
                        return message , True, True
                    else:
                        message.setContent(u"请检查您的一卡通账号！")
                        return message , True, True
                else:
                    message.setContent(u"您已注册！")
                    return message , True, True
            else:
                return 0, False, False
        except Exception as e:
            print "[" + BindCardModule.name + "][info]" + e.message
            traceback.print_exc()
            return 0, False, False