import os
import uuid
import stripe
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from benefactors import app, db, bcrypt, mail, stripe_keys
from benefactors.models import User, Post, PostComment, statusEnum, categoryEnum, ChatChannel, ChatMessages, UserReview
from benefactors.forms import LoginForm, SignUpForm, AccountUpdateForm, DonationForm, PostForm, RequestResetForm, \
    ResetPasswordForm, SearchForm, PostCommentForm, SendMessageForm, ReviewForm
from flask_mail import Message
from sqlalchemy import or_, desc, asc
from datetime import datetime
from .postalCodeManager import postalCodeManager
from .search import SearchUtil


# -------------------------------------------Login/Logout-------------------------------------------
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


# ----------------------------------------------SignUp----------------------------------------------

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, phone_number=form.phone_number.data,
                    postal_code=form.postal_code.data.upper(),
                    password=hash)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Account created!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Register', form=form)


# -----------------------------------------------Forgot Pass------------------------------------------

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f''' To Reset your password visit the following link:
    {url_for('reset_token', token=token, _external=True)}
If you did not make this request, simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with instruction has been sent to your email', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


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
    return render_template('reset_token.html', title='Reset Password', form=form)


# -----------------------------------------------Home-------------------------------------------------

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm(status=0, tag='allCat', radius=50)
    choices = [("allCat", "All Categories")]
    for c in categoryEnum:
        choices.append((c.name, c.name))
    form.category.choices = choices
    if form.validate_on_submit():
        posts = []
        searchString = form.searchString.data
        if len(searchString) > 0:
            searchString = "%{}%".format(searchString)  # Post.author.username.like(searchString)
            posts = db.session.query(Post).join(User, User.id == Post.user_id).filter(
                or_(Post.title.ilike(searchString),
                    Post.description.ilike(searchString),
                    User.username.ilike(searchString)))
        else:
            posts = db.session.query(Post).join(User, User.id == Post.user_id)
        # filter based on staus
        if (form.status.data != 'all'):
            posts = posts.filter(Post.status == statusEnum._member_map_[form.status.data])
        # filter based on category
        if (form.category.data != 'allCat'):
            posts = posts.filter(Post.category == categoryEnum._member_map_[form.category.data])
        # filter based on close by posts

        if form.postalCode.data:
            pcm = postalCodeManager()
            searchUtil = SearchUtil()
            searchRes = searchUtil.get_adv_pc_from_location(form)
            if len(searchRes[1]) > 0:
                flash(searchRes[1], 'warning')
                if searchRes[0] < 0:
                    return render_template('home.html', posts=[], form=form)
            pc = searchRes[0]
            pcm.getNearybyPassCodes(pc, form.radius.data)
            nearby_postal_codes = pcm.getNearybyPassCodes(pc, form.radius.data)
            try:
                posts = posts.filter(or_(*[User.postal_code.ilike(x) for x in nearby_postal_codes]))
            except:
                flash("WTF HAPPE$NED")
                pc = pcm.getPCfromCity(parsed_location[-3])  # rare case - a random bug w sqlalchemy

        flash("Search Updated!", "success")
        posts = posts.order_by(desc(Post.date_posted)).all()
        return render_template('home.html', posts=posts, form=form)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
        return render_template('home.html', posts=posts, form=form)


# -----------------------------------------------Posts----------------------------------------------

# Create new post
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_new_post():
    form = PostForm()
    choices = []
    for c in categoryEnum:
        choices.append((c.name, c.name))
    form.category.choices = choices
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data,
                    author=current_user, category=categoryEnum._member_map_[form.category.data])
        db.session.add(post)
        db.session.commit()
        flash('Post created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# Get specific post
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = db.session.query(PostComment).filter_by(post_id=post_id)
    form = PostCommentForm()
    searchUtil = SearchUtil()
    nearby_locations = searchUtil.get_nearby_locations(post)
    return render_template('post.html', post=post, comments=comments, form=form, a=nearby_locations)


# Update title/content of a specific post.
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    choices = []
    for c in categoryEnum:
        choices.append((c.name, c.name))
    form.category.choices = choices
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


# Update post status to open
@app.route("/post/<int:post_id>/status/open", methods=['GET', 'POST'])
@login_required
def open_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    post.status = statusEnum.OPEN
    db.session.commit()
    flash('Your post is now open!', 'success')
    return redirect(url_for('post', post_id=post.id))


# Update post status to close
@app.route("/post/<int:post_id>/status/close", methods=['GET', 'POST'])
@login_required
def close_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    post.status = statusEnum.CLOSED
    db.session.commit()
    flash('Your post is closed!', 'success')
    return redirect(url_for('post', post_id=post.id))


# Assign volunteer
@app.route("/post/<int:post_id>/volunteer", methods=['GET', 'POST'])
@login_required
def volunteer(post_id):
    post = Post.query.get_or_404(post_id)
    # This check is precautionary, we are already checking user in post.html.
    if post.author == current_user:
        flash("You can't volunteer for your own post!", 'warning')
    elif post.status != statusEnum.OPEN:
        flash('Post must be open to volunteer!', 'warning')
    else:
        post.volunteer = current_user.id
        post.status = statusEnum.TAKEN
        db.session.commit()
        flash('You are now volunteering for the post!', 'success')
    return redirect(url_for('post', post_id=post.id))


# Remove volunteer
@app.route("/post/<int:post_id>/unvolunteer", methods=['GET', 'POST'])
@login_required
def unvolunteer(post_id):
    post = Post.query.get_or_404(post_id)
    # This check is precautionary, we are already checking user in post.html.
    if post.volunteer != current_user.id:
        flash('You never volunteered for this post!', 'danger')
    else:
        post.volunteer = 0
        post.status = statusEnum.OPEN
        db.session.commit()
        flash('You are no longer volunteering for the post!', 'success')

    return redirect(url_for('post', post_id=post.id))


# Delete post
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


# -----------------------------------------------Comments----------------------------------------------

# Create a new comment on a post
@app.route("/post/<int:post_id>/comments/new", methods=['GET', 'POST'])
@login_required
def create_new_comment(post_id):
    post = Post.query.get_or_404(post_id)
    comments = db.session.query(PostComment).filter_by(post_id=post_id)
    form = PostCommentForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            created_comment = PostComment(comment_desc=form.comment_desc.data, cmt_author=current_user, post_id=post_id)
            db.session.add(created_comment)
            db.session.commit()
            flash('Comment added!', 'success')
            return redirect(url_for('post', post_id=post.id))

    return render_template('post.html', post=post, comments=comments, form=form)


# Update comment
# NOTE: Backend logic is complete but front end needs work in post.html.
# Feel free to make changes in update_comment if you are working in frontend.
@app.route("/post/<int:post_id>/comments/<int:comment_id>/update", methods=['GET', 'POST'])
@login_required
def update_comment(post_id, comment_id):
    form = PostCommentForm()
    post = Post.query.get_or_404(post_id)
    comment = PostComment.query.get_or_404(comment_id)

    if comment.cmt_author != current_user:
        abort(403)
    if form.validate_on_submit():
        comment.comment_desc = form.comment_desc.data
        db.session.commit()
        flash('Comment updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    if request.method == 'GET':
        form.comment_desc.data = comment.comment_desc
    return render_template('post.html', title=post.title, post=post, comments=comment, form=form)


# Delete comment
@app.route("/post/<int:post_id>/comments/<int:comment_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_comment(post_id, comment_id):
    comment = PostComment.query.get_or_404(comment_id)
    if comment.cmt_author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', 'success')
    return redirect(url_for('post', post_id=post_id))


# --------------------------------------Account----------------------------------------

def save_image(picture):
    picture_name = uuid.uuid4().hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static', 'user_images', picture_name)
    print(picture_path)
    reduced_size = (125, 125)
    user_image = Image.open(picture)
    user_image.thumbnail(reduced_size)
    user_image.save(picture_path)
    return picture_name


@app.route("/account/edit", methods=['GET', 'POST'])
@login_required
def edit_account():
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
        current_user.postal_code = form.postal_code.data.upper()
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('edit_account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.postal_code.data = current_user.postal_code
    user_image = url_for('static', filename='user_images/' + current_user.user_image)
    return render_template('edit_account.html', title='Edit Account', user_image=user_image, form=form)


@app.route("/account", methods=['GET'])
@login_required
def get_account():
    user = User.query.filter_by(email=current_user.email).first()
    to_do = Post.query.filter_by(volunteer=current_user.id)
    # to-do make sure only account owner can access this
    return render_template('account.html', user=user, to_do=to_do)


# -----------------------------------Other Account----------------------------------------


def get_avg_rating(reviews):
    ratings = [review.score for review in reviews]
    if ratings:
        average = sum(ratings) / len(ratings)
        return average
    return "No reviews available"


@app.route("/account/<int:user_id>", methods=['GET', 'POST'])
@login_required
def other_account(user_id):
    account = User.query.get_or_404(user_id)
    if account == current_user:
        return redirect(url_for('get_account'))

    form = ReviewForm()
    reviews = db.session.query(UserReview).filter_by(profile=user_id)
    avg_rating = get_avg_rating(reviews)
    return render_template('other_account.html', account=account, reviews=reviews, avg_rating=avg_rating, form=form)


# -----------------------------------------------Reviews----------------------------------------------


@app.route("/account/<int:user_id>/reviews/new", methods=['POST'])
@login_required
def add_review(user_id):
    form = ReviewForm()
    if request.method == 'POST':
        if user_id == current_user.id:
            flash('You cannot review yourself!', 'danger')
            return redirect(url_for('other_account', user_id=user_id))

        if form.validate_on_submit():
            review = UserReview(description=form.description.data, score=form.score.data,
                                profile=user_id, author=current_user.id)
            db.session.add(review)
            db.session.commit()
            flash('Review added!', 'success')

    return redirect(url_for('other_account', user_id=user_id))


@app.route("/account/<int:user_id>/reviews/<int:review_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_review(user_id, review_id):
    review = UserReview.query.get_or_404(review_id)
    if review.rev_author != current_user:
        abort(403)
    db.session.delete(review)
    db.session.commit()
    flash('Your review has been deleted!', 'success')
    return redirect(url_for('other_account', user_id=user_id))


# ---------------------------------------About-----------------------------------------

@app.route("/about")
def about():
    form = DonationForm()
    return render_template('about.html', form=form, key=stripe_keys['publishable_key'])


@app.route('/charge', methods=['POST'])
def charge():
    try:
        form = DonationForm()
        amount = form.amount.data
        # convert amount into cents
        amount *= 100

        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken']
        )

        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Donation'
        )
        flash('Thank you for your donation!', 'success')
        return redirect(url_for('about'))
    except:
        flash('Something went wrong!', 'danger')
        return redirect(url_for('about'))


# -------------------------------------Messages-----------------------------------------

@app.route("/messages", methods=['GET', 'POST'])
@login_required
def messages():
    channels = getAllChannelsForUser(current_user)
    return render_template('messages.html', owner=current_user, chatchannels=channels)


@app.route("/messages/<int:channel_id>", methods=['GET', 'POST'])
@login_required
def messages_chat(channel_id):
    channels = getAllChannelsForUser(current_user)
    messages = getConversationForChannel(channel_id)
    form = SendMessageForm()
    current_channel = ChatChannel.query.get_or_404(channel_id)

    # it might need the other user id and current user id
    # we will need to create a new channel here, depending on which user we choose to chat
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the time
            curr_time = datetime.utcnow()

            # Parse the form
            chatmessage = ChatMessages(sender_id=current_user.id, message_content=form.chat_message_desc.data,
                                       channel_id=channel_id)
            db.session.add(chatmessage)

            # Update the channel last_updated field because of new comments are made
            current_channel.last_updated = curr_time
            # DB update is caused by channel last_update
            db.session.commit()

            messages = getConversationForChannel(channel_id)

            return redirect(url_for('messages_chat', channel_id=channel_id))

    # In case the user submits an empty message or the request.method is GET
    return render_template('messages.html', owner=current_user, chatchannels=channels, form=form, messages=messages,
                           channel_id=channel_id)


@app.route("/messages/create/<int:cmt_auth_id>", methods=['GET'])
@login_required
def create_new_chat_channel(cmt_auth_id):
    if request.method == 'GET':
        # Check whether channel already exists
        channel_id = findSpecificChannel(current_user.id, cmt_auth_id)

        # If already exists retrieve messages
        if channel_id != -1:
            return redirect(url_for('messages_chat', channel_id=channel_id))
        # If not, create a new channel
        else:
            user1 = -1
            user2 = -1

            if current_user.id < cmt_auth_id:
                user1 = current_user.id
                user2 = cmt_auth_id
            else:
                user1 = cmt_auth_id
                user2 = current_user.id

            newChannel = ChatChannel(user1_id=user1, user2_id=user2)
            db.session.add(newChannel)
            # DB update is caused by creating a new channel
            db.session.commit()

            return redirect(url_for('messages_chat', channel_id=newChannel.id))


# ----------------------------------Messages Helper-------------------------------------

# Find whether the channel already exists
def findSpecificChannel(user1_id, user2_id):
    # initialize channel
    channel = ChatChannel.query.filter_by(user1_id=user1_id, user2_id=user2_id).first()

    if user1_id > user2_id:
        channel = ChatChannel.query.filter_by(user1_id=user2_id, user2_id=user1_id).first()

    if channel == None:
        return -1

    return channel.id


# Get the channel from the current_user
def getAllChannelsForUser(user):
    channels = []

    # Initialize two channels
    channels_1 = ChatChannel.query.filter_by(user1_id=current_user.id).order_by(ChatChannel.last_updated.desc()).all()
    channels_2 = ChatChannel.query.filter_by(user2_id=current_user.id).order_by(ChatChannel.last_updated.desc()).all()

    # Get the size of the channels
    size_1 = len(channels_1)
    size_2 = len(channels_2)

    i = 0
    j = 0
    # Sort the channel based on the most recent, loop through two channels and merge them
    while i < size_1 and j < size_2:
        if channels_1[i].last_updated > channels_2[j].last_updated:
            channels.append(channels_1[i])
            i += 1
        else:
            channels.append(channels_2[j])
            j += 1

    channels = channels + channels_1[i:] + channels_2[j:]
    return channels


def getConversationForChannel(id):
    conversations = ChatMessages.query.filter_by(channel_id=id).order_by(ChatMessages.message_time.asc()).all()
    return conversations
