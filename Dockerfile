FROM python:3.11-alpine

# Set workdirectory
WORKDIR /flask_achemy_mysql

# install dependencies
COPY requirements.txt .
RUN apk add --no-cache mariadb-dev build-base && \
    pip install -r requirements.txt && \
    apk del mariadb-dev && \
    apk add --no-cache mariadb-connector-c-dev

# copy project
COPY . .

# mysql conf
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mariadb"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/mariadb -lmysqlclient"


EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
# copy entrypoint.sh
# COPY entrypoint.sh .

# # установка разрешений на выполнение для entrypoint.sh
# RUN chmod +x entrypoint.sh

# # run entrypoint.sh
# # ENTRYPOINT ["/flask_achemy_mysql/entrypoint.sh"]
