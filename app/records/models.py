#from app import db
from db import session, Base
from flask.ext.login import UserMixin, current_user
from app.mixins import CRUDMixin
from sqlalchemy import *
from datetime import datetime
from app.users.models import User



# turn single-field row results from query.first() to a straight up list:
#   ((1,),(2,),(3,)) to (1,2,3)
def sfrToList(rs):
    return map(lambda l: l[0],rs)




class Edits(UserMixin, CRUDMixin, Base):
    __table__ = Table('edits', Base.metadata, autoload=True)

    def __init__(self, uid, rid):
	self.uid = uid
	self.rid = rid


class Records(UserMixin, CRUDMixin, Base):
    __table__ = Table('main_records', Base.metadata, autoload=True)


    def checkoutRecord(self,uid):
	
	check = session.query(Edits).filter(Edits.uid==uid).filter(Edits.rid==self.id).filter(Edits.date_in == None).first()
	if check:
	    return "Record already checked out by %s" % session.query(User.name).filter(User.id==uid).first()[0]
	else:
	    edit = Edits(uid,self.id)
	    edit.date_out = datetime.now()
	    edit.date_in = None
	    session.add(edit)
	    session.commit()
	    return "Record checked out"

    def checkinRecord(self,uid):
	edit = session.query(Edits).filter(Edits.uid==uid).filter(Edits.rid==self.id).\
	    filter(Edits.date_in == None).first()
	edit.date_in = datetime.now()
	session.add(edit)
	session.commit()

    @staticmethod
    def getValuesFromField(field):
	return sfrToList(session.query(getattr(Records,field)).distinct())
