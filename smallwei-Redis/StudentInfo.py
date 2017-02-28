from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

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
