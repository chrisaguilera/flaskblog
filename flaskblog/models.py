from mongoengine import Document, StringField, DateTimeField, ReferenceField

class User(Document):
    username = StringField()
    email = StringField()
    password = StringField()

class Post(Document):
    title = StringField()
    content = StringField()
    date_posted = DateTimeField()
    author = ReferenceField(User)
