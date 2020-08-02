from enum import Enum
from benefactors import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class genderEnum(Enum):
    male = 1
    female = 2
    others = 3


class statusEnum(Enum):
    OPEN = 1
    TAKEN = 2
    CANCELLED = 3
    CLOSED = 4

class categoryEnum(Enum):
    CLEANING = 1
    DELIVERY = 2
    MOVING = 3
    ERRANDS = 4
    TRANSPORTATION = 5
    LABOUR = 6
    GROCERY = 7
    MEDICATION = 8
    OTHERS = 9

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_image = db.Column(db.String(40), default='default.jpg')

    posts = db.relationship('Post', backref='author', lazy=True, foreign_keys='Post.user_id')
    comments = db.relationship('PostComment', backref='cmt_author', lazy=True, foreign_keys='PostComment.user_id')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.Enum(categoryEnum), nullable=False)
    status = db.Column(db.Enum(statusEnum), default=statusEnum.OPEN)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    volunteer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=0)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_desc = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.post_id}', '{self.user_id}', '{self.comment_desc}')"
