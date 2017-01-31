# -*- coding: utf-8 -*-
# 签到模块。
# 目前还没有什么乱用。

from BaseProcessModule import BaseProcessModule
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import random
import datetime
from DatabaseSession import Session
import traceback

from config import *

Base = declarative_base()


class SignInRecordModal(Base):
    __tablename__ = SIGNIN_RECORDS_TABLE_NAME

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, unique=True)
    personQQ = Column(BigInteger, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    addedScore = Column(Float, nullable=False)


class SignInUserModal(Base):
    __tablename__ = SIGNIN_USER_TABLE_NAME

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    personQQ = Column(BigInteger, nullable=False, unique=True)
    nickName = Column(VARCHAR(20), nullable=False)
    totalSignIn = Column(Integer, nullable=False)
    totalScore = Column(Float, nullable=False)
    ctnSignIn = Column(Integer, nullable=False)
    last_Date = Column(Date, nullable=True)
    last_Time = Column(Time, nullable=True)


class SignInModule(BaseProcessModule):
    name = "SignInModule"
    URL=u"https://mqq.tenpay.com/qrhb?c=9C22#ChAQAARXARcBKBQAEJgTFiUAEjC0Vkb7k088GvkOEVYQx8y7BakL8rSa2s3vnO73elj4dam7DKLfRjbsxWD/XQWqwgQ="

    SIGNIN_SUCCESS_REPLY = u"[CQ:share,url={0},title={1},content={2},image={3}]"
    SIGNIN_SUCCESS_CONTENT = u"连续签到{0}次\n累积签到{1}次\n累积积分{2}分"

    USER_LOGO = u"http://q2.qlogo.cn/headimg_dl?dst_uin={0}&spec=100&url_enc=0&referer=bu_interface&term_type=PC"

    CTN_SIGNIN_SCORE_TIMES = 0.05

    SCORE_HOUR_MIN = 6
    SCORE_HOUR_MAX = 7
    SCORE_MAX = 10

    RANDOM_SCORE_HOUR_MIN = 8
    RANDOM_SCORE_HOUR_MAX = 9
    RANDOM_SCORE_MAX = 9
    RANDOM_SCORE_MIN = 5

    @staticmethod
    def getAt(message):
        a = message.getSubType()
        if message.getSubType() == 2:
            return u"[CQ:at,qq={0}]".format(message.getPersonQQ())
        else:
            return ""

    @staticmethod
    def getYesterday():
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        return yesterday

    @staticmethod
    def getToday():
        today = datetime.date.today()
        return today

    @staticmethod
    def getNowDatetime():
        nowDatetime = datetime.datetime.now()
        return nowDatetime

    @staticmethod
    def getNowTime():
        nowTime = datetime.datetime.now().time()
        return nowTime

    @staticmethod
    def isSignIn(msg):
        if msg[0] == u"签":
            return True
        return False

    @staticmethod
    def inSuitableTime():
        hour = SignInModule.getNowTime().hour
        if SignInModule.SCORE_HOUR_MAX <= hour <= SignInModule.SCORE_HOUR_MAX:
            return 1
        # elif SignInModule.RANDOM_SCORE_HOUR_MIN <= hour <= SignInModule.RANDOM_SCORE_HOUR_MAX:
        #     return 2
        # return 0
        else:
            return 2

    @staticmethod
    def getSuitableScore(ctnSignIn, scoreType):
        totalScore = 0
        baseScore = 0
        ctnScore = 0
        if scoreType == 1:
            baseScore = SignInModule.SCORE_MAX
        elif scoreType == 2:
            baseScore = random.randint(SignInModule.RANDOM_SCORE_MIN, SignInModule.RANDOM_SCORE_MAX)
        totalScore = baseScore * (1 + ctnSignIn * SignInModule.CTN_SIGNIN_SCORE_TIMES)
        return totalScore

    @staticmethod
    def isRank(msg):
        if msg[0]==u"榜":
            return True
        else:
            return False

    @staticmethod
    def process(message):
        session = Session()
        scoreType = 0
        ctnSignIn = 0
        latter_totalScore = 0
        latter_totalSignIn = 0
        try:
            msg = message.getContent()
            if SignInModule.isSignIn(msg):
                # 签到口令
                print "[signin]" + str(message.getPersonQQ())
                if SignInModule.inSuitableTime() == 0:
                    print "[signin]--TimeWrong" + str(message.getPersonQQ())
                    reply = SignInModule.getAt(message) + u"【签到失败】\n只能在6-9点之间签到哦。"
                    message.setContent(reply)
                    return message, True, True
                elif SignInModule.inSuitableTime() == 1:
                    scoreType = 1
                else:
                    scoreType = 2
                query = session.query(SignInUserModal).filter(
                    SignInUserModal.personQQ == message.getPersonQQ()
                ).first()
                # 如果此人之前签过到，即数据库有此用户
                if query:
                    ctnSignIn = query.ctnSignIn
                    if query.last_Date == SignInModule.getToday():
                        reply = SignInModule.getAt(message) + u"您今天已经签到过了，明天再来试试吧!"
                        message.setContent(reply)
                        return message, True, True
                    else:
                        addedScore = SignInModule.getSuitableScore(query.ctnSignIn, scoreType=scoreType)
                        record = SignInRecordModal(
                            personQQ=message.getPersonQQ(),
                            date=datetime.datetime.fromtimestamp(message.getSendTime()).date(),
                            time=datetime.datetime.fromtimestamp(message.getSendTime()).time(),
                            addedScore=addedScore
                        )
                        session.add(record)
                        session.commit()
                        # update
                        latter_totalSignIn = query.totalSignIn + 1
                        latter_totalScore = query.totalScore + addedScore
                    if query.last_Date == SignInModule.getYesterday():
                        ctnSignIn = ctnSignIn + 1
                    else:
                        ctnSignIn = 0
                    query.ctnSignIn = ctnSignIn
                    query.totalScore = latter_totalScore
                    query.totalSignIn = latter_totalSignIn
                    query.last_Date = datetime.datetime.fromtimestamp(message.getSendTime()).date()
                    query.last_Time = datetime.datetime.fromtimestamp(message.getSendTime()).time()
                    session.commit()

                    print "[" + SignInModule.name + "]"
                    reply = SignInModule.SIGNIN_SUCCESS_REPLY.format(SignInModule.URL,
                                                                     query.nickName,
                                                                     SignInModule.SIGNIN_SUCCESS_CONTENT.format(
                                                                         ctnSignIn,
                                                                         latter_totalSignIn,
                                                                        latter_totalScore),
                                                                     SignInModule.USER_LOGO.format(message.getPersonQQ()))
                    # 返回内容
                    message.setContent(reply)
                    return message, True, False
                else:  # 如果此人之前未签过到，即数据库无此用户
                    print "[signin]--unRegister--" + str(message.getPersonQQ())
                    reply = SignInModule.getAt(message) + u"您尚未注册，输入[注册 昵称]即可注册，例: 注册 李云龙 "
                    message.setContent(reply)
                    return message, True, True
            elif SignInModule.isRank(msg):
                newContent=u"签到排行榜："
                query=session.query(SignInUserModal).order_by(desc(SignInUserModal.totalScore)).limit(6).all()
                for iq in range(0,len(query)):
                    newContent+=u"\n{0}.{1}:{2}分".format(iq,query[iq].nickname,query[iq].totalScore)
                message.setContent(SignInModule.getAt(message)+newContent)
                return message,True,True
            else:
                return 0, False, False
        except Exception as e:  #
            print "[" + SignInModule.name + "][error]" + e.message
            traceback.print_exc()
            return 0, False, False
        finally:
            session.close()


class RegisterModule(BaseProcessModule):
    name = "RegisterModule"

    @staticmethod
    def isRegitser(msg):
        msgS = msg.split(u' ')
        if len(msgS) == 2:
            if msgS[0] == u"注册":
                return True
        return False

    @staticmethod
    def process(message):
        session = Session()
        try:
            msg = message.getContent()
            if RegisterModule.isRegitser(msg):
                # 注册口令
                print "[register]" + str(message.getPersonQQ())
                query = session.query(SignInUserModal).filter(
                    SignInUserModal.personQQ == message.getPersonQQ()
                ).first()
                if query:
                    reply = SignInModule.getAt(message) + u"你已经注册过了啦\n现在回复“签”试一下吧~"
                    message.setContent(reply)
                    return message, True, True
                personQQ = message.getPersonQQ()
                nickName = msg.split(' ')[1]
                totalSignIn = 0
                totalScore = 0
                ctnSignIn = 0
                last_Date = SignInModule.getYesterday()
                last_Time = SignInModule.getNowTime()
                record = SignInUserModal(
                    personQQ=personQQ,
                    nickName=nickName,
                    totalSignIn=totalSignIn,
                    totalScore=totalScore,
                    ctnSignIn=ctnSignIn,
                    last_Date=last_Date,
                    last_Time=last_Time
                )
                session.add(record)
                session.commit()
                reply = SignInModule.getAt(message) + u"注册成功!\n现在回复“签”试一下吧~"
                message.setContent(reply)
                return message, True, True
            else:
                return 0, False, False
        except Exception as e:
            #
            print "[" + RegisterModule.name + "][error]" + e.message
            traceback.print_exc()
            return 0, False, False
        finally:
            session.close()
