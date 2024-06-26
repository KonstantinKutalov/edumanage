# Документация проекта "edumanage"

## 1. Обзор

Проект "edumanage" представляет собой веб-приложение, которое позволяет пользователям создавать, просматривать,
редактировать и удалять модули. Каждый модуль имеет уникальный порядковый номер, название, описание и принадлежит
определенному пользователю.

## 2. Структура проекта

| Директория | Файлы                                                                                                                   | Описание                                  |
|------------|-------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| config     | `__init__.py`, `asgi.py`, `celery.py`, `settings.py`, `urls.py`, `wsgi.py`                                              | Конфигурационные файлы проекта            |
| modules    | `__init__.py`, `admin.py`, `apps.py`, `models.py`, `pagination.py`, `serializers.py`, `tests.py`, `urls.py`, `views.py` | Все, что связано с моделью "Модуль"       |
| users      | `__init__.py`, `admin.py`, `apps.py`, `models.py`, `serializers.py`, `tests.py`, `urls.py`, `views.py`                  | Все, что связано с моделью "Пользователь" |

## 3. Модели

### 3.1. Модуль (modules.models.Module)

* **number** (IntegerField): Порядковый номер модуля (уникальный).
* **name** (CharField): Название модуля (не более 100 символов).
* **description** (TextField): Описание модуля (необязательно).
* **owner** (ForeignKey): Владелец модуля (связан с моделью User).

### 3.2. Пользователь (users.models.User)

* **email** (EmailField): Email пользователя (уникальный).
* **first_name** (CharField): Имя пользователя.
* **last_name** (CharField): Фамилия пользователя.

## 4. API

### 4.1. Модули

#### 4.1.1. Создание модуля

* **Метод:** POST
* **URL:** `/modules/create/`
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>`
* **Данные запроса (JSON):**
    ```json
    {
        "number": 1,
        "name": "Название модуля",
        "description": "Описание модуля"
    }
    ```
* **Ответ (JSON):**
    * **201 Created:** Модуль успешно создан.
    ```json
    {
        "id": 1,
        "number": 1,
        "name": "Название модуля",
        "description": "Описание модуля",
        "owner": 1
    }
    ```
    * **400 Bad Request:** Неверные данные в запросе.
    * **401 Unauthorized:** Не авторизован.

#### 4.1.2. Получение списка модулей

* **Метод:** GET
* **URL:** `/modules/`
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>`
* **Ответ (JSON):**
    * **200 OK:** Список модулей.
    ```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "number": 1,
                "name": "Название модуля 1",
                "description": "Описание модуля 1",
                "owner": 1
            },
            {
                "id": 2,
                "number": 2,
                "name": "Название модуля 2",
                "description": "Описание модуля 2",
                "owner": 1
            }
        ]
    }
    ```
    * **401 Unauthorized:** Не авторизован.

#### 4.1.3. Просмотр модуля

* **Метод:** GET
* **URL:** `/modules/<int:pk>/`
* **Параметры пути:**
    * `pk` (int): ID модуля.
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>`
* **Ответ (JSON):**
    * **200 OK:** Информация о модуле.
    ```json
    {
        "id": 1,
        "number": 1,
        "name": "Название модуля",
        "description": "Описание модуля",
        "owner": 1
    }
    ```
    * **401 Unauthorized:** Не авторизован.
    * **404 Not Found:** Модуль не найден.

#### 4.1.4. Обновление модуля

* **Метод:** PUT
* **URL:** `/modules/update/<int:pk>/`
* **Параметры пути:**
    * `pk` (int): ID модуля.
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>`
* **Данные запроса (JSON):**
    ```json
    {
        "name": "Новое название модуля",
        "description": "Новое описание модуля"
    }
    ```
