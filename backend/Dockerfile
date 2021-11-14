FROM python:3.7

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py makemigrations &&\
 python manage.py migrate &&\
 python manage.py collectstatic --noinput &&\
 gunicorn foodgram.wsgi:application --bind 0:8000