# Setup on Docker

## Install docker and docker-compose

## Build docker image and start DB container
```
docker-compose build
docker-compose up -d db
```
(wait for a while, let db finish setup...)

## Run db migrate on django container
```
docker-compose run --rm web python manage.py migrate
docker-compose up -d web
```

Open http://localhost:8000 on browser
