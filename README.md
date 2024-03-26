# Интернет-магазин MEGANO
Владелец торгового центра во время COVID-карантина решил перевести своих арендодателей в онлайн. Сделать это он намерен с помощью создания платформы, на которой продавцы смогут разместить информацию о себе и своём товаре. Онлайновый торговый центр или, другими словами, интернет-магазин, являющийся агрегатором товаров различных продавцов.
## log:pass
admin@gmail.com:123456
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
## Импорт данных

Приложение предоставляет возможность импорта данных из файлов CSV. Для успешного импорта необходимо следовать определенной структуре данных в CSV-файле.

### Структура CSV-файла

CSV-файл должен содержать следующие колонки:

1. **Название товара**: Наименование продукта.
2. **Основная категория**: Название основной категории, к которой принадлежит продукт.
3. **Подкатегория**: Название подкатегории, если она присутствует.
4. **Описание**: Описание продукта.
5. **Детали**: Дополнительные детали продукта в формате "ключ: значение".
6. **Теги**: Список тегов, разделенных запятыми.
7. **Цена**: Цена продукта.
8. **Остаток**: Количество оставшихся продуктов.

Пример структуры CSV-файла:

```csv
Название товара,Основная категория,Подкатегория,Описание,Детали,Теги,Цена,Остаток
Пример товара 1,Электроника,Смартфоны,Мощный смартфон,Размер экрана: 6",RAM: 4GB,Android,500,20
Пример товара 2,Одежда,Обувь,Удобные кроссовки,Цвет: черный,Размер: 42,Спорт,120,50
```
## Пример файла CSV

Вы можете воспользоваться [этим примером файла CSV](market/docs/Sheet1.csv) для тестирования импорта. Скачайте файл и используйте его для импорта данных в приложение.

### Инструкции по импорту

1. Войдите в систему и перейдите на страницу импорта.
2. Выберите файл CSV для импорта.
3. Нажмите кнопку "Начать импорт".
4. После завершения импорта вы увидите результаты операции.

Обратите внимание, что успешный импорт зависит от корректной структуры файла и данных в нем. Пожалуйста, удостоверьтесь, что ваш файл CSV соответствует указанным требованиям.

# Запуск Celery

Celery используется для асинхронной обработки задач. Убедитесь, что виртуальный окружение активировано, и сервер запущен, затем откройте новое окно терминала и выполните следующие команды:

**Запуск Celery Worker:**

```bash
celery -A config worker -l info

```
**Запуск Celery Beat откройте новое окно терминала:**

```bash
celery -A config beat -l info
```

Это запустит Celery Worker и Celery Beat, обеспечивая асинхронную обработку задач в фоновом режиме.

## Дополнительные замечания
Убедитесь, что у вас установлен и запущен брокер сообщений Redis, так как Celery требует его для управления очередью задач.

## Запуск оболочки django-extensions
```bash
python manage.py shell_plus  --print-sql
```

# Цели проекта

Код написан в учебных целях — это курс по Джанго на сайте [Skillbox](https://go.skillbox.ru/education/course/django-framework).
