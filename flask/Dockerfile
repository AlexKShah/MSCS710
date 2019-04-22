#flask setup
FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y supervisor python3 python3-dev python3-pip python3-venv && \
    pip3 install psutil gunicorn flask flask-login flask-mysql Flask-SQLAlchemy mysql-connector-python pandas schedule pyyaml pytest

COPY ./flask /flask
WORKDIR /flask
EXPOSE 5000

RUN chmod +x boot.sh
ENV FLASK_APP run.py

# supervisor setup

# make directories
RUN    mkdir -p /var/log/supervisor && \
       mkdir -p /etc/supervisor/conf.d

# move conf
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# launch supervisor, make it use local conf file
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
