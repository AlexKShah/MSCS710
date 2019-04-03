FROM ubuntu:latest
RUN apt update && \
    apt install -y supervisor

COPY supervisord.conf /
CMD ["/usr/bin/supervisord"]
