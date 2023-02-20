from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth=Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':          #if button pressed
        email=request.form.get('email')             # get info from form
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()    # query if we have this user in db only first one
        if user:
            if check_password_hash(user.password, password):    #check password match
                flash ('Login Success!', category = 'ok')
                login_user(user, remember=True)          #on login success pass user to flask login function. remember if user logged in
                return redirect(url_for('views.home'))  #redirect to home  
            else:
                flash('Incorrect password, please try again.', category = 'error')  #if password wrong
        else:
            flash('Email incorrect, please try again.', category = 'error')      #if no user match                            
    
    return render_template("login.html", user=current_user) #this is to pass to HTML   

@auth.route('/logout')
@login_required # this makes sure this page cannot be accessed unless user logged in used with flask_login
def logout():
    logout_user()   #this is from the flask_login function and will logout automatically
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])    # all of these auto vlidate
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')             #these get information from form
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()    #check to see if user exists already
        if user:
            flash('User already exists.', category='error')

        elif password1!=password2:                    #check passwords against each other and send message
            flash("Password confirmation not the same as password. Please try again.", category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'))
            # this will create a new instance of user and hash the password / method='sha256' is the hashing algorythm

            db.session.add(new_user)    #adds the new user to the database

            db.session.commit()             #commit to db
            flash ('Sign up success!', category = 'ok')
            login_user(new_user, remember=True)          #on login success pass user to flask login function. remember if user logged in

            return redirect(url_for('views.home'))  #views is name of blueprint and home is name of function        
        
    return render_template("sign_up.html", user=current_user) #to pass to HTML



