FROM ubuntu:latest

#prevent time zone setup from interrupting installation
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#Install products and dependencies for mysql, flask, supervisord
RUN apt-get update -y && \
    apt-get install -y curl libmysqlclient-dev supervisor python3 python3-dev python3-pip python3-venv software-properties-common && \
    pip3 install psutil gunicorn mysqlclient flask flask-login flask-mysql Flask-SQLAlchemy sqlalchemy mysql-connector-python pandas schedule pyyaml pytest pandas numpy

#copy all our files within limon container context
COPY ./flask /flask
WORKDIR /flask

#expose flask port
EXPOSE 5000

# supervisor setup
# make supervisor directories
RUN    mkdir -p /var/log/supervisor && \
       mkdir -p /etc/supervisor/conf.d

# move supervisor conf
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# launch supervisor, make it use local conf file
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
