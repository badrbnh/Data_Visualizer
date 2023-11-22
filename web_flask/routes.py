# app/routes.py
from flask import render_template, redirect, url_for, flash, request
from models.register import AddUser
from models.login import LoginForm
from models import db_storage
from sqlalchemy.orm import Session
from models.user import User
from flask_login import current_user, login_user, logout_user
from web_flask import app

app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/home', methods=['GET', 'POST'])
def home():
    username = request.args.get('username')
    return render_template('home.html', username=username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """route for registration"""
    form = AddUser()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User(username=username, email=email, password=password)
        db_storage.new(new_user)
        db_storage.save()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/' , methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already logged in.')
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        users = db_storage.all(User)
        for user in users.values():
            if user.username == form.username.data and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Login successful!', 'success')
                return redirect(url_for('home', username=user.username))

        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)