* **Ответ (JSON):**
    * **200 OK:** Модуль успешно обновлен.
    ```json
    {
        "id": 1,
        "number": 1,
        "name": "Новое название модуля",
        "description": "Новое описание модуля",
        "owner": 1
    }
    ```
    * **400 Bad Request:** Неверные данные в запросе.
    * **401 Unauthorized:** Не авторизован.
    * **403 Forbidden:** У пользователя нет прав на редактирование модуля.
    * **404 Not Found:** Модуль не найден.

#### 4.1.5. Удаление модуля

* **Метод:** DELETE
* **URL:** `/modules/delete/<int:pk>/`
* **Параметры пути:**
    * `pk` (int): ID модуля.
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>`
* **Ответ:**
    * **204 No Content:** Модуль успешно удален.
    * **401 Unauthorized:** Не авторизован.
    * **403 Forbidden:** У пользователя нет прав на удаление модуля.
    * **404 Not Found:** Модуль не найден.

### 4.2. Пользователи

#### 4.2.1. Создание пользователя

* **Метод:** POST
* **URL:** `/users/`
* **Данные запроса (JSON):**
    ```json
    {
        "email": "example@email.com",
        "password": "password",
        "first_name": "Имя",
        "last_name": "Фамилия"
    }
    ```
* **Ответ (JSON):**
    * **201 Created:** Пользователь успешно создан.
    ```json
    {
        "id": 1,
        "email": "example@email.com",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "module_count": 0
    }
    ```
    * **400 Bad Request:** Неверные данные в запросе.

#### 4.2.2. Получение списка пользователей

* **Метод:** GET
* **URL:** `/users/`
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>` (только для администраторов)
* **Ответ (JSON):**
    * **200 OK:** Список пользователей.
    ```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "email": "example@email.com",
                "first_name": "Имя",
                "last_name": "Фамилия",
                "module_count": 2
            },
            {
                "id": 2,
                "email": "admin@email.com",
                "first_name": "Admin",
                "last_name": "Admin",
                "module_count": 0
            }
        ]
    }
    ```
    * **401 Unauthorized:** Не авторизован.
    * **403 Forbidden:** У пользователя нет прав на просмотр списка пользователей.

#### 4.2.3. Просмотр пользователя

* **Метод:** GET
* **URL:** `/users/<int:pk>/`
* **Параметры пути:**
    * `pk` (int): ID пользователя.
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>` (только для администраторов)
* **Ответ (JSON):**
    * **200 OK:** Информация о пользователе.
    ```json
    {
        "id": 1,
        "email": "example@email.com",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "module_count": 2
    }
    ```
    * **401 Unauthorized:** Не авторизован.
    * **403 Forbidden:** У пользователя нет прав на просмотр информации о пользователе.
    * **404 Not Found:** Пользователь не найден.

#### 4.2.4. Обновление пользователя

* **Метод:** PUT
* **URL:** `/users/<int:pk>/`
* **Параметры пути:**
    * `pk` (int): ID пользователя.
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>` (только для администраторов)
* **Данные запроса (JSON):**
    ```json
    {
        "first_name": "Новое имя",
        "last_name": "Новая фамилия"
    }
    ```
* **Ответ (JSON):**
    * **200 OK:** Пользователь успешно обновлен.
    ```json
    {
        "id": 1,
        "email": "example@email.com",
        "first_name": "Новое имя",
        "last_name": "Новая фамилия",
        "module_count": 2
    }
    ```
    * **400 Bad Request:** Неверные данные в запросе.
    * **401 Unauthorized:** Не авторизован.
    * **403 Forbidden:** У пользователя нет прав на обновление информации о пользователе.
    * **404 Not Found:** Пользователь не найден.

#### 4.2.5. Удаление пользователя

* **Метод:** DELETE
* **URL:** `/users/<int:pk>/`
* **Параметры пути:**
    * `pk` (int): ID пользователя.
* **Заголовки:**
    * `Authorization: Bearer <токен_аутентификации>` (только для администраторов)
