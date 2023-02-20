from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager

db= SQLAlchemy()
DB_NAME="database.db"


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='this is the key'

    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Hols

    with app.app_context(): db.create_all()     #db function to create new db if doesnt exsist
                                                #sqlalchemy wont overwrite existing file

    login_manager=LoginManager() #initialise the login manager
    login_manager.login_view = 'auth.login' #direct to login page if not logged in
    login_manager.init_app(app)#tell it which app we are using

    @login_manager.user_loader  #telling flask how we load a user
    def load_user(id):
        return User.query.get(int(id)) #looks for primary key

    return app

