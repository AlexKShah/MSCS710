FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y curl supervisor python3 python3-dev python3-pip python3-venv software-properties-common && \
    pip3 install psutil gunicorn flask flask-login flask-mysql Flask-SQLAlchemy mysql-connector-python pandas schedule pyyaml pytest && \
    curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash

COPY ./flask /flask
WORKDIR /flask

#mariadb setup
RUN mkdir -p /etc/mysql/conf.d/
ADD mariadb.conf /etc/mysql/conf.d/mariadb.cnf

#expose flask port
EXPOSE 5000
#expose mariadb port
EXPOSE 3306

#prep flask startup
RUN chmod +x boot.sh
ENV FLASK_APP run.py

# supervisor setup

# make supervisor directories
RUN    mkdir -p /var/log/supervisor && \
       mkdir -p /etc/supervisor/conf.d

# move supervisor conf
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# launch supervisor, make it use local conf file
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
CMD ["/bin/sh", "-c", "while true; do echo 'test'; done"]
