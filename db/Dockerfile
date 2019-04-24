FROM mariadb:latest

COPY ./db /db
COPY mariadb.conf /etc/mysql/conf.d/mariadb.cnf
WORKDIR /db

CMD ["service mysqld start"]
