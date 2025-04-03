#!/bin/sh
# Verify that Postgres is healthy before applying the migrations and running the Django development server

if [ "$POSTGRES_DB" = "trois-rivieres" ]; then
    echo "Waiting for trois-rivieres..."
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

python ./manage.py makemigrations api
python ./manage.py makemigrations
python ./manage.py migrate
gunicorn --timeout 300 UserManagement.wsgi:application --bind 0.0.0.0:8000
exec "$@"
