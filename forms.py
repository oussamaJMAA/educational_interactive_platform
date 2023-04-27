from flask_wtf import FlaskForm # FlaskForm is a class that inherits from Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField # StringField is a class that represents an <input type="text"> HTML element
from wtforms.validators import DataRequired, Length, Email, EqualTo # DataRequired is a class that represents a validator that checks that the field is not submitted empty

# class registration form
class RegistrationForm(FlaskForm):
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