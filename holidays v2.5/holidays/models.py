from . import db        #the . means current package (website)
from flask_login import UserMixin
#from sqlalchemy.sql import func     #this is to import the datetime

class Hols(db.Model):       # db.model is the layout for an object that will be stored in database (table)
    id=db.Column(db.Integer, primary_key=True)
    date1=db.Column(db.DateTime) 
    date2=db.Column(db.DateTime) 
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):    #user only need logon and password
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    hol=db.relationship('Hols')