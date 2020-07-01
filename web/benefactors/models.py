from enum import Enum
from benefactors import db, login_manager
from datetime import datetime
from flask_login import UserMixin


class genderEnum(Enum):
    male = 1
    female = 2
    others = 3

# TODO: Reevaluate role requirement. Technically admin will have direct DB access and doesn't need an account.
"""
class roleEnum(Enum):
    consumer = 1
    admin = 2
"""

class statusEnum(Enum):
    open = 1
    in_progress = 2
    cancelled = 3
    closed = 4

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # gender = db.Column( db.Enum(genderEnum), default = genderEnum.others)
    phone_number = db.Column(db.String(16), nullable = False)
    postal_code = db.Column(db.String(10), nullable = False)
    password = db.Column(db.String(20), nullable = False)
    # role = db.Column( db.Enum(roleEnum), nullable = False)
    user_image = db.Column(db.String(40), default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # deadline = db.Column(db.DateTime, nullable = False)
    status= db.Column(db.Enum(statusEnum), default=statusEnum.open)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"