FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3.7 python-dev python-pip build-essential supervisor && \
    pip install psutil flask

COPY ./flask /flask
WORKDIR /flask
ENTRYPOINT ["python"]
CMD ["run.py"]
EXPOSE 5000
