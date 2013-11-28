from flask import Blueprint, Response, render_template, flash, redirect, session, url_for, request
from flask.ext.login import current_user, login_required
from app import app, login_manager
#from app import db
from app.records.models import Records, Edits
from app.records.forms import EditForm, SelectRecord, AutoIncrement
from db import session, Base
from datetime import datetime
import sqlalchemy




mod = Blueprint('records', __name__)


# turn a sqlalchemy row into a dict by field-name
row2dict = lambda r: {c.name: getattr(r,c.name) for c in r.__table__.columns}
    

def getNextRecord():
    x = remainingRecords()
    return x[0] if x else None

def remainingRecords():
    # unreviewed records have no open edits - either in and out are both null (never edited) or 
    # both are not null (edit has closed)
    return  session.query(Records).join(Edits).filter(Records.status=='unreviewed').\
	filter( ( (Edits.date_out==None) & (Edits.date_in==None) ) | \
	    ( (Edits.date_out!=None) & (Edits.date_in!=None ) )  ).all()


def listToChoices(l, bAddNull=False):
    mychoices = []
    for x in l:
	mychoices.append((x,x))
    if bAddNull:
	mychoices.append((None,""))
    return mychoices
    
def getCheckouts():
    edits = session.query(Edits).filter(Edits.uid==current_user.id).filter(Edits.date_in == None).all()
    checkouts = [] 
    for e in edits:
	checkouts.append((e,session.query(Records).filter(Records.id == e.rid).first()))
    return checkouts




@mod.route('/select/', methods=('GET', 'POST'))
@login_required
def select_view():
    form = SelectRecord(request.form)
    mychoices = []
    # determine which cases are checked out by user
    checkouts = getCheckouts()
    if checkouts:
	for (e,x) in checkouts:
	    mychoices.append((x.id,"Peer %s: %s (%s in %s) checked out on %s"\
		% (x.peerco, x.title, x.casenumber, x.district, e.date_out)))
    form.rid.choices = mychoices
    newrec = True
    if form.validate_on_submit():
	if request.form['subbtn'] == form.newsub:
	    #app.logger.debug("checkout new")
	    rec = getNextRecord()
	    if not rec:
		flash("No more unreviewed records")
		redirect("/select/")
	    app.logger.debug("check out %d" % rec.id)
	    msg = rec.checkout(current_user.id)
	    flash(msg)
	elif form.rid.data:
	    rec = session.query(Records).filter(Records.id==form.rid.data).first()
	if not rec:
	    flash("Record not found")
	    return render_template('records/select.html', form=form, newrec=newrec, co_recs=checkouts)
	if request.form['subbtn'] == form.cisub:
	    app.logger.debug("checkin")
	    rec.checkin(current_user.id)
	    flash("Record checked in.")
	    #return render_template('records/select.html', form=form, newrec=newrec, co_recs=checkouts)
	    return redirect("/select/")
	return redirect("/edit/%d" % rec.id)
    else:
	app.logger.debug("select form validation failed")
	if form.errors:
	    app.logger.debug(form.errors)
	    flash("error")
	return render_template('records/select.html', form=form, co_recs = checkouts)



@mod.route('/edit/', methods=('GET', 'POST'))
@login_required
def fake():
    app.logger.debug("empty /edit/ called - redirecting")
    return redirect("/select/")






@mod.route('/edit/<rid>', methods=('GET', 'POST'))
@login_required
def edit_view(rid):


    #debug
    if(request.form.has_key('subbtn')):
	subbtn = request.form['subbtn']
	app.logger.debug("subbtn = %s" % subbtn)
    else:
	app.logger.debug("no subbtn key")
	subbtn=None


    rec = session.query(Records).filter(Records.id == rid).first()
    form = EditForm(request.form, obj=rec)

    # set choices
    l = Records.getValuesFromField('phase')
    form.phase.choices = listToChoices(l)
    form.final_action.choices = listToChoices(Records.getValuesFromField('final_action'))

    if form.validate_on_submit():
	val = True
    else:
	val = False

    if subbtn:
	if subbtn == form.cancel:
	    app.logger.debug("cancel")
	    flash("Changes canceled")
	    return redirect('/select/')
	else:
	    app.logger.debug("saving record")
	    #form.populate_obj(rec)  # fucks up boolean nulls
	    data = form.data
	    for d in data:
		print "ghetto populate: %s -> %s" % (d, data[d])
		setattr(rec,d,data[d])
	    if val and not subbtn==form.saveselect:
		rec.status ="%s-done" % session.query(User).filter(id=uid).first().initials
	    session.add(rec)
	    session.commit()
	if subbtn == form.savenext:
	    rec.checkin(current_user.id)
	    n = getNextRecord()
	    msg = record.checkout(current_user.id)
	    flash(msg)
	    return redirect('/edit/%d' % n.id)
	elif subbtn==form.saveselect:
	    flash("Record saved but not checked in")
	    return redirect('/select/')
	    
	if form.errors:
	    app.logger.debug("oh shit:")
	    app.logger.debug(form.errors)
	flash("error")
	app.logger.debug("edit form validation failed")
    return render_template('records/edit.html', form=form, rec=rec, idx=AutoIncrement() ) 