* **Ответ:**
    * **204 No Content:** Пользователь успешно удален.
    * **401 Unauthorized:** Не авторизован.
    * **403 Forbidden:** У пользователя нет прав на удаление пользователя.
    * **404 Not Found:** Пользователь не найден.

## 5. Аутентификация

Для доступа к API требуется аутентификация с использованием JWT (JSON Web Token).

### 5.1. Получение токена

* **Метод:** POST
* **URL:** `/users/token/`
* **Данные запроса (JSON):**
    ```json
    {
        "email": "example@email.com",
        "password": "password"
    }
    ```
* **Ответ (JSON):**
    * **200 OK:** Токен аутентификации.
    ```json
    {
        "access": "токен_доступа",
        "refresh": "токен_обновления"
    }
    ```
    * **400 Bad Request:** Неверные данные в запросе.
    * **401 Unauthorized:** Неправильный email или пароль.

### 5.2. Обновление токена

* **Метод:** POST
* **URL:** `/users/token/refresh/`
* **Данные запроса (JSON):**
    ```json
    {
        "refresh": "токен_обновления"
    }
    ```
* **Ответ (JSON):**
    * **200 OK:** Новый токен аутентификации.
    ```json
    {
        "access": "новый_токен_доступа"
    }
    ```
    * **400 Bad Request:** Неверные данные в запросе.
    * **401 Unauthorized:** Токен обновления не действителен.

## 6. Права доступа

* **Пользователь:**
    * Может создавать, просматривать, редактировать и удалять только свои модули.
* **Администратор:**
    * Может создавать, просматривать, редактировать и удалять все модули и пользователей.

## 7. Тестирование

Тесты для проекта написаны с использованием модуля `django.test`.

## 8. Дополнительная информация

* Проект использует Celery для выполнения задач в фоновом режиме.
* Для хранения данных используется PostgreSQL.
* Для кэширования используется Redis.

## 9. Документация API

Документация API доступна по адресу [http://localhost:8000/swagger/](http://localhost:8000/swagger/).

## 10. Развертывание проекта

### 10.1. Локальное развертывание

1. **Клонирование репозитория:**
    ```sh
    git clone https://github.com/KonstantinKutalov/edumanage.git
    cd edumanage
    ```

2. **Создание виртуального окружения и установка зависимостей:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Создание файла `.env`:**
    ```sh
    cp .env.example .env
    ```
   Отредактируйте файл `.env`, добавив необходимые переменные окружения, необходимые окружения в `.env.sample`.

4. **Применение миграций и запуск сервера:**
    ```sh
    python manage.py migrate
    python manage.py runserver
    ```

5. **Запуск Celery:**
    ```sh
    celery -A edumanage worker -l info
    ```

### 10.2. Развертывание с использованием Docker

1. **Клонирование репозитория:**
    ```sh
    git clone https://github.com/KonstantinKutalov/edumanage.git
    cd edumanage
    ```

2. **Создание файла `.env`:**
    ```sh
    cp .env.example .env
    ```
   Отредактируйте файл `.env`, добавив необходимые переменные окружения, необходимые окружения указано в `.env.sample`.

3. **Запуск контейнеров:**
    ```sh
    docker-compose up --build
    ```

## Дипломная работа выполнена по заданию # ТВ2

## Описание

Написать небольшой проект на Django и Django Rest Framework с моделью "Образовательные модули". В них есть:

- порядковый номер
- название
- описание

## Задача

<aside>
👾 При создании проекта нужно:

1. реализовать для модели (моделей) все методы CRUD

2. Полностью покрыть автоматизированными юнит-тестами все модели, сериализаторы, виды.

</aside>

## Требуемый стэк

- python 3.11
- Docker
- Django

### Условия приемки

- код размещен в открытом репозитории
- доступна документация
- код покрыт автоматизированными юнит-тестами
- код оформлен согласно pep8
- оформлен Readme файл
- в проекте использован Docker