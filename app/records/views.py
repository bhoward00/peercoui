from flask import Blueprint, Response, render_template, flash, redirect, session, url_for, request
from flask.ext.login import current_user, login_required
from app import app, login_manager
from app import db
from app.records.models import Records
from app.records.forms import EditSomeRecords, SelectRecord
from db import session, Base
from datetime import datetime




mod = Blueprint('records', __name__)





def checkoutRecord(rid):
    if (rid not in session.query(Records.id)) or (not session.query(Records.locked).filter(Records.id == rid)):
	r = session.query(Records).filter(Records.id==rid)
	r.editing_uid = current_user.id
	r.date_out = datetime.now()
	session.commit()

def checkinRecord(rid):
    r = session.query(Records).filter(Records.id==rid)
    r.editing_uid = current_user.id
    r.date_in = datetime.now()
    session.commit()



def getNextRecord():
    # unreviewed records
    return  session.query(Records).filter(Records.status=='unreviewed').first()
    # logic to split things intelligently



def getChoicesFromField(field):
    return session.query(distinct(Records.field))
    



@mod.route('/select/', methods=('GET', 'POST'))
@login_required
def select_view():
    mychoices = []
    # determine which cases are checked out by user, pass them as options along with a "next"
    recs_co = session.query(Records.id).filter(Records.editing_uid == current_user.id).filter(Records.locked == True)
    form = SelectRecord(request.form)
    if form.validate_on_submit():
	rid = form.data.rid
	if form['btn'] == "checkout":
	    # check out the requested record
	    Records.checkoutRecord(rid)
	    #return redirect('/record/edit.html')
	    return render_template('/records/edit.html',rid=rid)
	elif form['btn'] == "checkin":
	    Records.checkinRecord(rid)
	    flash("Record checked in.")
    else:
	for x in recs_co:
	    mychoices.append((x.rid,"%s: %s (%s)" % (x.peerco, x.title, x.district, x.casenumber)))
	x = getNextRecord()
	mychoices.append((x.id,"%s: %s (%s %s)" % (x.peerco, x.title, x.district, x.casenumber)))
	form.rid.choices = mychoices
	return render_template('records/select.html', form=form)



@mod.route('/edit/<rid>', methods=('GET', 'POST'))
@login_required
def edit_view(rid):
    record = session.query(Records).filter(Record.id == rid)
    form = EditSomeRecords(request.form)

    # fill out the choices
    form.final_action.choices = getChoicesFromField('final_action')
    form.phase.choices = getChoicesFromField('phase')

    if form.validate_on_submit():
	# turn the form back into an object
        record = Records()
        form.populate_obj(record)
        session.add(record)
        session.commit()
        return redirect('/select/')
    return render_template('records/edit.html', form=form)


#@mod.route('/records/', methods=('GET', 'POST'))
#@login_required
#def records_view():
#    record = db.session.query(Records).filter(
#    form = EditSomeRecords(request.form,record)
#    #sites = current_user.sites.all()
#    if form.validate_on_submit():
#	# turn the form back into an object
#        record = Records()
#        form.populate_obj(record)
#        session.add(record)
#        session.commit()
#        return redirect('/select/')
#    return render_template('records/edit.html', form=form)
