python3 manage.py migrate
python3 manage.py collectstatic --noinput
exec gunicorn api.config.wsgi:application --bind 0.0.0.0:8000