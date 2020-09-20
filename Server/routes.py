from flask import render_template
from Server import app
from Server.forms import LoginForm, RegistrationForm


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
        print('registered')
    return render_template('register.html', form=form)
