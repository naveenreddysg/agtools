__author__ = 'hughson.simon@gmail.com'

from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, SelectField, StringField, TextAreaField  # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

# Define the login form (WTForms)


class LoginForm(Form):
    email = TextField(
        'Email Address', [
            Email(), Required(
                message='Forgot your email address?')])
    password = PasswordField('Password', [
        Required(message='Must provide a password. ;-)')])

# Define the login form (WTForms)


class RegistrationForm(Form):
    email = TextField(
        'Email Address', [
            Email(), Required(
                message='Forgot your email address?')])

class UsersForm(Form):
    choices = [('UserName', 'UserName'),
               ('UserType', 'UserType'),
               ('Subscriptions', 'Subscriptions')]
    select = SelectField('Search for Users:', choices=choices)
    search = StringField('')
