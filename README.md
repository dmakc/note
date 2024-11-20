#  Note

Сайт, который поможет вам не забыть о самом важном!

## Описание проекта

Проект создан для ведения заметок.
Посетителям доступна страница регистрации пользователей.
Авторизованные пользователи могут добавлять заметки и читать заметки других посетителей.

___
## Стек технологии
![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg) ![Django 3.2.15](https://img.shields.io/badge/Django-3.2.16-green.svg)

## Как развернуть проект

1. Клонировать репозиторий git@github.com:dmakc/note.git
```
git clone git@github.com:dmakc/note.git
```

2. Установить и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```

3. Установить зависимости и применить миграции
```
pip install -r requirements.txt
python manage.py migrate
```

4. Создать суперпользователя
```
python manage.py createsuperuser
```

5. Запустить проект
```
python manage.py runserver
```

## Автор
[Давыдов Максим](https://github.com/dmakc)
