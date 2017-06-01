# Setup on Mac

## install python

```
brew install python
```

## install MySQL database (if you use MySQL)

```
brew install mysql
```

## install other system dependencies

wand depends on imagemagick@6

```
brew install freetype
brew install imagemagick@6
```

in case you have imagemagick@7 installed

```
brew unlink imagemagick
brew link imagemagick@6 --force
```

## Install django requirements

```
pip install -r requirements.txt
```

# Launch Django App

## Start mysql database (if you use MySQL)

change the MySQL connection settings in the config file:

```
gov_track_hk_web/gov_track_hk_web/settings.py
```

```
mysql.server start
```

## Run db migrations

```
python manage.py migrate
```

## Start django app server

```
python manage.py runserver
```
