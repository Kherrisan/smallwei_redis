from DatabaseSession import *
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import traceback
import re

ALL_INFO_TABLE_NAME = "student_info"

Base = declarative_base()

engine = create_engine("mysql+mysqlconnector://remote:459861@115.159.53.213:3306/testsmallwei", pool_size=10)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
sess = Session()


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


def txt2db():
    fail = 0
    try:
        ini_path = open("QQ_SEU.ini", "r")
        for line in ini_path.xreadlines():
            args_list = line.split("\t|")
            print int(args_list[1])
            query = sess.query(StudentInfoModal).filter(StudentInfoModal.cardNo == int(args_list[1])).first()
            if not query:
                fail += 1
        print fail
        return
    except Exception as e:
        print e
        traceback.print_exc()
        return


if __name__ == '__main__':
    txt2db()
