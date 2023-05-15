from flask_wtf import FlaskForm # FlaskForm is a class that inherits from Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField # StringField is a class that represents an <input type="text"> HTML element
from wtforms.validators import DataRequired, Length, Email, EqualTo ,ValidationError# DataRequired is a class that represents a validator that checks that the field is not submitted empty
from app.models import User
# class registration form
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # DataRequired() is a validator that checks that the field is not submitted empty
    # Length() is a validator that checks that the field is within a certain length
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Email() is a validator that checks that the field is a valid email address
    password = PasswordField('Password', validators=[DataRequired()])
    # PasswordField() is a field that stores a password as a hash instead of the actual string
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # EqualTo() is a validator that checks that the field is equal to another field

    submit = SubmitField('Sign Up')
    # SubmitField() is a button that submits the form
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# class login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Email() is a validator that checks that the field is a valid email address
    password = PasswordField('Password', validators=[DataRequired()])
    # PasswordField() is a field that stores a password as a hash instead of the actual string
    remember = BooleanField('Remember Me')
    # BooleanField() is a checkbox
    submit = SubmitField('Login')
    # SubmitField() is a button that submits the form