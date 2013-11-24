from app import db
from db import session, Base
from flask.ext.login import UserMixin, current_user
from app.mixins import CRUDMixin
from sqlalchemy import *
import datetime


def getValuesFromField(field):
    return session.query(field).distinct()



class Records(UserMixin, CRUDMixin, Base):
    __table__ = Table('main_records', Base.metadata, autoload=True)


    def getNextRecord():
	# need better logic for getting the next one
	# find a case that is not present in checkouts (or not locked if present)
	pass


