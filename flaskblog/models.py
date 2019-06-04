from mongoengine import Document, StringField, DateTimeField, ReferenceField
from flask_login import UserMixin
from flaskblog import login_manager
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

class User(Document, UserMixin):
    username = StringField(unique=True, required=True)
    email = StringField(unique=True, required=True)
    password = StringField(required=True)
    image_file = StringField(default='default.jpg')

class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    date_posted = DateTimeField(default=datetime.datetime.now())
    author = ReferenceField(User, required=True)
