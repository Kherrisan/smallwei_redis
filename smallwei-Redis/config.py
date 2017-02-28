# -*- coding: utf-8 -*-
# 这是python端的配置文件，有些内容需要和cpp端保持一致，再将来将提高配置文件的内聚。

DATABASE_URL = 'mysql+mysqlconnector://root:459861@localhost:3306/'  # mysql数据库的url
DATABASE_NAME = 'testsmallwei'  # 数据库的名字
DATABASE_CONNECTION_POOL_SIZE = 10  # 数据库连接池的尺寸

MESSAGE_TABLE_NAME = 'messagelist'  # 消息记录的数据表的表名

REDIS_IN_QUEUE_NAME = "smallwei:in"  # 从cq到py的任务队列的名字。需要和cpp中的一致。
#SMALLWEI_QQ = 896153878  #
#SMALLWEI2016_QQ = 459861669  #
SMALLWEI_QQ = 1368994461  # 大微的qq号。
SMALLWEI2016_QQ = 2762968041  # 小微2016的qq号。
REDIS_OUT_QUEUE_NAME_BIG = "smallweiout:" + str(SMALLWEI_QQ)  # 从py到大微的cq的任务队列的名字，需要和cpp中的一致。
REDIS_OUT_QUEUE_NAME_2016 = "smallweiout:" + str(SMALLWEI2016_QQ)  # 从py到小微2016的cq的任务队列的名字，需要和cpp中的一致。

REDIS_CONNECTION_HOST = "localhost"  # redis连接的主机名。
REDIS_CONNECTION_PORT = 6379  # redis连接的端口
REDIS_QUEUE_DB = 0  # redis连接的数据库的号码，默认为0。
REDIS_CONTEXT_CACHE_HASH_NAME = "smallwei:context"

SIGNIN_RECORDS_TABLE_NAME = 'signin_records'  # 签到记录的数据表的表名。
SIGNIN_USER_TABLE_NAME = "signin_user"  # 签到功能的用户表的表名。

TREEHOLE_TABLE_NAME = 'treehole'     # 树洞功能的数据表的表名。
YUNYINGQQ=588694674   #运营群群号

TURING_API_URL = "http://www.tuling123.com/openapi/api"  # 图灵机器人的api
TURING_KEY = "8a489e57bb34bc5295aaa695ec727122"  # 图灵机器人的key

BLESSING_TABLE_NAME = "blessings"
REDIS_BLESSING_WAITING_QUEUE = "blessqueue"

MAX_THREAD_NUM = 10

NUM_PORVINCES_MAP = {
    "11": u"北京",
    "12": u"天津",
    "13": u"河北",
    "14": u"山西",
    "15": u"内蒙",
    "21": u"辽宁",
    "22": u"吉林",
    "23": u"黑龙江",
    "31": u"上海",
    "32": u"江苏",
    "33": u"浙江",
    "34": u"安徽",
    "35": u"福建",
    "36": u"江西",
    "37": u"山东",
    "41": u"河北",
    "42": u"湖北",
    "43": u"湖南",
    "44": u"广东",
    "45": u"广西",
    "46": u"海南",
    "50": u"重庆",
    "51": u"四川",
    "52": u"贵州",
    "53": u"云南",
    "54": u"西藏",
    "61": u"陕西",
    "62": u"甘肃",
    "63": u"青海",
    "64": u"宁夏",
    "65": u"新疆"
}

DEPARTMENT_ABBR_MAP = {
    u"[100337]艺术学院": u"艺术",
    u"[100285]经济管理学院": u"经管",
    u"[100342]法学院": u"法学院",
    u"[100304]外国语学院": u"外院",
    u"[100331]仪器科学与工程学院": u"仪科",
    u"[100295]电气工程学院": u"电气",
    u"[100180]机械工程学院": u"机械",
    u"[100247]计算机科学与工程学院": u"计科",
    u"[100193]能源与环境学院": u"能环",
    u"[100372]医学院": u"医学院",
    u"[100365]公共卫生学院": u"公卫",
    u"[100314]化学化工学院": u"化学",
    u"[100319]交通学院": u"交通",
    u"[100272]材料科学与工程学院": u"材料",
    u"[100202]信息科学与工程学院": u"信息",
    u"[100242]自动化学院": u"自动化",
    u"[100215]土木工程学院": u"土木",
    u"[100278]人文学院": u"人文",
    u"[100225]电子科学与工程学院": u"电子",
    u"[100234]数学系": u"数学",
    u"[100265]生物科学与医学工程学院": u"生医",
    u"[100259]物理系": u"物理",
    u"[100172]建筑学院": u"建筑",
    u"[100383]软件学院": u"软件",
    u"[100381]吴健雄学院": u"吴院",
    u"[100351]医学院": u"医学院",
    u"[100157]学习科学研究中心": u"学科",
}
