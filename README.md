# Purpose

1. Создайте docker-compose:
    База данных (postgres, mysql, clickhouse или другое)
    Сервер для создания api (Django, Flask, FastApi или другое)

2. Создайте два метода:

    2.1 POST /hero/ обязательный параметр name. Должен найти героя по апи с таким именем https://superheroapi.com/ и добавить его в базу данных, если нет героя с таким именем, вернуть ошибку, что нет такого героя.

    2.2 GET /hero/
    Параметры (все необязательные):
    - name
    - intellegence
    - strength
    - speed
    - power

    Параметр name - ищет точное совпадение
    Остальные числовые параметры ищут по значению больше или равно, меньше или равно и точное совпадение.

    Выводит всех героев с учётом фильтров из базы данных, если нет героев с такими параметрами, то выводить ошибку.

3. Написать тесты для обоих методов на pytest.

! Для работы с базой данных используйте любую ORM (Django ORM, SqlAlchemy или другую)

# Development

## Dev environment

### Before the very first use

* ```
    # install uv
    uv sync
    uv tool run pre-commit install
    ```
* In IDE, do not forget to select the environment from `.venv`

### Setting application parameters
* Copy .env.example to .env
* Set the following variables:
    * app_superhero_api_access_token (On abtaining the value, check https://superheroapi.com/)

### Running the application (non-containerized)
* `python -m app`
* Note in the logs: `Uvicorn running on http://localhost:8080 (Press CTRL+C to quit)`
* Optionally, open API docs UI: http://127.0.0.1:8080/docs or http://127.0.0.1:8080/redoc

### Running the application (Docker)
* Define the app_superhero_api_access_token env variable in docker-compose.yml
* `docker compose up -d --build`
* Browse Swagger on http://localhost:8080/docs

### Running linters
* `ruff check`
* `mypy app`

### API docs
* OpenAPI specification: /openapi.json
* Swagger UI: /docs
* ReDoc: /redoc

# Deployment

## Linting and type checking

* `docker build --tag superhero-api-proxy-test --target test .`
* `docker run --rm superhero-api-proxy-test ruff check`
* `docker run --rm superhero-api-proxy-test mypy app`
* TODO: Add unit testing

## Building

* `docker build --tag superhero-api-proxy .`

# ToDo

* Add DB-baked repository for the hero info (keep in-memory implementation for unit tests)
* Add descriptions to API docs
* In the hero repo, evaluate the implementation using PG-specific "upserts" (complexity, readability)
* Add unit tests using in-memory implementation of hero repo, include to Docker for CI
* Make function-level isolation for all tests and fixtures
* Migrate from dependency-injector to dishka
