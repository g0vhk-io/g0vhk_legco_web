FROM python:2.7.13

RUN apt-get update \
    && apt-get install -y \
        libfreetype6-dev \
        imagemagick \
    && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
ARG MYSQL_USER
ARG MYSQL_PASSWORD
ARG MYSQL_HOST
ARG MYSQL_DATABASE
ARG MYSQL_PORT
ENV MYSQL_USER="$MYSQL_USER"
ENV MYSQL_PASSWORD="$MYSQL_PASSWORD"
ENV MYSQL_HOST="$MYSQL_HOST"
ENV MYSQL_DATABASE="$MYSQL_DATABASE"
ENV MYSQL_PORT="$MYSQL_PORT"
CMD ./run.sh

FROM node:9.8.0-slim
RUN mkdir -p /usr/src/node_app
WORKDIR /usr/src/node_app
COPY . /usr/src/node_app
RUN npm install
CMD ["npm run build-dev"]
