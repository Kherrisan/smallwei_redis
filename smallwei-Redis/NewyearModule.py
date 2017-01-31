# -*- coding:utf-8 -*-
# 新年特别模块

from BaseProcessModule import *
from GetInfoFromIni import *
from Message import *


class NewyearModule(BaseProcessModule):
    '''新年祝福特别模块

    主要功能实现：
    1.用户发送“福+想说的话”后，将用户的QQ账号数据存储到祝福清单的数据库中，并通过读取QQ_SEU.ini文件中的数据，获取用户的姓名和院系信息并存储（如果有）
    *2.将用户所发送的祝福的话通过py程序转换成html文件(string->jpg->html)，并用该用户的QQ账号命名此网页
    (将用户所发送的话通过py程序转换成jpg文件(string->jpg)由网页getQQ账号来实现不同祝福的传递)
    *3.通过死循环计时，每隔1分钟向队列中最前端用户发送rand(0.100+id)的对应的QQ号的网页，其中前100为小微默认祝福网页（本段程序可以考虑是否将用过的祝福删除）

    '''
    name = "NewyearModule"

    @staticmethod
    def process(message):
        try:
            temp = message.getContent()
            if temp[0] == u"福":
                fromQQ = str(message.getPersonQQ())
                # msg为所存储的祝福的话，使用模块将其转换为图片格式或者html格式
                msg = temp[1:]
                # 向文本中存储QQ账号、姓名、院系（如果有）等有关信息
                if getinfo(fromQQ)[0] == 0:
                    f_obj = open('Bless.ini', 'a')
                    seq = [str(fromQQ) + '\t|', msg.encode('utf-8') + '\r']
                    f_obj.writelines(seq)
                    f_obj.close()
                    message.setContent(u"已收录您的祝福，系统检测到您尚未注册，请回复“绑定+一卡通号”注册后享受完整功能哦！")
                else:
                    f_obj = open('Bless.ini', 'a')
                    seq = [str(fromQQ) + '\t|', msg.encode('utf-8') + '\t|',
                           getinfo(fromQQ)[2].decode('utf-8').encode('utf-8') + '\t|',
                           getinfo(fromQQ)[1].decode('utf-8').encode('utf-8') + '\r']
                    f_obj.writelines(seq)
                    f_obj.close()
                    message.setContent(u"来自" + getinfo(fromQQ)[2].decode('utf-8') + u"的" + getinfo(fromQQ)[1].decode(
                        'utf-8') + u"同学，您的祝福已经收集！请等待不久后来自陌生人的祝福哦~")
                return message, True, True
            else:
                return 0, False, False
        except Exception as e:
            print "[" + NewyearModule.name + "][info]" + e.message
            traceback.print_exc()
            return 0, False, False
