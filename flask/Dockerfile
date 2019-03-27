FROM python:latest

RUN apt-get update -y && \
    apt-get install -y python3.3 python-dev python-pip && \
    pip install psutil flask

COPY ./flask /flask
WORKDIR /flask
ENTRYPOINT ["python"]
CMD ["flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
