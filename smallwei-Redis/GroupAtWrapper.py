import re
from config import *


class GroupAtWrapper:
    def __init__(self, message):
        GROUP_AT_PATTERN = r"^\[CQ:at,qq=([0-9]+)\]"
        res = re.search(GROUP_AT_PATTERN, message.getContent())
        if res and res.group(1) == str(message.getTargetQQ()):
            self.message = message
            self.atFlag = True
        else:
            self.message = message
            self.atFlag = False

    def get_context_str(self):
        if self.message.getSubType()==1:
            return str(self.message.getPersonQQ())
        elif self.message.getSubType()==2:
            return str(self.message.getGroupQQ())+str(self.message.getPersonQQ())
        else:
            return str(self.message.getDiscussionQQ())+str(self.message.getPersonQQ())

    def at_someone(self, message=None):
        GROUP_AT_CQ = "[CQ:at,qq={0}]"
        if self.atFlag:
            return GROUP_AT_CQ.format(message.getPersonQQ())
        else:
            return ""
