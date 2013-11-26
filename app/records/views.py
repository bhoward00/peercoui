from flask import Blueprint, Response, render_template, flash, redirect, session, url_for, request
from flask.ext.login import current_user, login_required
from app import app, login_manager
#from app import db
from app.records.models import Records
from app.records.forms import EditSomeRecords, SelectRecord
from db import session, Base
from datetime import datetime




mod = Blueprint('records', __name__)


# turn a sqlalchemy row into a dict by field-name
row2dict = lambda r: {c.name: getattr(r,c.name) for c in r.__table__.columns}
    

def getNextRecord():
    # unreviewed records
    return  session.query(Records).filter(Records.status=='unreviewed').first()
    # logic to split things intelligently


def listToChoices(l, bAddNull=False):
    mychoices = []
    for x in l:
	mychoices.append((x,x))
    if bAddNull:
	mychoices.append((None,""))
    return mychoices
    



@mod.route('/select/', methods=('GET', 'POST'))
@login_required
def select_view():
    form = SelectRecord(request.form)
    mychoices = []
    # determine which cases are checked out by user, pass them as options along with a "next"
    recs_co = session.query(Records.id).filter(Records.editing_uid == current_user.id).  \
	filter(Records.locked == True)
    for x in recs_co:
	mychoices.append((x.rid,"%s: %s (%s)" % (x.peerco, x.title, x.district, x.casenumber)))
    x = getNextRecord()
    mychoices.append((x.id,"%s: %s (%s %s)" % (x.peerco, x.title, x.district, x.casenumber)))
    form.rid.choices = mychoices
    if form.validate_on_submit():
	r = form.rid.data
	app.logger.debug("rid = %d" % r)
	rec = session.query(Records).filter(Records.id==r).first()
	if not rec:
	    flash("Record not found")
	    return render_template('records/select.html', form=form)
	if form.cosub:
	    # check out the requested record
	    if rec.locked:
		flash("Record already locked by %s" % session.query(User.name).\
		    filter(User.id==rec.editing_uid).first()[0])
		return render_template('records/select.html', form=form)
	    n = rec.checkoutRecord(current_user.id)
	    session.add(n)
	    session.commit()
	    flash("Record checked out")
	    return redirect("/edit/%d" % n.id)
	    #return render_template('/records/edit.html',rid=r)
	elif form.cisub:
	    n = rec.checkinRecord(current_user.id)
	    session.add(n)
	    session.commit()
	    flash("Record checked in.")
	    return render_template('records/select.html', form=form)
    else:
	print form.errors
	return render_template('records/select.html', form=form)



@mod.route('/edit/<rid>', methods=('GET', 'POST'))
@login_required
def edit_view(rid):
    record = session.query(Records).filter(Records.id == rid).first()
    form = EditSomeRecords(request.form)

    # set choices
    form.phase.choices = listToChoices(Records.getValuesFromField('phase'))
    form.final_action.choices = listToChoices(Records.getValuesFromField('final_action'))

    #set defaults - consider moving below validation to not clobber selections if problem
    form.status.default = "Done"+ current_user.initials
    form.filed_on.default = record.filed_on
    form.terminated_on.default = record.terminated_on
    form.term_de.default = record.term_de
    form.is_early.default = record.is_early
    form.is_child.default = record.is_child
    form.is_stayed.default = record.is_stayed
    form.is_settled.default = record.is_settled
    form.final_action.default = record.final_action
    form.phase.default = record.phase
    form.damages.default = record.damages
    form.ent_type.default = record.ent_type
    form.is_dj.default = record.is_dj
    form.claimant.default = record.claimant
    form.claimdef.default = record.claimdef
    form.notes.default = record.notes
    if form.validate_on_submit():
	# turn the form back into an object
	if form.save:
	    form.populate_obj(record)
	    session.add(record)
	    session.commit()
        return redirect('/select/')
    caseinfo = {
	'rid'	    : record.id,
	'title'	    : record.title, 
	'caseno'    : record.casenumber, 
	'peerco'    : record.peerco, 
	'district'  : record.district,
	'caseid'    : record.iplc_case_id, 
	'filed_on'  : record.filed_on, 
	'origin'    : record.origin }
    return render_template('records/edit.html', form=form, caseinfo=caseinfo)


