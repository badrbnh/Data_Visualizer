# app/routes.py
from flask import render_template, redirect, url_for, flash
from models.register import AddUser
from models import db_storage
from models.user import User
from web_flask import app

app.config['SECRET_KEY'] = 'you-will-never-guess'

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
        return redirect(url_for('register'))

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)