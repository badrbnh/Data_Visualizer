# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from models import db_storage
from models.user import User

class AddUser(FlaskForm):
    """This class handles registration"""""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    
    def validate_username(self, username):
        users = db_storage.all(User)
        for user in users.values():
            if username.data == user.username:
                raise ValidationError('Please use a different username.')
    
    
    def validate_email(self, email):
        users = db_storage.all(User)
        for user in users.values():
            if user.email == email.data:
                raise ValidationError('Please use a different email.')
        
