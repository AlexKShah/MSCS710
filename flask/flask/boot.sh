#!/bin/sh
exec export FLASK_APP=run.py
exec gunicorn -w 4 -b 0.0.0.0:5000 "run:create_app()"
