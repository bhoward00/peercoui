from flask.ext.wtf import Form, TextField, BooleanField, SelectField, HiddenField, RadioField,fields, validators
from flask.ext.wtf import InputRequired, Email, EqualTo
from app.users.models import User
from app.records.models import Records
from app import db
from db import *



def pairup(mylist):
    for x in mylist:
	out.append((x,x))
    return out




class SelectRecord(Form):
    rid = RadioField("Record Select", choices=[], coerce=int,validators=[InputRequired()])

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
	# I know I can pass in obj, but I want to control the mapping (and generate my select lists)
    def __init__(self, record):
	status	    = SelectField("Status",default = record.status, 
			    choices=[   ('AutoReviewed','AutoReviewed'),
					('BHdone','BHdone'),
					('JMdone','JMdone'),
					('CRdone','CRdone'),
					('2d-pass','2d-pass')]
			    ,validators=[InputRequired()])
	filed_on	    = DateField("Filed Date", default = record.filed_on,validators=[InputRequired()])
	terminated_on   = DateField("Term Date", default = record.terminated_on,validators=[InputRequired()])
	term_de	    = IntegerField("Term DE", default = record.term_de,
			    validators=[InputRequired(),NumberRange(min=0)])
	is_early	    = BooleanField("is early?", default = record.is_early,validators=[InputRequired()])
	is_child	    = BooleanField("is child?", default = record.is_child,validators=[InputRequired()])
	is_stayed	    = BooleanField("is stayed?", default = record.is_stayed,validators=[InputRequired()])
	is_settled	    = BooleanField("is settled?", default = record.is_settled,validators=[InputRequired()])
	final_action    = SelectField("final action by Peer", default = record.final_action, 
			    choices=pairup(getValuesFromField(record.final_action)),validators=[InputRequired()])
	phase	    = SelectField("phase at Peer's termination",default = record.phase,
			    choices=pairup(getValuesFromField(record.phase)),validators=[InputRequired()])
	damages	    = IntegerField("Damages to the dollar",default = record.damages,
			    validators=[InputRequired(), NumberRange(min=0)])
	ent_type	    = SelectField("Entity Type", 
			    choices=[('OC','Operating Company'),('NPE','NPE'),('U','University'),('O','Other')], 
			    default=record.ent_type, validators=[InputRequired()])
	is_dj	    = BooleanField("is DJ?",default=record.is_dj,validators=[InputRequired()])
	claimant	    = BooleanField("is Claimant?",default=record.claimant, validators=[InputRequired()])
	claimdef	    = BooleanField("is Claim Def?",default=record.claimdef,validators=[InputRequired()])
	notes	    = TextField("Notes",default=record.notes,validators=[InputRequired(), Length(max=200)])


	id		    = HiddenField(record.id)

	#iplc_case_id    = HiddenField(record.iplc_case_id)
	#origin	    = HiddenField(record.origin)
	#peerco	    = HiddenField(record.peerco)
	#title	    = HiddenField(record.title)
	#district	    = HiddenField(record.district)
	#casenumber	    = HiddenField(record.casenumber)
	#orig_year	    = HiddenField(record.orig_year)




