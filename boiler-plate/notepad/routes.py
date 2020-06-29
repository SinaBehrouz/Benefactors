from notepad import app, db
from flask import Flask, request, jsonify, render_template
from notepad.models import User, Post
# from flask_restful import abort

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
        query = Post.query.all();
        # for p in query:
        #     print(p)
        return render_template("posts.html", posts=query),200
        # client_post_1_info = {
        #     'post_id': "128976",
        #     'title': "Dummy Title 1",
        #     'description': "Dummy Description 1",
        #     'author_email': "Dummy_email1@gmail.com",
        #     'date_posted': "10/06/2020",
        #     'date_deadline': "10/07/2020",
        #     'status': 'OPEN'
        # }
        # client_post_2_info = {
        #     'post_id': "987654",
        #     'title': "Dummy Title 2",
        #     'description': "Dummy Description 2",
        #     'author_email': "Dummy_email2@gmail.com",
        #     'date_posted': "10/06/2020",
        #     'date_deadline': "10/07/2020",
        #     'status': 'IN_PROGRESS'
        # }
        # client_post_3_info = {
        #     'post_id': "876543",
        #     'title': "Dummy Title 3",
        #     'description': "Dummy Description 3",
        #     'author_email': "Dummy_email3@gmail.com",
        #     'date_posted': "10/06/2020",
        #     'date_deadline': "25/06/2020",
        #     'status': 'CLOSED'
        # }
        #return jsonify(client_post_1_info, client_post_2_info, client_post_3_info), 200

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
        query = Post.query.get(post_id)
        post_info = {
            'post_id': query.post_id,
            'title': query.title,
            'description': query.description,
            'author_email': query.author_email,
            'date_posted': query.date_posted,
            'date_deadline': query.date_deadline,
            'status': query.status.name
        }
        return {"Post retrieved ": post_info }, 200
    elif request.method == 'PUT':
        updated_post_info = request.get_json()
        # add db call in here to update information in the db
        query = Post.query.get(post_id)
        for key,value in updated_post_info.items():
            query[key] = updated_post_info[key]

        # for e in updated_post_info:
        #     query[e] = updated_post_info[e]
        return {'Post updated ': updated_post_info}, 200
    elif request.method == 'DELETE':
        post_to_delete = request.get_json()
        # add db call to delete post from db
        try:
            Post.query.filter_by(post_id = post_id).delete()
            db.session.commit()
        except:

        #@todo: are we actually deleting the post or changing the status to closed or deleted?
        return {"Message": 'post with id ' + str(post_id) + ' has been deleted'}, 200
