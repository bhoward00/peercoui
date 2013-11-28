from flask.ext.wtf import Form, TextField, BooleanField, SelectField, HiddenField, RadioField, DateField, SubmitField,fields, validators, IntegerField, NumberRange, Length
from flask.ext.wtf import InputRequired, Email, EqualTo, Optional
from app.users.models import User
from app.records.models import Records
#from app import db
from db import Base, session
from app.validators import RequiredIf, RequiredIfNot
from app import app



def pairup(mylist):
    for x in mylist:
	out.append((x,x))
    return out


class AutoIncrement():
    def __init__(self):
	self.count = 1;
    def next(self):
	self.count = self.count +1
	return self.count



class SelectRecord(Form):
    #rid = RadioField("Record Select", choices=[], coerce=int,validators=[RequiredIfNot('newsub')])
    rid = RadioField("Record Select", choices=[], coerce=int,validators=[Optional()])
    editsub = "Edit Record"
    cisub = "Check In Record"
    newsub = "Check Out New Record"

#    def validate(self):
#	if not Form.validate(self):
#	    return False
#	if session.query(Records.id).filter(Records.id == self.rid.data):
#	    return True
#	else:
#	    return False
    
###  debug - disable csrf
#    def __init__(self,*args,**kwargs):
#	kwargs['csrf_enabled'] = False
#	super(SelectRecord, self).__init__(*args,**kwargs)



class EditForm(Form):
	# rather than passing in an obj to populate, I want dynamic population for choices & defaults
	# these are set in views.py after the form is created, before validate_on_submit
    status	    = SelectField("Status",
			choices=[   ('AutoReviewed','AutoReviewed'),
				    ('BHdone','BHdone'),
				    ('JMdone','JMdone'),
				    ('CRdone','CRdone'),
				    ('2d-pass','2d-pass')]
			,validators=[InputRequired()])
    filed_on	    = DateField("Filed Date", validators=[InputRequired()])
    terminated_on   = DateField("Termination Date", validators=[InputRequired()])
    term_de	    = IntegerField("Terminating DE for Peer",
			validators=[InputRequired(),NumberRange(min=0)])
    is_early	    = BooleanField("Is early?", validators=[InputRequired()])
    is_child	    = BooleanField("Is child?", validators=[InputRequired()])
    is_stayed	    = BooleanField("Is stayed?", validators=[InputRequired()])
    is_settled	    = BooleanField("Is settled?", validators=[InputRequired()])
    final_action    = SelectField("Final action by Peer",  choices=[],validators=[InputRequired()])
    phase	    = SelectField("Phase at Peer's termination", validators=[InputRequired()])
    damages	    = IntegerField("Damages to the dollar", validators=[InputRequired(), NumberRange(min=0)])
    ent_type	    = SelectField("Entity Type", 
			choices=[('OC','Operating Company'),('NPE','NPE'),('U','University'),('O','Other')], 
			validators=[InputRequired()])
    is_dj	    = BooleanField("Is DJ?", validators=[InputRequired()])
    claimant	    = BooleanField("Is Claimant?", validators=[InputRequired()])
    claimdef	    = BooleanField("Is Claim Def?",validators=[InputRequired()])
    notes	    = TextField("Notes", validators=[InputRequired(), Length(max=200)])
    savenext	    = "Save & Edit Next Record"
    saveselect	    = "Save & Select Record"
    cancel	    = "Cancel changes"



