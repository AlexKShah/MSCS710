from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import yaml
import pathlib

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#get database parameters from config
with open("sys_poll.yml", 'r') as configfile:
    cfg = yaml.safe_load(configfile)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + cfg['db_username'] + ':'+ cfg['db_password'] + '@' + cfg['db_host'] + '/poll'
db = SQLAlchemy(app)

from app import routes, models
