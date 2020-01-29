from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Recipe
from flask_login import login_user

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
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Now, you can log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
