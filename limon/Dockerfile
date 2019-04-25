FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y curl supervisor python3 python3-dev python3-pip python3-venv software-properties-common && \
    pip3 install psutil gunicorn flask flask-login flask-mysql Flask-SQLAlchemy mysql-connector-python pandas schedule pyyaml pytest pandas numpy

#RUN mysql_secure_installation; sleep 30;
#RUN service mysql start

COPY ./flask /flask
WORKDIR /flask

#expose flask port
EXPOSE 5000

# expose mysql port
#EXPOSE 3306

#prep flask startup
#RUN chmod +x boot.sh
ENV FLASK_APP run.py

#ENV MYSQL_ROOT_PASSWORD: password
#ENV MYSQL_DATABASE: poll


# supervisor setup

# make supervisor directories
RUN    mkdir -p /var/log/supervisor && \
       mkdir -p /etc/supervisor/conf.d

# move supervisor conf
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# launch supervisor, make it use local conf file
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
CMD ["/bin/sh", "-c", "while true; do echo 'running...'; sleep 180; done"]
