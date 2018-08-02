from datetime import datetime
from  sqlalchemy import (Column, Integer, String, DateTime)
from sqlalchemy.sql import exists
from .db import Base, session

class User(Base):
    """
    user
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    password = Column(String(50), nullable=False)
    last_login = Column(DateTime,default=datetime.now)
    created = Column(DateTime,default=datetime.now)

    def __repr__(self):
        return '<User #{}: {}>'.format(self.id, self.name)


    @classmethod
    def is_exists(cls,username):
        return session.query(exists().where(User.name == username)).scalar()


    @classmethod
    def add_user(cls, username, password):
        user = User(name=username, password=password)
        session.add(user)
        session.commit()

    @classmethod
    def get_pass(cls, username):
        user = session.query(cls).filter_by(name=username).scalar()
        if user:
            return user.password
        else:
            return ''
