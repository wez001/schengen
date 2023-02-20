from flask import render_template, request, flash, jsonify, Blueprint
from .models import Hols
from . import db
from flask_login import login_required, current_user
import json
from datetime import datetime
from .working import re_order_db, test

views=Blueprint('views',__name__)   

@views.route('/', methods=['GET','POST'])   #get and display holidays
@login_required # this makes sure this page cannot be accessed unless user logged in used with flask_login
def home():
    if request.method == 'POST':            #if buttin pressed get holiday dates and add to database
        d1=request.form.get('date1')
        d2=request.form.get('date2')                #recieved as string
        d1 = datetime.strptime(d1, '%Y-%m-%d')      #converts to datetime.date
        d2 = datetime.strptime(d2, '%Y-%m-%d')
        
        if d1>d2:
            flash('Invalid dates.', category = 'error')
            return render_template("home.html", user=current_user)
        
        new_hol = Hols(date1=d1, date2 = d2, user_id=current_user.id)
        re_order_db(new_hol)            #send to the reorder function as to not write db twice
        flash('Holiday added.',category='ok')

    return render_template("home.html", user=current_user)


@views.route('/about')          #about website
def about():
    return render_template("about.html", user=current_user)

@views.route('/daysleft', methods=['GET','POST'])   #select date and work out how many days left
@login_required
def daysleft():
    if request.method=='POST':          #if button pressed get data and work out days left from datebox
        d3=request.form.get("date3")
        d3 = datetime.strptime(d3, '%Y-%m-%d')
        days_left=test(d3)
    else:
        dtt=datetime.today()            #if not work out from todays date
        days_left=test(dtt) 
        d3=dtt                          #for passing to html

    return render_template("daysleft.html", user=current_user, dl=days_left.days, testdate=d3)


@views.route('/delete-hol', methods=['POST'])   #delete holiday from list
def delete_note():          #delete a holiday in db
    hol = json.loads(request.data)
    holId = hol['holId']
    hol=Hols.query.get(holId)
    if hol:
        if hol.user_id==current_user.id:
            db.session.delete(hol)
            db.session.commit()
    return jsonify({})