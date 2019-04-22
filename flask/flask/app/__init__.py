from flask import Flask, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_url_path='')

# TODO get database name and pass from config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/mysql'
db = SQLAlchemy(app)

from app import views, routes, models
