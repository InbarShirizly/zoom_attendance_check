from flask import render_template, redirect, url_for, request, flash
from Server import app, bcrypt, db
from Server.forms import LoginForm, RegistrationForm, CreateClassForm
from Server.models import User, Classroom
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os


def save_file(form_file): #TODO: create better algorithem to save the files
    _, f_ext = os.path.splitext(form_file.filename) 
    file_name = secrets.token_hex(8) + f_ext
    file_path = os.path.join(app.root_path, 'static', 'students', file_name)
    form_file.save(file_path)
    return file_name


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CreateClassForm()
    if form.validate_on_submit():
        file_name = save_file(form.students_file.data)
        new_class = Classroom(name=form.name.data, csv_students_file=file_name, teacher=current_user)
        db.session.add(new_class)
        db.session.commit()
    return render_template('home.html', form=form)


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
            flash(f'Invalid credentials', 'danger')

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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))