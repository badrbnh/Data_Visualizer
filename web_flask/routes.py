# app/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from models.register import AddUser
from models.login import LoginForm
from models import db_storage
from models.user import User
from models.data import Data
import os
from sqlalchemy.orm import Session
from web_flask import app
from werkzeug.utils import secure_filename
from uuid import uuid4

app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/inside', methods=['GET', 'POST'])
def inside():
    return render_template('inside.html')

@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/' , methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
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
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
    app.config['UPLOAD_FOLDER'] = '/home/chikara/Programming/Projects/Data_Visualizer/data'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # Save the file with a secure filename to the configured UPLOAD_FOLDER
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        user_id = current_user.id
        file.save(file_path)
        data = Data(file_name=filename, user_id=user_id)
        db_storage.new(data)
        db_storage.save()
        return redirect(url_for('inside'))

    return 'Invalid file format'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)