# -*- coding:utf-8 -*-
# 学生信息模块

"""功能实现：
1.绑定功能（从当前数据库中检测注册信息是否合法）：绑定+一卡通号
--使用已有数据库，绑定结果返回文字信息
2.查信息功能（仅对制定管理人员有效，检查数据库）：查信息+一卡通号/QQ
--内部查人功能，通过输入部分信息，返回用户的所有信息
--已实现删除功能：解绑+一卡通号/QQ
3.查课表功能（对绑定完成后的学生提供的课表查询）：课表/查课表
4.查跑操功能（对绑定完成后的学生提供的跑操查询）：跑操/查跑操
--对外开放功能，已绑定的用户发送指定内容即可返回需要查询的信息
"""

from paocaoapi import *
import re

from config import *
from BaseProcessModule import *
from Sender import *
from Logger import log
from DatabaseSession import Session

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import datetime

Base = declarative_base()

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


class StudentInfoModule(BaseProcessModule):
    '''学生信息模块

    '''
    name = "StudentInfoModule"
    COURSE_TABLE_URL=u"[CQ:share,url=http://115.159.53.213:8000/coursetable?id={0},title=亲爱的{1}同学，您好！,content=点我直接查看课表哦~,image=http://q2.qlogo.cn/headimg_dl?dst_uin={2}&spec=100&url_enc=0&referer=bu_interface&term_type=PC]"
    INFO_REPLY_SCHEDULE = u"[CQ:share,url=http://xk.urp.seu.edu.cn/jw_service/service/lookCurriculum.action?queryStudentId={0}&queryAcademicYear=16-17-2,title=亲爱的{1}同学，您好！,content=课表请连接seu-wlan查询！,image=http://q2.qlogo.cn/headimg_dl?dst_uin={2}&spec=100&url_enc=0&referer=bu_interface&term_type=PC]"
    INFO_REPLY_PAOCAO = u"[CQ:share,title={0}同学，你已经跑了{1}次啦！,content=棒棒哒！还请继续加油哦！,image=http://q2.qlogo.cn/headimg_dl?dst_uin={2}&spec=100&url_enc=0&referer=bu_interface&term_type=PC]"
    INFO_REPLY_PAOCAO_2 = u"[CQ:share,title={0}同学，很抱歉,content=您的跑操次数{1}，如果不是高年级同学请等待修复哦~,image=http://q2.qlogo.cn/headimg_dl?dst_uin={2}&spec=100&url_enc=0&referer=bu_interface&term_type=PC]"
    INFO_REPLY_SIGNIN = u"[CQ:share,title={0}您好！点我查看课表,content=当前跑操次数：{1}\n时间：{2}\n日期：{3},image=http://q2.qlogo.cn/headimg_dl?dst_uin={4}&spec=100&url_enc=0&referer=bu_interface&term_type=PC,url=http://115.159.53.213:8000/coursetable?id={5}]"

    @staticmethod
    def process(message):
        session = Session()
        try:
            if message.getSubType() == 1 or message.getSubType() ==2:
                message.remove_group_at()
                content = message.getContent()
                #管理功能，较高权限
                #绑定功能：绑定 + 一卡通号
                if content[0:2] == u"绑定":
                    cardNo = int(content[2:].strip())
                    student_qq = session.query(StudentInfoModal).filter(StudentInfoModal.QQ == int(message.getPersonQQ())).first()
                    if not student_qq:
                        student = session.query(StudentInfoModal).filter(StudentInfoModal.cardNo == cardNo).first()
                        if not student:
                            message.setContent(u"没有找到此一卡通，请检查您的一卡通账号！")
                            if message.getSubType() == 2:
                                message.group_at()
                            send(message,True)
                            return
                        elif student.QQ is not None:
                            if student.QQ == message.getPersonQQ():
                                message.setContent(u"您已注册过！可以直接回复我“课表”查询课表哦~")
                            else:
                                message.setContent(u"该一卡通已经绑定过QQ了，请检查您的一卡通账号！")
                            if message.getSubType() == 2:
                                message.group_at()
                            send(message,True)
                            return
                        else:
                            student.QQ = message.getPersonQQ()
                            session.commit()
                            message.setContent(student.name + u"同学，您已经绑定成功！可以直接回复我“课表”查询课表哦~")
                            if message.getSubType() == 2:
                                message.group_at()
                            send(message,True)
                            return
                    else:
                        message.setContent(student_qq.name + u"同学，您已经绑定过啦！如有错误请发送您的一卡通到我邮箱哦~")
                        if message.getSubType() == 2:
                            message.group_at()
                        send(message,True)
                        return

                #管理员查信息功能：查信息 + 一卡通号 / QQ
                #只有开发群内有此权限
                elif content[0:3] == u"查信息" and message.getGroupQQ() == 588694674:
                    tempNo = content[3:].strip()
                    if int(tempNo)/1000000 == 213:
                        student = session.query(StudentInfoModal).filter(StudentInfoModal.cardNo == tempNo).first()
                    elif len(tempNo) == 8:
                        student = session.query(StudentInfoModal).filter(StudentInfoModal.stuNo == tempNo).first()
                    else:
                        student = session.query(StudentInfoModal).filter(StudentInfoModal.QQ == tempNo).first()
                    if not student:
                        message.setContent(u"尊敬的管理员：查询的目标不存在！")
                    else:
                        tempMsg = u"尊敬的管理员，你所查询的" + student.name + u"同学的信息如下：\n学号：" + str(student.stuNo) + u"\n一卡通：" + str(student.cardNo) + u"\nQQ：" + str(student.QQ) + u"\n院系：" + student.dept + u"\n专业：" + student.major
                        message.setContent(tempMsg)
                    if message.getSubType() == 2:
                        message.group_at()
                    send(message,True)
                    return

                #管理员解绑功能：解绑 + 一卡通号 / QQ
                #只有开发群内有此权限
                elif content[0:2] == u"解绑" and message.getGroupQQ() == 588694674:
                    tempNo = content[2:].strip()
                    #判断需要解除绑定的号码是否是一卡通号
                    if int(tempNo)/1000000 == 213:
                        student = session.query(StudentInfoModal).filter(StudentInfoModal.cardNo == tempNo).first()
                    elif len(tempNo) == 8:
                        student = session.query(StudentInfoModal).filter(StudentInfoModal.stuNo == tempNo).first()
                    else:
                        student = session.query(StudentInfoModal).filter(StudentInfoModal.QQ == tempNo).first()
                    if not student:
                        message.setContent(u"尊敬的管理员：查询的目标不存在！")
                    elif student.QQ is not None:
                        student.QQ = None
                        session.commit()
                        tempMsg = u"尊敬的管理员，" + student.name + u"同学的QQ信息已删除"
                        message.setContent(tempMsg)
                    else:
                        tempMsg = u"该一卡通账号尚未绑定QQ，请核实！"
                        message.setContent(tempMsg)
                    if message.getSubType() == 2:
                        message.group_at()
                    send(message,True)
                    return

                #用户功能，绑定后即查
                if content[0:3].find(u"课表") != -1 or content[0:3].find(u"跑操") != -1 or content[0].find(u"签") != -1:
                    student = session.query(StudentInfoModal).filter(StudentInfoModal.QQ == message.getPersonQQ()).first()
                    if not student:
                        message.setContent(u"您好，系统检测到您尚未绑定！请先回复“绑定+一卡通号”进行绑定！\n如：绑定213111111")
                        if message.getSubType() == 2:
                            message.group_at()
                        send(message,True)
                        return

                    else:
                        if content.find(u"课表") != -1:
                            tempMsg = StudentInfoModule.COURSE_TABLE_URL.format(student.stuNo,student.name,student.QQ)
                            message.setContent(tempMsg)
