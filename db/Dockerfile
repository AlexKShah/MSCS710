FROM mariadb:latest

COPY ./db /db
WORKDIR /db

CMD ["/user/bin/mysql –user=root –password=password limon && mysql limon < script.sql"]
