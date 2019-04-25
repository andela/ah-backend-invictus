release: python manage.py makemigrations --merge && python manage.py migrate
web: gunicorn authors.wsgi --log-file -
