from benefactors import db
from datetime import datetime
from enum import Enum

class genderEnum(Enum):
    male = 1
    female = 2
    others = 3

# class roleEnum(Enum):
#    consumer = 1
#    admin = 2

class statusEnum(Enum):
    open = 1
    in_progress = 2
    cancelled = 3
    closed = 4

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), primary_key=True)
    gender = db.Column( db.Enum(genderEnum), default = genderEnum.others)
    phone_number = db.Column(db.String(16), nullable = False)
    postal_code = db.Column(db.String(10), nullable = False)
    password = db.Column(db.String(20), nullable = False)
    # role = db.Column( db.Enum(roleEnum), nullable = False)
    display_pic = db.Column( db.String(20), default = 'default')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    date_deadline = db.Column(db.DateTime, nullable = False)
    status= db.Column( db.Enum(statusEnum), default = statusEnum.open, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

