# g0vhk Legco website
香港人的線上民主平台 (<http://govhk.io>)


## Quick Start with Docker
1. Install docker and docker-compose
2. Build docker image and start DB container
    ```
    docker-compose build
    docker-compose up -d db
    ```
3. Run db migrate on django container
    ```
    docker-compose run --rm web python manage.py migrate
    docker-compose up -d web
    ```
4. Open <http://localhost:8000> on browser


## Running on Mac without Docker

### Prerequisite requirements
Python 2.7, Django 1.9.7, ImageMagick 6.x, MySQL (optional)

Below is the steps to install these requirements on MacOS with [Homebrew](https://brew.sh/):

- Install Python: `brew install python`
- Install MySQL (optional): `brew install mysql`
- Install Freetype: `brew install freetype`
- Install ImageMagick 6.x: `brew install imagemagick@6`

Since [Wand](https://github.com/dahlia/wand/) depends on imagemagick@6, In case you have imagemagick@7 installed

```
brew unlink imagemagick
brew link imagemagick@6 --force
```

### Install project dependencies
```
git clone https://github.com/g0vhk-io/g0vhk_legco_web.git
cd g0vhk_legco_web
pip install -r requirements.txt
```

### Config database 
change the MySQL connection settings in the config file: `gov_track_hk_web/gov_track_hk_web/settings.py`

Example config (MySQL)
```
DATABASES = {
    'default': {
        'OPTIONS': {
            'read_default_file': '/etc/mysql/gov_track_hk.cnf',
        },
    }
}
```
Example gov_track_hk.cnf
```
[client]
host = HOST
database = govlabhk
user = USER
password = PASSWORD
default-character-set = utf8
```

### Start mysql database (if you use MySQL)

```
mysql.server start
```

### Run DB migrations
Create the database if not exists, then run this command
```
python manage.py migrate
```

### Start Django app server

```
python manage.py runserver
```
Open <http://localhost:8000> in browser


## How to contribute
Fork, modify and send pull requests

## Contact and discussion
- Facebook: <https://www.facebook.com/g0vhk.io/>
- Code4HK Facebook group: <https://www.facebook.com/groups/code4hk/>

## Licence
(TODO)