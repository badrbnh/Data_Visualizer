# app/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from models.register import AddUser
from models.login import LoginForm
from models import db_storage
from models.user import User
from models.profile import ProfileForm
import os
from web_flask import app

app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/inside', methods=['GET'])
def inside():
    """route for inside of the app"""
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('inside.html')

@app.route('/' , methods=['GET', 'POST'])
@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    """route for home page"""
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """route for registration"""
    form = AddUser()
    if current_user.is_authenticated:
        return redirect(url_for('inside'))
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User(username=username, email=email, password=password)
        db_storage.new(new_user)
        db_storage.save()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """route for user login"""
    if current_user.is_authenticated:
        return redirect(url_for('inside'))

    form = LoginForm()
    if form.validate_on_submit():
        users = db_storage.all(User)
        for user in users.values():
            if user.username == form.username.data and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('inside', username=user.username))
            flash('Invalid username or password', 'error')      
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    """allow user to logout"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/edit', methods=['GET', 'POST'], strict_slashes=False)
def edit():
    """endpoint for editing profile"""
    form = ProfileForm()
    return render_template('profile.html', form=form)


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)