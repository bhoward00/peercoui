from flask import Blueprint, Response, render_template, flash, redirect, session, url_for, request
from flask.ext.login import current_user, login_required
from app import app, login_manager
from app import db
from app.records.models import Records
from app.records.forms import EditSomeRecords, SelectRecord
from db import session, Base
from datetime import datetime




mod = Blueprint('records', __name__)


def sfrToList(rs):
    return map(lambda l: l[0],rs)






def getNextRecord():
    # unreviewed records
    return  session.query(Records).filter(Records.status=='unreviewed').first()
    # logic to split things intelligently



def getChoicesFromField(field):
    return session.query(distinct(Records.field))
    



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
	    #return redirect('/record/edit.html')
	    return render_template('/records/edit.html',rid=r)
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


