from flask import render_template, redirect, url_for
from Server import app, bcrypt, db
from Server.forms import LoginForm, RegistrationForm
from Server.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('logged')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
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
def logout():
    pass