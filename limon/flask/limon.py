#!flask/bin/python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import yaml
import pathlib
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

#get database parameters from config
with open("sys_poll.yml", 'r') as configfile:
    cfg = yaml.safe_load(configfile)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + cfg['db_username'] + ':'+ cfg['db_password'] + '@' + cfg['db_host'] + '/poll'
db = SQLAlchemy(app)

class Metric(db.Model):
    cpu_percent = db.Column(db.String(255))
    memory_percent = db.Column(db.String(255))
    name = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=str(datetime.datetime.now()))
    num_threads = db.Column(db.String(255))
    pid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Metric {}>'.format(self.body)
#endblock

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config.html', methods=['GET', 'POST'])
def config():
    return render_template('config.html')

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=5000)
