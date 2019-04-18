FROM ubuntu:latest

RUN        apt update && \
           apt-get -y install supervisor && \
           mkdir -p /etc/supervisor/conf.d && \
           chmod 777 /etc/supervisor/conf.d/

COPY       supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN        chmod 777 /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
