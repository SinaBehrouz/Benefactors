from notepad import app, db
from flask import Flask, request, jsonify
# from flask_restful import abort

from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime

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
        return f"User('{self.email}'| '{self.first_name}'| '{self.last_name}')"

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    #sample DateTime value: 2020-06-28 20:40:55.952515
    date_deadline: db.Column(db.DateTime, nullable = False)
    status= db.Column( db.Enum(statusEnum), nullable = False)
    author_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable = False)
    def __repr__(self):
        return f"Post('{self.title}'| '{self.date_posted}' )"


# to do:
# figure out if we want to authenticate/authorize on each endpoint
# organize project into multiple files
# add error handling/validation once db has been added
# add password reset API
# all non-admins are now called consumers

@app.route("/login", methods=['POST'])
def login():
    login_info = request.get_json()
    # will change drastically when we implement login properly, this is just a dummy implementation
    # return success/failure accordingly
    return {"Message": "Successfully logged in as " + login_info['email']}, 200

def signup():
    sign_up_info = request.get_json()
    # will change drastically when we implement login properly, this is just a dummy implementation
    return {"Message": "Successfully signed up as " + sign_up_info['email']}, 201

# Get all posts
@app.route("/posts", methods=['GET'])
def get_all_posts():
    # dummy data for now, replace with db call
        x = User.query.get('a@a.com');
        print(x)
        return ("done")
        client_post_1_info = {
            'post_id': "128976",
            'title': "Dummy Title 1",
            'description': "Dummy Description 1",
            'author_email': "Dummy_email1@gmail.com",
            'date_posted': "10/06/2020",
            'date_deadline': "10/07/2020",
            'status': 'OPEN'
        }
        client_post_2_info = {
            'post_id': "987654",
            'title': "Dummy Title 2",
            'description': "Dummy Description 2",
            'author_email': "Dummy_email2@gmail.com",
            'date_posted': "10/06/2020",
            'date_deadline': "10/07/2020",
            'status': 'IN_PROGRESS'
        }
        client_post_3_info = {
            'post_id': "876543",
            'title': "Dummy Title 3",
            'description': "Dummy Description 3",
            'author_email': "Dummy_email3@gmail.com",
            'date_posted': "10/06/2020",
            'date_deadline': "25/06/2020",
            'status': 'CLOSED'
        }
        return jsonify(client_post_1_info, client_post_2_info, client_post_3_info), 200

# Create new post
@app.route("/post/new", methods=['POST'])
def create_new_post():
    post_info = request.get_json()
    # add db call in here to post information to the db
    return {'Post saved! ': post_info}, 201


# Get/Edit/Delete a single post
@app.route("/posts/<int:post_id>", methods=['GET', 'PUT', 'DELETE'])
def single_post(post_id):
    if request.method == 'GET':
        # replace with db call to get post info from db
        post_info = {
            'post_id': post_id,
            'title': "Dummy Title",
            'description': "Dummy Description",
            'author_email': "Dummy_email@gmail.com",
            'date_posted': "10/06/2020",
            'date_deadline': "10/07/2020",
            'status': 'OPEN'
        }
        return {"Post retrieved ": post_info }, 200
    elif request.method == 'PUT':
        updated_post_info = request.get_json()
        # add db call in here to update information in the db
        return {'Post updated ': updated_post_info}, 200
    elif request.method == 'DELETE':
        post_to_delete = request.get_json()
        # add db call to delete post from db
        return {"Message": 'post with id ' + str(post_id) + ' has been deleted'}, 200
