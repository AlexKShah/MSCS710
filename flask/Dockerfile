FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3.7 python-dev python-pip build-essential && \
    pip install psutil flask

COPY ./flask /flask
WORKDIR /flask
ENTRYPOINT ["python"]
CMD ["flasktest.py"]
EXPOSE 5000
