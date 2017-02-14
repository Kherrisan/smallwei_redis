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


def main():
    file = open("info.csv", "r")
    file.read(3)
    try:
        for line in file.xreadlines():
            args_list = line.split(",")
            line_modal = StudentInfoModal(stuNo=args_list[1],
                                          cardNo=int(args_list[0]),
                                          name=args_list[2],
                                          dept=args_list[3],
                                          major=args_list[4],
                                          grade=int(args_list[0][3:5]))
            sess.add(line_modal)
        sess.commit()
    except Exception as e:
        print e.message
        traceback.print_exc()
    finally:
        file.close()
        return


if __name__ == '__main__':
    main()