#                            群聊转私发代码
#                            if message.getSubType() == 2:
#                                message.setSubType(1)
#                                message.setGroupQQ(0)
                            send(message,True)
                            return
                        
                        elif content.find(u"跑操") != -1:
                            num = getpaocao(student.cardNo)
                            if num == '' or student.grade < 15:
                                tempMsg = StudentInfoModule.INFO_REPLY_PAOCAO_2.format(student.name,"N/A",student.QQ)
                            else:
                                tempMsg = StudentInfoModule.INFO_REPLY_PAOCAO.format(student.name,num,student.QQ)
                            message.setContent(tempMsg)
                            send(message,True)
                            return

                        elif content.find(u"签") != -1:
                            num = getpaocao(student.cardNo)
                            date = datetime.date.today()
                            time = str(datetime.datetime.now())[11:19]
                            if num == '' or student.grade < 15:
                                tempMsg = StudentInfoModule.INFO_REPLY_SIGNIN.format(student.name,"N/A",time,date,student.QQ,student.stuNo)
                            else:
                                tempMsg = StudentInfoModule.INFO_REPLY_SIGNIN.format(student.name,num,time,date,student.QQ,student.stuNo)
                            message.setContent(tempMsg)
                            if message.getSubType() == 2:
                                message.setSubType(1)
                                message.setGroupQQ(0)
                            send(message,True)
                            return

        except Exception as e:
            if isinstance(e, Block):
                raise Block()
            log(moduleName=StudentInfoModule.name, level="error", content=e.message)
            return
                    
                    

                        
                    