# Step by step for Python Flask App from Scratch

Boilerplate how to get started using the Flask framework. 
- [x] create new virtual env and install the necessary packages and get a basic Hello World Application running in our browser. 
- [x] create register and login form using wtforms
- [x] adding styling(used sass pre-processor - libsass)
- [x] database with Flask-SQLAlchemy
- [x] user authentication
- [ ] creating user account with uploading the picture
- [ ] adding pagination
- [ ] creating custom error pages
- [ ] deployment

## 1. Creating virtual environment for new project.

Virtual Environments in Python allow us to keep project-specific dependencies in a separate place than our global site-packages. This is extremely useful when you have different versions of packages for different projects.


##### Folder to keep all environments on my computer:

```
/Environments
```

##### 1.1 To create new env: 

```
virtualenv {nameOfProject}
```

In case, when you want create new, virtual env with specific version of Python:

```
virtualenv -p /usr/bin/python2.6 {nameOfProject}
```

##### 1.2. Activate Python env:

```
source {nameOfNewProject}/bin/activate
```

##### 1.3. Install new packages into local env:


```
pip install {nameOfPackage}

pip install flask
```

If you want to go back to being in the global env:

```
deactivate
```
Prompt with name of project no longer shows up.


If you want delete virtual env:

```
rm -rf {nameOfProject}
```

To enlist all packages:


```
pip list
```

You can also use your global site packages within virtual Python environment.

Freezing is a process where pip reads the versions of all installed packages in a local virtual environment and then produces a text file with the package version for each python package specified. By convention, it's named requirements. txt .

```
pip freeze --local >environment.txt
```

To make sure you got all packages:

```
cat environment.txt
```

You get list of all packages with versions.


In case, you want install those packages from environment.txt in next project:

```
pip install -r requirements.txt
```



## 2. Creating app.py 

Create new folder for your application and file app.py, starting with example from the documentation:

```
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

```

##### 2.1. Join virtual environment with Python app's file:

Before running application you need to set an environment variable to the file, that you want to be flask application.

In line command of your virtual Python environment go to your project's folder and type in:

```
export FLASK_APP=app.py

```



On the port 5000 it will show Hello world.




## 3.Forms and User Input.

```
pip install flask-wtf

```

Create files: register.html and login.html.
Build new forms according to documentation using packages below:

- wtforms,
- flash,
- url_for,
- redirect


## 3.Styling with pre-processors SASS.

In the virtual env install new packages:

```
pip install rcssmin rjsmin sass
```
Using these 3 packages:
    - Compiles scss to css
    - Minifies css
    - Minifies JavaScript

In new script runner.py:

```

sass_map = {"app/static/scss/style.scss": "app/static/css/style.css"}


css_map = {"app/static/css/style.css": "app/static/css/style.min.css"}


js_map = {"app/static/js/app.js": "app/static/js/app.min.js"}


def compile_sass_to_css(sass_map):

    print("Compiling scss to css:")

    for source, dest in sass_map.items():
        with open(dest, "w") as outfile:
            outfile.write(sass.compile(filename=source))
        print(f"{source} compiled to {dest}")


def minify_css(css_map):

    print("Minifying css files:")

    for source, dest in css_map.items():
        with open(source, "r") as infile:
            with open(dest, "w") as outfile:
                outfile.write(rcssmin.cssmin(infile.read()))
        print(f"{source} minified to {dest}")


def minify_javascript(js_map):

    print("Minifying JavaScript files:")

    for source, dest in js_map.items():
        with open(source, "r") as infile:
            with open(dest, "w") as outfile:
                outfile.write(rjsmin.jsmin(infile.read()))
        print(f"{source} minified to {dest}")

```

Add to app.py:

```
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.min.css') }}">
```

## 4. Creating database with flask-SQLAlchemy.


install new package in virtual env:

``` 
pip install flask-sqlalchemy
```
and import into application. After that, choose location of database and create database instance:

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
```

After creating tables, import database from application file:

```
$ python

>>> from app import db
>>> db.create_all()
>>> from app import User, Recipe
```

After that, create user and add into a database:

```
>>> user_1 = User(username='user', email='user@gmail.com', password='password')
>>> db.session.add(user_1)

```

![Structure](images/structure.png)


## 4. User Authentication.

```
pip install flask-bcrypt

```

Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for application.
To use the extension simply import the class wrapper and pass the Flask app object.

What is hashing function? It takes plain text and turns into a string of text that always has the same length. And it works only one way.

Bcrypt takes a password as input along with a salt and a cost. Salt is a fixed-length cryptographically-strong random value that is added to the input of hash functions to create unique hashes for every input. A salt is added to make a password hash output unique even for users adopting common passwords. 


## 4. Adding recipes into development database (sqlite).

```
@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, content=form.content.data, ingredients=form.ingredients.data, image_file_recipe=form.picture.data, tag=form.tag.data, author=current_user)
        db.session.add(recipe)
        db.session.commit()
        flash('Twój przepis został dodany!', 'success')
        return redirect(url_for('home'))
    return render_template('new_recipe.html', title='New Title', form=form)
```

 validate_on_submit will check if it is a POST request and if it is valid.

 On the home route add variable recipes, which gather all those recipes from the database:

 ```
 def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)
```

#### 4.1. Adding images into database.

After adding images using input (type="file", name="image"), you can print out in console name of the file:

![Structure](images/filestorage.png)


FileStorage is special flask object over incoming files. It is used by the request object to represent uploaded files. 
Using app.config specify full path, where files will be saved:

```
app.config["IMAGE_UPLOADS"] = "/home/beatronoks/Dokumenty/Workspace/boilerplate-flask-app/app/static/images/recipes"

image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

```