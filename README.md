# Foodgram
## Продуктовая социальная сеть для любителей вкусной еды и ценителей необычных рецептов.

### Технологии backend:
Python, Django, Django Rest-Framework, Docker, Postgres, Nginx

### Для запуска потребуется:

- Создать файл .env в корневой директории проекта и добавить переменные:
```bash
sudo nano .env

    DB_ENGINE=<СУБД проекта>
    DB_NAME=<название СУБД>
    POSTGRES_USER=<имя пользователя СУБД>
    POSTGRES_PASSWORD=<пароль пользователя СУБД>
    DB_HOST=<сервер размещения СУБД>
    DB_PORT=<порт доступа к СУБД>
    SECRET_KEY=<секретный ключ проекта>
    ALLOWED_HOSTS=<разрешённые сервера проекта>
    DEBUG=<False - для рабочего режима, True - для режима отладки>
```
- В папке infra в разделе с проектом выполнить команду:
```bash
docker-compose up -d
```
- Установка необходимых приложений, миграции и сбор статики выполняются при сборке образа.
```
- Задать суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

### Может быть полезно:
- Установка Docker:
```bash
pip install docker
pip install docker-compose
```
- Клонирование с GitHub:
```bash
git clone https://<имя_пользователя_на_github>:<пароль>@github.com/Danielseddian/foodgram-project-react
```
- Копиование образа с DockerHub:
```bash
docker pull danielseddian/foodgram
```

_Redoc проекта с инструкцией для доступа к API сервера: http://www.webtodo.xyz/api/docs/redoc/_

_Автор: Кучин Денис, DanielSeddian@, при поддержке наставников и материалов учебного курса_ *Яндекс.Практикум Python-разработчик*
![foodgram workflow](https://github.com/Danielseddian/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### web-адрес проекта:
- webtodo.xyz
### логин и пароль администратора:
- Yandex.Practicum
- Practicum1q2w3e
