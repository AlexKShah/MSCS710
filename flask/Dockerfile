FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3.7 python-dev python-pip build-essential supervisor && \
    pip install psutil flask
RUN mkdir -p /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./flask /flask
WORKDIR /flask
ENTRYPOINT ["python"]
CMD ["flasktest.py"]
CMD ["/usr/bin/supervisord"]
EXPOSE 5000
