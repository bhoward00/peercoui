#from app import db
from db import session, Base
from flask.ext.login import UserMixin, current_user
from app.mixins import CRUDMixin
from sqlalchemy import *
from datetime import datetime



# turn single-field row results from query.first() to a straight up list:
#   ((1,),(2,),(3,)) to (1,2,3)
def sfrToList(rs):
    return map(lambda l: l[0],rs)


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

    @staticmethod
    def getValuesFromField(field):
	return sfrToList(session.query(getattr(Records,field)).distinct())
