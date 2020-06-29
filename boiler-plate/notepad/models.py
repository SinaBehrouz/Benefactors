from notepad import db
from datetime import datetime
from enum import Enum

#@ask: what is this????!??
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # def __repr__(self):
    #     return f"Note('{self.author}', '{self.title}', '{self.date_posted}')"

class genderEnum(Enum):
    male = 1
    female = 2
    others = 3
class roleEnum(Enum):
    consumer = 1
    admin = 2
class statusEnum(Enum):
    open = 1
    in_progress = 2
    cancelled = 3
    closed = 4

class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(20), nullable = False)
    gender = db.Column( db.Enum(genderEnum), default = genderEnum.others)
    phone_number = db.Column(db.String(16), nullable = False)
    postal_code = db.Column(db.String(10), nullable = False)
    role = db.Column( db.Enum(roleEnum), nullable = False)
    display_pic = db.Column( db.String(20), default = 'default')

    posts = db.relationship('Post', backref='Author', lazy=True)
    def __repr__(self):
        return str(self.email)+'|'+str(self.first_name)+'|'+str(self.last_name)
        # return f"User('{self.email}'| '{self.first_name}'| '{self.last_name}')"

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    #sample DateTime value: 2020-06-28 20:40:55.952515
    date_deadline = db.Column(db.DateTime, nullable = False)
    status= db.Column( db.Enum(statusEnum), nullable = False)
    author_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable = False)
    def __repr__(self):
        return str(self.title) + " | " + str(self.author_email)
        # return f"Post('{self.title}'| '{self.date_posted}' )"
