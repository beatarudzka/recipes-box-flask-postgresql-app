from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed 
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj się')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() 
        if user:
            raise ValidationError('Nazwa użytkownika jest zajęta. Wybierz inną nazwę użytkownika')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('Ten email jest zajęty przez innego użytkownika. Wpisz inny email')
            
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Zmień zdjęcie profilowe', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Zmień dane profilowe')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() 
            if user:
                raise ValidationError('Nazwa użytkownika jest zajęta. Wybierz inną nazwę użytkownika')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() 
            if user:
                raise ValidationError('Ten email jest zajęty przez innego użytkownika. Wpisz inny email')

class RecipeForm(FlaskForm):
    title = StringField('Tytuł',
                           validators=[DataRequired()])
    content = TextAreaField('Opis', validators=[DataRequired()])
    ingredients = TextAreaField('Składniki', validators=[DataRequired()])
    picture = FileField('Dodaj zdjęcie')  
    tag = StringField('Znaczniki(tagi)', validators=[DataRequired()])
    submit = SubmitField('Dodaj przepis')  
             