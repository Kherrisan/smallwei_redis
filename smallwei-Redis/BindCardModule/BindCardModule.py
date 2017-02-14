# -*- coding:utf-8 -*-
# 一卡通绑定模块
from config import *
from GetInfoFromIni import *
from BaseProcessModule import *
from Sender import *
from Logger import log
from DatabaseSession import Session

ALL_INFO_TABLE_NAME = "student_info"

class StudentInfoModal(Base):
    __tablename__ = ALL_INFO_TABLE_NAME

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    stuNo = Column(TEXT, nullable=False)
    cardNo = Column(BigInteger, nullable=False)
    name = Column(TEXT, nullable=False)
    dept = Column(TEXT, nullable=False)
    major = Column(TEXT, nullable=False)
    QQ = Column(BigInteger, nullable=True)
    grade = Column(Integer, nullable=False)
    password = Column(TEXT, nullable=True)


class BindCardModule(BaseProcessModule):
    '''绑定信息模块

    主要功能实现：
    1.用户回复“绑定+一卡通号”将其QQ信息以及校内信息写入文件QQ_SEU.ini中

    '''
    name = "BindCardModule"

    @staticmethod
    def process(message):
        session = Session()
        try:
            if message.getSubType() == 1 or message.getSubType() == 2:
                message.remove_group_at()
                content = message.getContent()
                if content[0] == u"绑":
                    cardNo = int(content[1:].strip())
                    student = session.query(StudentInfoModal).filter(
                        StudentInfoModal.cardNo == cardNo).first()
                    if not student:
                        message.setContent(u"请检查您的一卡通账号！")
                        if message.getSubType() == 2:
                            message.group_at()
                        send(message)
                        return
                    if student.QQ is not None:
                        # 该用户提供的一卡通号已经被注册。
                        if student.QQ == message.getPersonQQ():
                            # 该用户想要注册的一卡通号对应的qq就是该用户qq。
                            message.setContent(u"您已注册！")
                        else:
                            # 该用户想要注册的一卡通号对应的qq不是该用户qq。
                            message.setContent(u"请检查您的一卡通账号！")
                        if message.getSubType() == 2:
                            message.group_at()
                        send(message)
                        return
                    else:
                        student.QQ = message.getPersonQQ()
                        session.commit()
                        message.setContent(u"绑定成功！")
                        if message.getSubType() == 2:
                            message.group_at()
                        send(message)
                        return
        except Exception as e:
            if isinstance(e, Block):
                raise Block()
            log(moduleName=BindCardModule.name, level="error", content=e.message)
            return

    @staticmethod
    def process_(message):
        try:
            temp = message.getContent()
            # 判断第一个字是否是“绑”
            if temp[0] == u"绑":
                fromQQ = str(message.getPersonQQ())
                # msg为一卡通账号
                msg = temp[2:]
                log(moduleName=BindCardModule.name, level="info", content=str(fromQQ) + " " + msg)
                # 判断当前QQ账号是否已经绑定过
                if getinfo(fromQQ)[0] == 0:
                    # 判断当前一卡通是否在all_info.txt内
                    if insertinfo(fromQQ, msg):
                        message.setContent(u"绑定成功！")
                        send(message, True)
                    else:
                        message.setContent(u"请检查您的一卡通账号！")
                        send(message, True)
                else:
                    message.setContent(u"您已注册！")
                    send(message, True)
            else:
                return
        except Exception as e:
            if isinstance(e, Block):
                raise Block()
            log(moduleName=BindCardModule.name, level="error", content=e.message)
            return
