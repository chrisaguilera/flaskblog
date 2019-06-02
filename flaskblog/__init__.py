import os
from flask import Flask
from flask_bcrypt import Bcrypt
import pymongo
from flask_login import LoginManager
from mongoengine import connect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config['MONGODB_URI'] = 'mongodb+srv://chrisaguilera:lakers2416!@cluster0-degwh.mongodb.net/flaskBlog'
connect(db='flaskBlog',host='mongodb+srv://chrisaguilera:lakers2416!@cluster0-degwh.mongodb.net/flaskBlog')

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
