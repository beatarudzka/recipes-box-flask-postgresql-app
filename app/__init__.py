from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_fontawesome import FontAwesome

app = Flask(__name__)
app.config['SECRET_KEY'] = '88438def1dc83dcc3ca5f07362d4a5df'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["IMAGE_UPLOADS"] = "/home/beatronoks/Dokumenty/Workspace/boilerplate-flask-app/app/static/images/recipes"
app.config["ALLOWED EXTENSIONS"] = ['png', 'jpg', 'jpeg', 'gif']
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


fa = FontAwesome(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from app import routes
