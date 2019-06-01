from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime

class User(Document):
    username = StringField(unique=True, required=True)
    email = StringField(unique=True, required=True)
    password = StringField(required=True)

class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    date_posted = DateTimeField(default=datetime.datetime.now())
    author = ReferenceField(User, required=True)
