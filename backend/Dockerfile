FROM python:3.7

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py makemigrations food &&\
 python manage.py migrate --run-syncdb &&\
 python manage.py collectstatic --noinput &&\
 gunicorn foodgram.wsgi:application --bind 0:8000