#from app import db
from db import session, Base
from flask.ext.login import UserMixin, current_user
from app.mixins import CRUDMixin
from sqlalchemy import *
from datetime import datetime


def getValuesFromField(field):
    return session.query(field).distinct()



class Records(UserMixin, CRUDMixin, Base):
    __table__ = Table('main_records', Base.metadata, autoload=True)


    def checkoutRecord(self,uid):
	self.editing_uid = uid
	self.date_out = datetime.now()
	return self

    def checkinRecord(self,uid):
	self.editing_uid = uid
	self.date_in = datetime.now()
	return self
