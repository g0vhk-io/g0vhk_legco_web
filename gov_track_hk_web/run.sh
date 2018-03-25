python3 manage.py migrate
python3 manage.py collectstatic --noinput
DJANGO_DEBUG=false python3 manage.py runserver 0.0.0.0:8080
