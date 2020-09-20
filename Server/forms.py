from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email

# NOTE: add validations acoording to db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # Add special signs validations
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    auth = StringField('Auth', validators=[DataRequired()]) # Auth can be username or email
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')