FROM alpine:latest

RUN apt-get update && \
    apt-get install python3 python-pip && \
    pip install psutil

USER nobody
EXPOSE 8080
