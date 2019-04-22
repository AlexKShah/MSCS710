FROM mariadb:latest

COPY ./db /db
COPY mariadb.conf /etc/mysql/conf.d/config-file.cnf
WORKDIR /db

CMD ["/user/bin/mysql –user=alex –password=password poll"]
