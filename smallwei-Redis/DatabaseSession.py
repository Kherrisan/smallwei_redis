# -*- coding: utf-8 -*-
# 提供数据库Session的文件，任何需要操作数据库的模块都需要包含该文件。

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import DATABASE_NAME, DATABASE_URL, DATABASE_CONNECTION_POOL_SIZE

engine = create_engine(DATABASE_URL + DATABASE_NAME, pool_size=DATABASE_CONNECTION_POOL_SIZE)  # 这里使用了数据库连接池，应该是支持多线程的。

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)  # Session()即可获得一个数据库连接。Session()是线程安全的。
