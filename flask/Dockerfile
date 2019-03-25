FROM alpine:latest

RUN apt-get update -y && \
    apt-get install -y python3 python-dev python-pip && \
    pip install psutil flask

COPY ./flask
WORKDIR /flask
ENTRYPOINT ["python"]
CMD ["flasktest.py"]
