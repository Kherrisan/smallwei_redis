# -*- coding: utf-8 -*-
# 聊天记录的记录模块。

from BaseProcessModule import *
from Message import *
from DatabaseSession import Session
from Sender import *
from Logger import log


class MessageStoreDBModule(BaseProcessModule):
    """该模块将所有小微可见的消息都写进数据库中。

    """
    name = "MessageStoreDBModule"

    @staticmethod
    def process(message):
        session = Session()
        try:
            session.add(Message.produceDBMessage(message))  # 根据Message对象生成MessageModel对象，并写入数据库中。
            log(moduleName=MessageStoreDBModule.name,content=message.getContent()+" "+str(message.getGroupQQ())+" "+str(message.getPersonQQ()))
            session.commit()  # 数据库实际上发生变化是在这一行之后。相当于提交了插入操作。
            return
        except Exception as e:
            if isinstance(e,Block):
                raise Block()
            log(moduleName=MessageStoreDBModule.name,level="error",content=e.message)
            return
        finally:
            session.close()
