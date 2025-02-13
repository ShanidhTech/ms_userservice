from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    user_type = Column(Integer)


class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True)    
    user_type = Column(String, unique=True, index=True)
