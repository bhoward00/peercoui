from flask.ext.wtf import Form, TextField, BooleanField, SelectField, HiddenField, RadioField, DateField, SubmitField,fields, validators, IntegerField, NumberRange, Length
from flask.ext.wtf import InputRequired, Email, EqualTo
from app.users.models import User
from app.records.models import Records
#from app import db
from db import Base, session



def pairup(mylist):
    for x in mylist:
	out.append((x,x))
    return out




class SelectRecord(Form):
    rid = RadioField("Record Select", choices=[], coerce=int,validators=[InputRequired()])
    cosub = SubmitField("Check Out")
    cisub = SubmitField("Check In")

    def validate(self):
	if not Form.validate(self):
	    return False
	if session.query(Records.id).filter(Records.id == self.rid.data):
	    return True
	else:
	    return False
    
###  debug - disable csrf
#    def __init__(self,*args,**kwargs):
#	kwargs['csrf_enabled'] = False
#	super(SelectRecord, self).__init__(*args,**kwargs)



class EditSomeRecords(Form):
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
    save	    = SubmitField("Save")
    cancel	    = SubmitField("Cancel")

