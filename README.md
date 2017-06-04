# Quick Start

## Setup on Docker
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
4. Open http://localhost:8000 on browser


# Running on Mac without Docker
1. install python
    ```
    brew install python
    ```
2. install MySQL database (if you use MySQL)
    ```
    brew install mysql
    ```
3. install other system dependencies
    (wand depends on imagemagick@6)
        ```
        brew install freetype
        brew install imagemagick@6
        ```
    in case you have imagemagick@7 installed
        ```
        brew unlink imagemagick
        brew link imagemagick@6 --force
        ```

4. Install django requirements
    ```
    pip install -r requirements.txt
    ```

5. Start mysql database (if you use MySQL)
   change the MySQL connection settings in the config file:
    ```
    gov_track_hk_web/gov_track_hk_web/settings.py
    ```
6. Start MySQL Server
    ```
    mysql.server start
    ```

7. Run db migrations
    ```
    python manage.py migrate
    ```

8. Start django app server
    ```
    python manage.py runserver
    ```
