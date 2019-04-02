FROM mariadb:latest

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./db /db
WORKDIR /db

CMD ["/user/bin/mysql –user=root –password=password limon && mysql limon < script.sql"]
