from flask import render_template, redirect, url_for, flash, Blueprint
from Server import bcrypt, db
from Server.users.forms import LoginForm, RegistrationForm
from Server.models import User
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('classrooms.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.auth.data).first() or \
         User.query.filter_by(username=form.auth.data).first() # User can be validated with both username and email
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('classrooms.home'))
        else: # Unique validation that has to be checked here
            flash(f'Invalid credentials', 'danger')

    return render_template('login.html', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('classrooms.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash((form.password.data)).decode('utf-8') 
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))