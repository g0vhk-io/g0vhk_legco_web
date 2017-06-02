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
