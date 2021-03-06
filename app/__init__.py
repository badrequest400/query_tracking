from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from config import basedir
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models