#!/bin/sh
# entrypoint.sh

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py migrate --run-syncdb
python3 manage.py runserver 0.0.0.0:8002