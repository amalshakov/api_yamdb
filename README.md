# Проект YaMDb

### Описание
Проект YaMDb собирает отзывы пользователей на произведения.

### Технологии
- Python 3.7,
- Django 2.2.19
- Django Rest Framework 3.12.4
- Simple JWT
### Как запустить проект:
- Клонировать репозиторий и перейти в него в командной строке:

```git clone git@github.com:amalshakov/api_yamdb.git```

```cd api_yamdb```

- Cоздать и активировать виртуальное окружение:

```python -m venv env```

```source env/Scripts/activate```

```python -m pip install --upgrade pip```

- Установить зависимости из файла requirements.txt:

```pip install -r requirements.txt```

- Выполнить миграции:

```python manage.py migrate```

- Заполнить базу данных тестовым контентом:

```python manage.py importcsv```

- Запустить проект:

```python manage.py runserver```

- Посмотреть документацию при запущенном сервере:

[Ссылка на документацию](http://127.0.0.1:8000/redoc)

### Авторы:
- [Мальшаков Александр](https://github.com/amalshakov)
- [Печерица Андрей](https://github.com/Pe4enka5)
- [Михайлов Андрей](https://github.com/Andew-063)
