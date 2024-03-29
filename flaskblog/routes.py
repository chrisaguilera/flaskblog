import os
import secrets
import json
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    posts = []
    for post_object in Post.objects: 
        posts.append(post_object)
    posts.reverse()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        user.save()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn = save_profile_picture(form.picture.data)
            current_user.update(image_file=picture_fn)
        current_user.update(username=form.username.data, email=form.email.data)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        user = User.objects(username=current_user.username).first()
        post = Post(title=form.title.data, content=form.content.data, author=user)
        post.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post", form=form, legend="Create New Post")

@app.route("/post/<post_id>")
def post(post_id):
    post = Post.objects(id=post_id).first()
    if not post:
        abort(404)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.objects(id=post_id).first()
    if not post:
        abort(404)
    user = User.objects(id=current_user.id).first()
    if post.author != user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.update(title=form.title.data, content=form.content.data)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data  = post.title
        form.content.data = post.content
        return render_template('create_post.html', title="Update Post", form=form, legend="Update Post")

@app.route("/post/<post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.objects(id=post_id).first()
    if not post:
        abort(404)
    user = User.objects(id=current_user.id).first()
    if post.author != user:
        abort(403)
    post.delete()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
