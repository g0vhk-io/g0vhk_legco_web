# g0vhk Legco website
香港人的線上民主平台 (<http://govhk.io>)

## Prerequisite requirements
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

## Getting started

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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gov_track_hk_web',
        'USER': 'gov_track_hk_web',
        'PASSWORD': 'P@ssw0rd',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
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