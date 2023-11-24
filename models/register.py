# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from models import db_storage
from models.user import User
from models.admin import Admin
from models.customer import Customer

class AddUser(FlaskForm):
    """This class handles registration"""""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    classes = [User, Customer, Admin]
    
    def validate_username(self, username):
        for cls in self.classes:
            users = db_storage.all(cls)
            for user in users.values():
                if username.data == user.username:
                    raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        for cls in self.classes:
            users = db_storage.all(cls)
            for user in users.values():
                if user.email == email.data:
                    raise ValidationError('Please use a different email.')
