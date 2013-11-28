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


    def __repr__(self):
	return "<Edit id=%d uid=%d rid=%d in=%s out=%s>" % (self.id, self.uid, self.rid, self.date_in, self.date_out)

class Records(UserMixin, CRUDMixin, Base):
    __table__ = Table('main_records', Base.metadata, autoload=True)


    def checkout(self,uid):
	check = session.query(Edits).filter(Edits.uid==uid).filter(Edits.rid==self.id).\
	    filter(Edits.date_out != None).filter(Edits.date_in == None).first()
	if check:
	    return "Record already checked out by %s" % session.query(User.name).filter(User.id==uid).first()[0]
	else:
	    edit = Edits(uid,self.id)
	    edit.date_out = datetime.now()
	    edit.date_in = None
	    session.add(edit)
	    session.commit()
	    #self.status="%s-done" % session.query(User).filter(id=uid).first().initials
	    #session.add(self)
	    return "Record checked out"

    def checkin(self,uid, bStatusDone=False):
	edit = session.query(Edits).filter(Edits.uid==uid).filter(Edits.rid==self.id).\
	    filter(Edits.date_in == None).first()
	edit.date_in = datetime.now()
	session.add(edit)
	session.commit()
	if bStatusDone:
	    self.status="%s-done" % session.query(User).filter(User.id==uid).first().initials
	    session.add(self)
	    session.commit()

    @staticmethod
    def getValuesFromField(f):
	return sfrToList( session.query(getattr(Records,f)).distinct().all() )



