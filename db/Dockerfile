FROM mysql:8.0

COPY init.sql /docker-entrypoint-initdb.d/

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=wallet_homolog
ENV MYSQL_USER=wallet_api_homolog
ENV MYSQL_PASSWORD=api123

EXPOSE 3306