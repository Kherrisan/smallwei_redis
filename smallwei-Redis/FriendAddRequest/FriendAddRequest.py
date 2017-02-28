# -*- coding: utf-8 -*-

from Sender import *
import re
from BaseProcessModule import *
from Logger import log
from DatabaseSession import Session

# add_friend_request content部分 "responseFlag#好友申请的内容"

from StudentInfo import StudentInfoModal


class FriendAddRequest(BaseProcessModule):
    name = "FriendAddRequest"

    @staticmethod
    def process(message):
        if message.getSubType() == 12:
            try:
                # content 即为一卡通号或者准考证号。
                content = message.getContent()
		content=re.search(ur"[0-9]+",content).group(0)
                cardNum = int(content)
                if not FriendAddRequest.validify_cardnum(cardNum):
                    return
                set_friend_add_request(message, message.getResponseFlag(), REQUEST_ALLOW)
                return
            except ValueError as e:
                log(moduleName=FriendAddRequest.name, level="error", content=e)
                return
            except Block:
                raise Block()
            except Exception as e:
                log(moduleName=FriendAddRequest.name, level="error", content=e.message)
                return

    @staticmethod
    def validify_cardnum(cardNum):
        session = Session()
        try:
            student = session.query(StudentInfoModal).filter(StudentInfoModal.cardNo == cardNum).first()
            if not student:
                return False
            else:
                return True
        except Exception as e:
            log(moduleName=FriendAddRequest.name, level="error", content=e.message)
            return False
