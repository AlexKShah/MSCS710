#flask setup
FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y supervisor python3 python3-dev python3-pip && \
    pip3 install psutil flask mysql-connector-python pandas schedule pyyaml pytest

COPY ./flask /flask
WORKDIR /flask
EXPOSE 5000

# supervisor setup

# make directories
RUN    mkdir -p /var/log/supervisor && \
       mkdir -p /etc/supervisor/conf.d

# move conf
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# launch supervisor, make it use local conf file
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
