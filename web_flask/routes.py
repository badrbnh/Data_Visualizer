# app/routes.py
from flask import render_template, abort, jsonify, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from models.register import AddUser
from models.login import LoginForm
from models import db_storage
from models.user import User
from models.profile import ProfileForm
from models.sendMail import sendmail
import requests
import secrets
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
    """Route for registration"""
    form = AddUser()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        verification_token = secrets.token_urlsafe(16)

        new_user = User(username=username, email=email, password=password, verification_token=verification_token)
        db_storage.new(new_user)
        db_storage.save()

        # Send verification email
        url = f"http://localhost:5000/api/v1/verify/{email}/{verification_token}"
        subject = 'Email Verification'
        html_content = f"Welcome to CHATTER-HUB! Click the following link to verify your email: {url}"
        sendmail(subject, html_content, email)

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
                if  user.is_verified == 1:
                    login_user(user, remember=form.remember_me.data)
                    return redirect(url_for('inside', username=user.username))
                else:
                    flash('Email not verified', 'error')
            else:
                flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    """allow user to logout"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/edit', methods=['GET', 'PUT', 'POST'], strict_slashes=False)
def edit():
    """endpoint for editing profile"""
    form = ProfileForm()
    if request.method == 'POST' and form.validate():
        user_id = current_user.id
        url = f"http://localhost:5000/api/v1/users/{user_id}"
        data = {
            "username": form.username.data,
            "email": form.email.data,
        }
        
        response = requests.put(url, json=data)
            
        if response.status_code == 200:
            return redirect(url_for("edit"))
        elif response.status_code == 404:
            abort(404)
        else:
            abort(response.status_code)
    elif request.method == 'POST':
        flash("Email or Username already exists", "error")
    
    return render_template('profile.html', form=form)


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)