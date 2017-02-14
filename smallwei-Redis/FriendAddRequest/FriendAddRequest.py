# -*- coding: utf-8 -*-

from Sender import *
from BaseProcessModule import *
from Logger import log


# add_friend_request content部分 "responseFlag#好友申请的内容"

class FriendAddRequest(BaseProcessModule):
    name = "FriendAddRequest"

    @staticmethod
    def process(message):
        if message.getSubType() == 12:
            try:
                content = message.getContent()
                msg = content[content.indexOf("#") + 1:]
                cardNum = int(msg)
                if not FriendAddRequest.validify_cardnum(cardNum):
                    return
                set_friend_add_request(message, REQUEST_ALLOW)
                return
            except ValueError as e:
                log(moduleName=FriendAddRequest.name, level="error", content=e)
                return
            except Block:
                raise Block()
            except Exception as e:
                log(moduleName=FriendAddRequest.name, level="error", content=e.message)
                return
        elif message.getSubType()==

    @staticmethod
    def validify_cardnum(cardNum):
        return False
