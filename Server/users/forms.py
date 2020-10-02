from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from Server.models import TeacherModel


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = TeacherModel.query.filter_by(username=username.data).first()
        if user:
            print(user)
            raise ValidationError('Username already taken.')
        # Add special signs validations

    def validate_email(self, email):
        user = TeacherModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken.')     


class LoginForm(FlaskForm):
    auth = StringField('Auth', validators=[DataRequired()]) # Auth can be username or email
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
