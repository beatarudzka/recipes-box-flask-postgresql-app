
from flask import Flask, render_template
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
