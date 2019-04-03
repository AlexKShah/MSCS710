FROM ubuntu:latest

RUN        apt update && \
           apt install -y supervisor
RUN        apt-get -y install supervisor && \
           mkdir -p /var/log/supervisor && \
           mkdir -p /etc/supervisor/conf.d
RUN        mkdir /var/log/supervisord

COPY       supervisord.conf /
COPY       supervisord.log /

CMD ["/usr/bin/supervisord"]
