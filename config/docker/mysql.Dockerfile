FROM mysql:latest
COPY ./config/sql/* /docker-entrypoint-initdb.d/
