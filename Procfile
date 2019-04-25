release: python manage.py makemigrations --merge
release: python manage.py migrate
web: gunicorn authors.wsgi