# Интернет-магазин MEGANO
Владелец торгового центра во время COVID-карантина решил перевести своих арендодателей в онлайн. Сделать это он намерен с помощью создания платформы, на которой продавцы смогут разместить информацию о себе и своём товаре. Онлайновый торговый центр или, другими словами, интернет-магазин, являющийся агрегатором товаров различных продавцов.
## log:pass
admin@gmail.com:123456
user1@gmail.com:123456
user2@gmail.com:123456
user3@gmail.com:123456
user4@gmail.com:123456
user5@gmail.com:123456
user6@gmail.com:123456
user7@gmail.com:123456
user8@gmail.com:123456
user9@gmail.com:123456
user10@gmail.com:123456


## Как установить
Для работы сервиса требуются:
- Python версии не ниже 3.10.
- установленное ПО для контейнеризации - [Docker](https://docs.docker.com/engine/install/).
- Инструмент [poetry](https://python-poetry.org/) для управления зависимостями и сборкой пакетов в Python.

Настройка переменных окружения
1. Скопируйте файл .env.dist в .env
2. Заполните .env файл. Пример:
```yaml
DATABASE_URL = postgresql://skillbox:secret@127.0.0.1:5439/market
REDIS_URL = redis://127.0.0.1:6379/0
```

## Загрузка фикстур Django

Этот скрипт предназначен для загрузки всех фикстур Django из каталога 'fixtures' в db проекта.

### Использование

- Запустите скрипт, используя интерпретатор Python:

    ```bash
    python load_fixtures.py
    ```

Скрипт автоматически обнаружит и загрузит все файлы JSON в указанном каталоге 'fixtures'. Если порядок загрузки важен, файлы будут обработаны в отсортированном порядке.

### Запуск СУБД Postgresql
```shell
docker run --name skillbox-db-39 -e POSTGRES_USER=skillbox -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=market -p 5439:5432 -d postgres
```
### Запуск брокера сообщений REDIS
```shell
docker run --name redis-db -d -p 6379:6379 redis
```
### Установка и активация виртуального окружения
```shell
poetry install  ; установка пакетов
poetry shell  ; активация виртуального окружения
pre-commit install  ; установка pre-commit для проверки форматирования кода, см. .pre-commit-config.yaml
```
## Как удалить контейнеры
### СУБД Postgres
```shell
docker rm -f -v skillbox-db-39
```

### Брокер сообщений REDIS
```shell
docker rm -f -v redis-db
```

## Проверка форматирования кода
Проверка кода выполняется из корневой папки репозитория.
* Анализатор кода flake8
```shell
flake8 market
```
* Линтер pylint
```shell
pylint --fail-under=7 --rcfile=.pylintrc market/*
```
* Линтер black
```shell
black market
```

## Как запустить web-сервер
Запуск сервера производится в активированном локальном окружение из папки `market/`
```shell
python manage.py runserver 0.0.0.0:8000
```

# Цели проекта

Код написан в учебных целях — это курс по Джанго на сайте [Skillbox](https://go.skillbox.ru/education/course/django-framework).
