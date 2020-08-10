from enum import Enum
from benefactors import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref


class genderEnum(Enum):
    male = 1
    female = 2
    others = 3

class notificationTypeEnum(Enum):
    VOLUNTEER = 1
    UN_VOLUNTEER = 2
    COMMENT = 3
    STATUS = 4
    COM_VOLUNTEER = 5
    STATUS_CLOSED = 6
    STATUS_OPEN = 7
    DELETED = 8
    POST_DELETED_VOLUNTEER = 9
    POST_DELETED_COM = 10


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


class channelStatusEnum(Enum):
    READ = 1
    DELIVERED = 2


class messageStatusEnum(Enum):
    SENT = 1
    DELETED = 2


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------------------------------Account----------------------------------------------------------

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
    reviews = db.relationship('UserReview', backref='rev_author', lazy=True, foreign_keys='UserReview.author')

    channels = db.relationship('ChatMessages', backref='channel_user', lazy=True, foreign_keys='ChatMessages.sender_id')

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


# ----------------------------------------------------Posts-------------------------------------------------------------

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


# ----------------------------------------------------Comments----------------------------------------------------------

class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_desc = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"PostComment('{self.post_id}', '{self.user_id}', '{self.comment_desc}')"


# ----------------------------------------------------Reviews-----------------------------------------------------------

class UserReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    score = db.Column(db.Numeric, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"UserReview('{self.description}', '{self.score}''{self.date_posted}')"


# ------------------------------------------------------Messages--------------------------------------------------------

# User1 and User2 cannot switch position, let's say user1 has a chat channel with user2, user 2 should have the same channel with user 1.
# You cannot have two channels between two same users twice, unless the channel is closed
class ChatChannel(db.Model):
    __tablename__ = "chatchannel"

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # always lower than user2_id
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user1_status = db.Column(db.Enum(channelStatusEnum), default=channelStatusEnum.READ)
    user2_status = db.Column(db.Enum(channelStatusEnum), default=channelStatusEnum.READ)

    user_1 = db.relationship("User", backref=backref("usr_1", uselist=False), foreign_keys=[user1_id])
    user_2 = db.relationship("User", backref=backref("usr_2", uselist=False), foreign_keys=[user2_id])

    def __repr__(self):
        return f"ChatChannel('{self.user1_id}', '{self.user2_id}', '{self.user_1.username}', '{self.user_2.username}', '{self.last_updated}')"


class ChatMessages(db.Model):
    __tablename__ = "chatmessages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_content = db.Column(db.Text, nullable=False)
    message_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message_status = db.Column(db.Enum(messageStatusEnum), default=messageStatusEnum.SENT)

    channel_id = db.Column(db.Integer, db.ForeignKey('chatchannel.id', ondelete='CASCADE'), nullable=False)
    sender = db.relationship("User", backref=backref("usr_snd", uselist=False), foreign_keys=[sender_id])

    def __repr__(self):
        return f"ChatMessages('{self.sender}', '{self.message_content}', '{self.message_sent}', '{self.message_time}, {self.channel_id}')"

# ----------------------------------------------------Notifications-----------------------------------------------------------

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipient = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notifier = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    notification_message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=0)
    type = db.Column(db.Enum(notificationTypeEnum), nullable=False)

def __repr__(self):
        return f"Notification('{self.notification_message}', '{self.user_id}', '{self.post_id}')"
