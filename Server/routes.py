from flask import render_template, redirect, url_for, request
from Server import app, bcrypt, db
from Server.forms import LoginForm, RegistrationForm
from Server.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/home')
# @login_required
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.auth.data).first() or \
         User.query.filter_by(username=form.auth.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            print('failed login') # for now

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))