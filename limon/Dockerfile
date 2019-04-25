FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y curl supervisor python3 python3-dev python3-pip python3-venv software-properties-common mysql-server && \
    #pip3 install -U -r requirements.txt && \
    pip3 install psutil gunicorn flask flask-login flask-mysql Flask-SQLAlchemy mysql-connector-python pandas schedule pyyaml pytest pandas numpy
    # asn1crypto==0.24.0 atomicwrites==1.3.0 attrs==19.1.0 Click==7.0 cryptography==2.1.4 Flask==1.0.2 Flask-Login==0.4.1 Flask-MySQL==1.4.0 Flask-SQLAlchemy==2.3.2 gunicorn==19.9.0 idna==2.6 itsdangerous==1.1.0 Jinja2==2.10.1 keyring==10.6.0 keyrings.alt==3.0 MarkupSafe==1.1.1 more-itertools==7.0.0 mysql-connector-python==8.0.15 numpy==1.16.3 pandas==0.24.2 pluggy==0.9.0 protobuf==3.7.1 psutil==5.6.1 py==1.8.0 pycrypto==2.6.1 pygobject==3.26.1 PyMySQL==0.9.3 pytest==4.4.1 python-dateutil==2.8.0 pytz==2019.1 pyxdg==0.25 PyYAML==5.1 schedule==0.6.0 SecretStorage==2.3.1 six==1.11.0 SQLAlchemy==1.3.3 Werkzeug==0.15.2

RUN service mysql start

COPY ./flask /flask
WORKDIR /flask

#expose flask port
EXPOSE 5000

# expose mysql port
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
