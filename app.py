from flask import Flask, render_template, url_for

app = Flask(__name__)

recipes = [
    {
        'author': 'Beata Rudzka',
        'title': 'Recipe_1',
        'content': 'First recipe content',
        'date_posted': 'April 21, 2019'
    },
    {
        'author': 'Beata Rudzka',
        'title': 'Recipe_2',
        'content': 'Second recipe content',
        'date_posted': 'April 23, 2019'
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', recipes=recipes)


@app.route('/add')
def add():
    return render_template('addRecipe.html')


if __name__ == '__main__':
    app.run(debug=True)
