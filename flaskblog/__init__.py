from flask import Flask
from flask_bcrypt import Bcrypt
import pymongo
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '931e4b05996d46785a129699551ef3a3'
app.config['MONGODB_URI'] = 'mongodb+srv://chrisaguilera:lakers2416!@cluster0-degwh.mongodb.net/test?retryWrites=true'
client = pymongo.MongoClient(app.config['MONGODB_URI'])
db = client.flaskBlog

# Enforce unique username and email
db.users.create_index(
    [('username', pymongo.ASCENDING)],
    unique=True
)
db.users.create_index(
    [('email', pymongo.ASCENDING)],
    unique=True
)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskblog import routes
