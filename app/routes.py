import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecipeForm
from app.models import User, Recipe
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app.tasks import create_image_set

import redis
from rq import Queue

r = redis.Redis()
q = Queue(connection=r)


@app.route("/")
@app.route("/home")
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Twoje konto zostało stworzone. Teraz możesz się zalogować', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Nie możesz się zalogować. Błędny email lub hasło', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def allowed_image(filename):
    if not "." in filename:
        return False
    extension = filename.rsplit(".", 1)[1]

    if extension.lower() in app.config["ALLOWED EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/recipe/new/upload_image", methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    flash("Przekroczono limit rozmiaru zdjęcia", 'danger')
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == '':
                    flash('Nie wybrano pliku.', 'danger')
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = image.filename
                    image_dir_name = secrets.token_hex(8)
                    os.mkdir(os.path.join(
                        app.config["IMAGE_UPLOADS"], image_dir_name))
                    image.save(os.path.join(
                        app.config["IMAGE_UPLOADS"], image_dir_name, filename))
                    image_dir = os.path.join(
                        app.config["IMAGE_UPLOADS"], filename)

                    flash("Plik zapisany", 'success')

                    return render_template("upload_image.html", image_name=filename)

                else:
                    flash(
                        "Nie dozwolone rozszerzenie pliku. Proszę wybrać inne zdjęcie z rozszerzeniem: .jpg, .jpeg, .gif, .png", 'danger')
                    return redirect(request.url)

    return render_template("upload_image.html")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/images/defaultpicuser', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
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
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='images/defaultpicuser/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data, content=form.content.data,
                        ingredients=form.ingredients.data, image_file_recipe=form.picture.data, author=current_user)
        db.session.add(recipe)
        db.session.commit()
        flash('Twój przepis został dodany!', 'success')
        return redirect(url_for('home'))
    return render_template('new_recipe.html', title='New Title', form=form, legend='Stwórz nowy przepis')


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', title=recipe.title, content=recipe.content, ingredients=recipe.ingredients, recipe=recipe)


@app.route("/recipe/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.content = form.content.data
        recipe.ingredients = form.ingredients.data
        db.session.commit()
        flash('Twój przepis jest zaktualizowany', 'success')
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.content.data = recipe.content
        form.ingredients.data = recipe.ingredients
    return render_template('new_recipe.html', title='Update Recipe', form=form, legend='Edytuj przepis')


@app.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Twój przepis został usuniety!', 'success')
    return redirect(url_for('home'))
