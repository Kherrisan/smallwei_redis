# -*- coding: utf-8 -*-
from Logger import log
from BaseProcessModule import BaseProcessModule
from DatabaseSession import Session
from StudentInfo import StudentInfoModal
import re
from Sender import *
from config import *

class GroupAddRequest(BaseProcessModule):
    name = "GroupAddRequest"

    GROUP_CARD_TEMPLATE = u"{0}-{1}-{2}"

    @staticmethod
    def validify_freshman(content):
        # 假设新生申请加入新生群的验证信息为姓名加准考证号，例如：邹迪凯1732xxxxxxxxx
        import re
        res = re.search(ur"([\u4e00-\u9fa5]+)(\d{14})", content)
        if not res:
            return None, None
        else:
            name = res.group(1)
            num = res.group(2)
            return name, num

    @staticmethod
    def process(message):
        message = message[:]
        session = Session()
        content = message.getContent()
	content=re.search(ur"[0-9]+",content).group(0)
        try:
            name, num = GroupAddRequest.validify_freshman(content)
            if message.getSubType() == 13:
                # 如果是有人申请加入小微管理的群的话。
                if len(content) == 9:
                    cardNo = int(content)
                    # 从数据库中查询验证信息中的一卡通号
                    student = session.query(StudentInfoModal).filter(StudentInfoModal.cardNo == cardNo).first()
                    if not student:
                        set_group_add_request(message, message.getResponseFlag(), REQUEST_DENY)
                    else:
                        set_group_add_request(message, message.getResponseFlag(), REQUEST_ALLOW)
                        deptAbbr = DEPARTMENT_ABBR_MAP[student.dept]
                        set_group_card(message, message.getGroupQQ(), message.getPersonQQ(),
                                       GroupAddRequest.GROUP_CARD_TEMPLATE.format(student.grade, deptAbbr,
                                                                                  student.name))
                        raise Block()
                elif name:
                    try:
                        province = NUM_PORVINCES_MAP[num[2:4]]
                        grade = int(num[0:2])
                        set_group_add_request(message, message.getResponseFlag(), REQUEST_ALLOW)
                        set_group_card(message, message.getGroupQQ(), message.getPersonQQ(),
                                       GroupAddRequest.GROUP_CARD_TEMPLATE.format(grade, province, name))
                        raise Block()
                    except KeyError:
                        set_group_add_request(message, message.getResponseFlag(), REQUEST_DENY)
                else:
                    set_group_add_request(message, message.getResponseFlag(), REQUEST_DENY)
        except Exception as e:
            if isinstance(e, Block):
                raise Block()
            log(moduleName=GroupAddRequest.name, level="error", content=e.message)
            return
