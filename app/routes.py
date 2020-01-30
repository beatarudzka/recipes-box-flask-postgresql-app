import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Recipe
from flask_login import login_user, current_user, logout_user, login_required

recipes=[
    {
        'author': 'Beata Rudzka',
        'title': 'Title1',
        'content': 'Content1',
        'date_posted': 'January 21 2020'
    },
    {
        'author': 'Beata Rudzka',
        'title': 'Title2',
        'content': 'Content2',
        'date_posted': 'January 21 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', recipes=recipes)


@app.route("/add")
def add():
    return render_template('add.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Twoje konto zostało stworze. Możesz się teraz zalogować.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if  next_page else redirect(url_for('home'))
        else:
            flash('Nie możesz się zalogować. Błędny email lub hasło', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/defaultpicuser', picture_fn )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Twoje konto zostało zaktualizowane', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data =current_user.username
        form.email.data =current_user.email
    image_file = url_for('static', filename='images/defaultpicuser/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
