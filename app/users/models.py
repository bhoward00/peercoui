from app import db
from db import Base
from app.mixins import CRUDMixin
from flask.ext.login import UserMixin
from sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash

class User(UserMixin, CRUDMixin,  Base):
    __table__ = Table('users_user', Base.metadata, autoload=True)



    ##### OLD - introspect in instead
    #__tablename__ = 'users_user'
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(50), unique=True)
    #email = db.Column(db.String(120), unique=True)
    #password = db.Column(db.String(120))

    #def __init__(self, name=None, email=None, password=None):
    #    self.name = name
    #    self.email = email
    #    self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)


    def set_password(self, password):
	self.pwdhash = generate_password_hash(password)
       
    def check_password(self, password):
     return check_password_hash(self.pwdhash, password)
