#!/usr/bin/env python
from sqlalchemy import *
import sqlalchemy.dialects as postgres
import sqlalchemy.orm as orm
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import re
import sys, os
import dateutil.parser as dup


engine = create_engine('postgresql://bhoward@localhost:5432/GPeerCoDB')
engine.echo = False
#metadata = MetaData(bind=engine)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.metadata.bind = engine



class Records(Base):
    __table__ = Table('main_records', Base.metadata, autoload=True)

class User(Base):
    __table__ = Table('users_user', Base.metadata, autoload=True)

class Edits(Base):
    __table__ = Table('edits', Base.metadata, autoload=True)


os.environ['PYTHONINSPECT'] = 'True'
