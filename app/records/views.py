from flask import Blueprint, Response, render_template, flash, redirect, session, url_for, request
from flask.ext.login import current_user, login_required
from app import app, login_manager
#from app import db
from app.records.models import Records, Edits
from app.records.forms import EditSomeRecords, SelectRecord, AutoIncrement
from db import session, Base
from datetime import datetime




mod = Blueprint('records', __name__)


# turn a sqlalchemy row into a dict by field-name
row2dict = lambda r: {c.name: getattr(r,c.name) for c in r.__table__.columns}
    

def getNextRecord():
    # unreviewed records
    return  session.query(Records).filter(Records.status=='unreviewed').first()
    # logic to split things intelligently

def remainingRecords():
    # unreviewed records
    return  session.query(Records).filter(Records.status=='unreviewed').all()


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
    edits = session.query(Edits).filter(Edits.uid==current_user.id).filter(Edits.date_in == None).all()
    for e in edits:
	x = session.query(Records).filter(Records.id == e.rid).first()
	mychoices.append((x.id,"Peer %s: %s (%s in %s) checked out on %s" % (x.peerco, x.title, x.casenumber, x.district, e.date_out)))
    form.rid.choices = mychoices
    co_recs = True if edits else False
    newrec = True if remainingRecords() else False
    if form.validate_on_submit():
	if form.newsub.data:
	    app.logger.debug("checkout new")
	    rec = getNextRecord()
	elif form.rid.data:
	    rec = session.query(Records).filter(Records.id==form.rid.data).first()
	if not rec:
	    flash("Record not found")
	    return render_template('records/select.html', form=form, newrec=newrec, co_recs = co_recs)
	if form.cisub.data:
	    app.logger.debug("checkin")
	    rec.checkinRecord(current_user.id)
	    flash("Record checked in.")
	    return render_template('records/select.html', form=form, newrec=newrec, co_recs = co_recs)
	app.logger.debug("checkout")
	msg = rec.checkoutRecord(current_user.id)
	flash(msg)
	return redirect("/edit/%d" % rec.id)
	#return render_template('/records/edit.html',rid=r)
    else:
	app.logger.debug("select form validation failed")
	if form.errors:
	    app.logger.debug(form.errors)
	    flash("error")
	return render_template('records/select.html', form=form, newrec=newrec, co_recs = co_recs)



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
    return render_template('records/edit.html', form=form, caseinfo=caseinfo, idx=AutoIncrement())


