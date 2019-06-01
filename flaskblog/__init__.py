from flask import Flask
from flask_bcrypt import Bcrypt
import pymongo
from flask_login import LoginManager
from mongoengine import connect

app = Flask(__name__)
app.config['SECRET_KEY'] = '931e4b05996d46785a129699551ef3a3'
app.config['MONGODB_URI'] = 'mongodb+srv://chrisaguilera:lakers2416!@cluster0-degwh.mongodb.net/flaskBlog'
connect(db='flaskBlog',host='mongodb+srv://chrisaguilera:lakers2416!@cluster0-degwh.mongodb.net/flaskBlog')

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskblog import routes
