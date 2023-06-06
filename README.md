## Federation of Sports Tourism of Russia API (FSTR API)
---
### Content
1. [About](#about)
2. [Configuration](#installation)
3. [GET method](#GET_method)
4. [POST method](#POST_method)
5. [PATCH method](#PATCH_method)
---
<a id='about'></a>
### About
FSTR API is a small API for working with databases with specific structure which is required in FSTR.
Speaking about the version which is loaded on the GitHub, it bases on the __Django 4.2.1__, __Django Rest Framework 3.14.0__. 
__DRF Spectacular 0.26.2__ is used for automatical generation of the documentation.
__Schema documetation__ can be get by typing `http://127.0.0.1:8000/api/schema/`.
Alse you can just view __Schema__ by typing `http://127.0.0.1:8000/api/docs/`.
___
<a id='installation'></a>
### Installation
PostgreSQL is used as a base database, but anyway you can use all databases which Django supports. 
All environmental variables are kept in the __.env__ file right in the directory.
>In this way first of all create __.env__ in the directory with the following variables:
```python
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=...
```
>For working with environmental variables __Python Dotenv 1.0.0__ is used.

Then, configure `setting.py` in the `fstr_rest` directory according to your settings.
After all this operation you can type `python manage.py runserver` for checking if everything is correct.
___
<a id='GET_method'></a>
### GET method
>__Attention__: all examples below are presented for `localhost` server. That's why for your server these can be different.

__GET method__ works in two ways.
1. __Get all _heights___ by typing `http://127.0.0.1:8000/submitData/`.
In this way you will get all data of all _heights_ in the database in the following format:
```python
[
    {
        "beauty_title": "example__beauty_title",
        "title": "example_title",
        "other_titles": "examaple_other_titles",
        "connect": "example_connect",
        "add_time": "2024-05-31T20:19:38.075000Z",
        "user": {
            "email": "example@mail.ru",
            "last_name": "example_last_name",
            "first_name": "example_first_name",
            "patronymic": "example_patronymic",
            "phone": "example_phone" #Phone is configured for russian format, 
            #you can changed it in the models.py in the rest directory.
        },
        "coords": {
            "height": 100,
            "longitude": 0.0,
            "latitude": 0.0
        },
        "level": {
            "winter": "",
            "spring": "",
            "summer": "",
            "autumn": ""
        },
        "images": [
            {
                "title": "string",
                "image": "string"
            }
        ]
    },
...
]
```
2. __Get all _height_ by sorting with the following user.__ For this purpose, parametrn `user_email=...` is available.
Speaking about the Backend part. Model requires `email` field unique. In this way you can sort all `heights` by the user with the help of his email.
For that you need type `http://127.0.0.1:8000/submitData/?user_email=example@mail.ru`.
After it you will get all information about `height` like in firt example but for __only one user__.

>__Attention__: there is a concealed field `status` for every `height`. It has 4 possible values that can be changed only by moderators: `new`, `pending`, `accepted` and `rejected`.
___
<a id="POST_method"></a>
### POST method
Working with __POST method__ is quite easy. You need pass the data in JSON format to the `http://127.0.0.1:8000/submitData/` URL like in the example below:
```python
[
    {
        "beauty_title": "example__beauty_title",
        "title": "example_title",
        "other_titles": "examaple_other_titles",
        "connect": "example_connect",
        "add_time": "2024-05-31T20:19:38.075000Z",
        "user": {
            "email": "example@mail.ru",
            "last_name": "example_last_name",
            "first_name": "example_first_name",
            "patronymic": "example_patronymic",
            "phone": "example_phone" #Phone is configured for russian format, 
            #you can changed it in the models.py in the rest directory.
        },
        "coords": {
            "height": 100,
            "longitude": 0.0,
            "latitude": 0.0
        },
        "level": {
            "winter": "",
            "spring": "",
            "summer": "",
            "autumn": ""
        },
        "images": [
            {
                "title": "string",
                "image": "string"
            }
        ]
    },
...
]
```
Speaking about the fields:
1. `beauty_title` requires string format. (Required)
2. `title` requires string format. (Required)
3. `other_titles` requires string format. (Required)
4. `connect` requires string format. Here you need to pass something which is user for connection. (Not required)
5. `add_time` requires DateTime format like in SQL databases. (Required)
6. `user`:
    6.1. `email` requires email format with the special symbol `@`. (Required)
    6.2. `last_name` requires string format. (Required)
    6.3. `first_name` requires string format. (Required)
    6.4. `patronymic` requires string format. (Required)
    6.5. `phone` is special field for phone number. You can type `+79532125354` or `+7 953 212 53 54` - there is no matter. All input will be turn into following `+79532125354`. (Required)
7. `Coords`:
    7.1. `Height` requires integer format. (Required)
    7.2. `longitude` requires float format. (Required)
    7.3. `latitude` requires float format. (Required)
    Coords are used like a unique key for `heights`. With the help of them, system checks if `height` with passing coords exists. 
    If you will try to duplicate the existing `height` it will return `{"message": 'Такой объект уже существует'}`.
8. `Level`:
    All fields can accept the following values `1A`, `1B`, `2A`...`3B`.
9. `images` working with the list. You can pass several fields with the following format:
    ```
    {
                "title": "string",
                "image": "string"
            }
    ```
    `title` requires string format.
    `image` requires image format.

After creation every `height` get `status` field with the value `new`. The response `{"status": 200, "message": "null", "id": "id of created height"}` will be returned.
However, if there are any proble with database connection it will return `{"message": "Ошибка записи в базу данных"}`.
___
<a id='PATCH_method'></a>
### PATCH method
This is similar to the __POST method__ but you need to pass `id` of the `height` you want to change.
>__Attention__: you can change values of all fields except for `user`. This information is restricted for changing and will be skipped.

If `status` field of changing `height` has value `new`, it will be changed. However, if it has any other value, it can't be changed. In this way it will return `{"state": 0, "message": "Статус объекта не позволяет осуществлять редактирование"}`.
If everything is correct, it will return `{"state": 1, "message": "null"}`.
___
For more information you can connect with me on the GitHub.
