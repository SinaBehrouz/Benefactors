import os
import uuid
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from benefactors import app, db, bcrypt, mail
from benefactors.models import User, Post, statusEnum
from benefactors.forms import (LoginForm, SignUpForm, AccountUpdateForm,
                                PostForm, RequestResetForm, ResetPasswordForm, SearchForm)
from flask_mail import Message
from sqlalchemy import or_
#-------------------------------------------Login/Logout-------------------------------------------

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Incorrect email or password. Please try again!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#----------------------------------------------SignUp----------------------------------------------

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone_number=form.phone_number.data, postal_code=form.postal_code.data, password=hash)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Account created!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Register', form=form)
#-----------------------------------------------Forgot Pass------------------------------------------

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender ='noreply@demo.com',
                    recipients=[user.email])
    msg.body = f''' To Reset your password visit the following link:
    {url_for('reset_token', token=token, _external =True)}
If you did not make this request, simply ignore this email and no changes will be made.
    '''
    mail.send(msg)



@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email with instruction has been sent to your email', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired toekn", 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)

#-----------------------------------------------Home-------------------------------------------------

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        posts = []
        searchString = form.searchString.data
        searchString = "%{}%".format(searchString) #Post.author.username.like(searchString)
        posts = db.session.query(Post).join(User, User.id==Post.user_id).filter( or_( Post.title.ilike(searchString),
                                                     Post.description.ilike(searchString),
                                                     User.username.ilike(searchString))).all()
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts, form=form)

#-----------------------------------------------Posts----------------------------------------------

# Create new post
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        if current_user.is_authenticated:
            post.volunteer = current_user.id
            post.status = statusEnum.taken
            db.session.commit()
            flash('You Are now volunteering for the post!', 'success')
            #it should redirect to a chat screen or message screen
            return redirect(url_for('home'))
        else:
            flash('You must be logged in to volunteer for a post!', 'warning')
            return redirect(url_for('login'))
    else:
        curr_user_volunteering = False
        if post.volunteer == current_user.id:
            curr_user_volunteering = True
        return render_template('post.html', title=post.title, post=post, curr_user_volunteering=curr_user_volunteering)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    if request.method == 'GET':
       form.title.data = post.title
       form.description.data = post.description
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('home'))

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
            print("")

        #@todo: are we actually deleting the post or changing the status to closed or deleted?
        return {"Message": 'post with id ' + str(post_id) + ' has been deleted'}, 200


#--------------------------------------Account----------------------------------------

def save_image(picture):
    picture_name = uuid.uuid4().hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static', 'user_images', picture_name)
    print(picture_path)
    reduced_size = (125, 125)
    user_image = Image.open(picture)
    user_image.thumbnail(reduced_size)
    user_image.save(picture_path)
    return picture_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_image(form.picture.data)
            current_user.user_image = picture_name
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.postal_code = form.postal_code.data
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.postal_code.data = current_user.postal_code
    user_image = url_for('static', filename='user_images/' + current_user.user_image)
    return render_template('profile.html', title='Account', user_image=user_image, form=form)
