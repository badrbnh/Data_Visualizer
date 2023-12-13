from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_login import current_user
from models import db_storage
from models.user import User

class ProfileForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Save')
    
    def validate_username(self, username):
        """Method to validate the username"""
        if username.data is not None:
            if len(username.data) < 1:
                username.data = None
        else:
            username.data = current_user.username
        users = db_storage.all(User)
        if username.data is not None:
            for user in users.values():
                if username.data != current_user.username:
                    if username.data == user.username:
                        raise ValidationError('Please use a different username.')
        else:
            username.data = current_user.username

    def validate_email(self, email):
        """Method to validate email"""
        if email.data is not None:
            if len(email.data) < 1:
                email.data = None
        else:
            email.data = current_user.email
        if email.data is not None:
            if email.data is Email()(self, email):
                raise ValidationError('Invalid email format.')
            users = db_storage.all(User)
            for user in users.values():
                if email.data != current_user.email:
                    if user.email == email.data:
                        raise ValidationError('Please use a different email.')
        else:
            email.data = current_user.email
