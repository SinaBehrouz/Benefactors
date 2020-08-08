from flask_login import login_user, current_user, logout_user, login_required
from benefactors import app, db, bcrypt, mail, stripe_keys
from benefactors.models import User, Post, PostComment, statusEnum, notificationTypeEnum, Notification
from sqlalchemy import or_, desc, asc
import json
from sqlalchemy.exc import IntegrityError
import datetime



# change from commenter user id to something else 
def notify_commenters(post_id, notifier_user_id,notification_message, type):
    unique_comments = db.session.query(PostComment).filter_by(post_id=post_id).distinct(PostComment.user_id)
    post = Post.query.get_or_404(post_id)
    for comment in unique_comments:  
        print("made it here", flush=True)
        if comment.user_id != notifier_user_id and comment.user_id != post.user_id : # don't want to notify the person who made the comment, or the author cus they get notification later
            print("hello")
            print("printing unique id that we will create ication for", flush=True)
            print(comment.user_id, flush=True)
            recipient = comment.user_id 

            # should be unique 'recipient', 'notifier', 'post_id', 'is_read', 'type'
            duplicate = Notification.query.filter_by(recipient=recipient, notifier=notifier_user_id, post_id=post_id, type=type).first()
            if duplicate: 
                print("printing duplicate", flush=True)
                print("volunteeered")
                print(duplicate.notification_message, flush=True)
                duplicate.is_read=False
                duplicate.date_created=datetime.datetime.now()
                db.session.commit()
            else: 
                print("should create a notification", flush=True)
                notification = Notification(recipient=recipient, notifier=notifier_user_id, post_id=post_id, notification_message=notification_message, is_read=0, type=type)
                db.session.add(notification)
                db.session.commit()
    
# change from commenter user id to something else 
def notify_volunteer(post_id, notifier_user_id, notification_message, type):
    post = Post.query.get_or_404(post_id)
    if post.volunteer and notifier_user_id != post.volunteer:
        recipient = post.volunteer 
        duplicate = Notification.query.filter_by(recipient=recipient, notifier=notifier_user_id, post_id=post_id, type=type).first()
        if duplicate: 
            print("printing duplicate", flush=True)
            print(duplicate.notification_message, flush=True)
            duplicate.is_read=False
            duplicate.date_created=datetime.datetime.now()
            db.session.commit()  
            
        else: 
            print("should nbe making it here", flush=True)
            recipient = post.volunteer
            notification = Notification(recipient=recipient, notifier=notifier_user_id, post_id=post_id, notification_message=notification_message, is_read=0, type=type)
            db.session.add(notification)
            db.session.commit()

# change from commenter user id to something else 
def notify_post_owner(post_id, notifier_user_id, notification_message, type):
    post = Post.query.get_or_404(post_id)
    if notifier_user_id != post.user_id:
        recipient = post.user_id
        duplicate = Notification.query.filter_by(recipient=recipient, notifier=notifier_user_id, post_id=post_id, type=type).first()
        if duplicate: 
            print("printing duplicate", flush=True)
            print(duplicate.notification_message, flush=True)
            duplicate.is_read=False
            duplicate.date_created=datetime.datetime.now()
            db.session.commit()  
        else: 
            notification = Notification(recipient=recipient, notifier=notifier_user_id, post_id=post_id, notification_message=notification_message, is_read=0, type=type)
            db.session.add(notification)
            db.session.commit()  