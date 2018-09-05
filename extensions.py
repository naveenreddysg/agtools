"""The flask_sqlalchemy module does not have to be initialized with the app right away """

__author__ = 'hughson.simon@gmail.com'

from flask_login import LoginManager

login_manager = LoginManager()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
