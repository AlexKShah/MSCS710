#!flask/bin/python
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import os
import yaml
import time
import pathlib
import datetime
import psutil

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

#get database parameters from config
with open("sys_poll.yml", 'r') as configfile:
    cfg = yaml.safe_load(configfile)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + cfg['db_username'] + ':'+ cfg['db_password'] + '@' + cfg['db_host'] + '/poll'
db = SQLAlchemy(app)

class Metrics(db.Model):
    cpu_percent = db.Column(db.Float())
    memory_percent = db.Column(db.Float())
    name = db.Column(db.String(255))
    num_threads = db.Column(db.Integer)
    pid = db.Column(db.Integer, primary_key=True)

    def __init__(self, cpu_percent, memory_percent, name, timestamp, num_threads, pid):
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent
        self.name = name
        self.num_threads = num_threads
        self.pid = pid

    def __repr__(self):
        return '<{} {} {} {} {}>'.format(self.cpu_percent, self.memory_percent, self.name, self.num_threads, self.pid)

#end class

@app.route('/')
def index():
    try:
        p = psutil.Process()
        with p.oneshot():
          cpunow = psutil.cpu_percent(interval=0.01, percpu=True)
          psutil.getloadavg()
          cpuavg=psutil.getloadavg()
          ramnow = psutil.virtual_memory()[2]
    except psutil.NoSuchProcess:
        pass
    data = Metrics.query.all()
    # give data gathering enough time to not block
    time.sleep(0.1)
    return render_template('index.html', data=data, cpunow=cpunow, ramnow=ramnow, cpuavg=cpuavg)

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=5000)
