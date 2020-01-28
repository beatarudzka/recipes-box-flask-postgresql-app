from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '88438def1dc83dcc3ca5f07362d4a5df'
recipes = [
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
