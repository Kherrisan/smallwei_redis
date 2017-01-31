# -*- coding:utf-8 -*-
# 新年特别模块 发送模块

from BaseProcessModule import *
from GetInfoFromIni import *
from Message import *

import random

num = 0


class SendBlessModule(BaseProcessModule):
    '''新年祝福特别模块

    主要功能实现：
    *1.用户发送“福+想说的话”后，将用户的QQ账号数据存储到祝福清单的数据库中，并通过读取QQ_SEU.ini文件中的数据，获取用户的姓名和院系信息并存储（如果有）
    2.将用户所发送的祝福的话通过py程序转换成html文件(string->jpg->html)，并用该用户的QQ账号命名此网页
    (将用户所发送的话通过py程序转换成jpg文件(string->jpg)由网页getQQ账号来实现不同祝福的传递)
    3.通过死循环计时，每隔1分钟向队列中最前端用户发送rand(0.100+id)的对应的QQ号的网页，其中前100为小微默认祝福网页（本段程序可以考虑是否将用过的祝福删除）

    '''
    name = "SendBlessModule"

    @staticmethod
    def process(message):
        try:
            temp = message.getContent()
            global num
            num += 1
            print num
            # 根据总体发言情况预估需要发送消息的频率，每接受到100条信息的时候发送一条
            # 从第100行开始计次，前100行为默认祝福
            '''
            当前测试阶段为接受一条发送一条
            修改为100条应当将下面的 num % 1 == 0 和 num // 1 == i - 100 中的1改为100

            '''
            if num % 1 == 0:
                f_obj = open('Bless.ini')
                i = 0
                line = ""
                for line in f_obj:
                    the_text = f_obj.next()
                    print the_text
                    i += 1
                    if i >= 50:
                        break
                for line in f_obj:
                    the_text = f_obj.next()
                    print the_text
                    i += 1
                    if num // 1 == i - 100:
                        frombless = random.randint(1, i - 1)
                        toqnum = the_text[0:the_text.find('\t')]
                        message.setPersonQQ(int(toqnum))
                        message.setGroupQQ(0)
                        message.setDiscussionQQ(0)
                        # message.setTargetQQ(1368994461)
                        message.setSubType(1)
                        f_obj.close()
                        f_o = open('Bless.ini')
                        t = -1
                        for line2 in f_o:
                            t += 1
                            text = f_o.next()
                            if t == frombless:
                                print t
                                message.setContent(
                                    text[text.find('|') + 1:text.find('\t', text.find('\t|') + 1)].decode('utf-8'))
                                print "S1"
                                f_o.close()
                                return message, True, True
            return 0, False, False
        except Exception as e:
            print "[" + SendBlessModule.name + "][info]" + e.message
            traceback.print_exc()
            return 0, False, False
