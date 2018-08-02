from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'wang'
USERNAME = 'tudo'
PASSWORD = 'qwe123'

DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

engine = create_engine(DB_URL)
dbSession = sessionmaker(bind=engine)
session = dbSession()
Base = declarative_base(engine)