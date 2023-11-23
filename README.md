![CI](https://github.com/brivazz/legpromRF_tz/actions/workflows/code-checker.yml/badge.svg)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/brivazz/legpromRF_tz)
![GitHub language count](https://img.shields.io/github/languages/count/brivazz/legpromRF_tz)![GitHub top language](https://img.shields.io/github/languages/top/brivazz/legpromRF_tz)![Github Repository Size](https://img.shields.io/github/repo-size/brivazz/legpromRF_tz)

# Обогащение данных о рисках по ИНН

### Задание

1) Вытащить и записать в базу всю возможную информацию о рисках компании по ИНН при помощи сервиса <https://damia.ru/apiscoring>
2) Оформить API эндпоинт с помощью fastapi, который будет возвращать эти данные
3) Небольшой фронтик (буквально визуализировать данные)
4) Оформить всё в докер и прислать архив

***

### Используемые технологии сервиса

Технологический стек проекта:

1. [Nginx](https://nginx.org/ru/) - веб-сервер
2. [MongoDB](https://www.mongodb.com/) - документоориентированная БД
3. [FastAPI](https://fastapi.tiangolo.com/) - веб-фреймворк для создания веб-приложений
4. [GitHub Actions](https://docs.github.com/ru/actions) - для реализации CI

Сервис запускается с помощью Docker контейнеров, тем самым реализуя в проекте микросервисную архитектуру. Сервисы связаны между собой с помощью docker compose.

У API есть версионирование, которое позволяет менять API без ущерба для конечных пользователей.

### Подготовка к запуску "Обогащение данных о рисках по ИНН"

1. Для работы сервиса у Вас должен быть установлен [Python](https://www.python.org/) на локальной машине и [Docker](https://www.docker.com/)

2. В корневой директории проекта создайте файл `.env` и скопируйте в него содержимое файла [.env.example](https://github.com/brivazz/legpromRF_tz/blob/main/.env.example) или переименуйте его в .env

3. [Опционально] Находясь в корневой директории проекта в терминале введите команду `python3 -m venv venv`, тем самым будет создано виртуальное окружение для установки и изоляции необходимых для проекта зависимостей

4. [Опционально] Активируйте созданное на предыдущем этапе вируальное окружение командой `source venv/bin/activate`

5. [Опционально] команда `make env` установит необходимые зависимости для профилирования кода, указанные в файле [requirements.txt](https://github.com/brivazz/legpromRF_tz/blob/main/requirements.txt)

# Запуск

В проекте предусмотрен Makefile для удобства запуска проекта.

Для запуска проекта достаточно:

1. Команда `make start` запустит docker-compose и сервис будет доступен для запросов по адресу: <http://127.0.0.1:80/api/v1/{inn}>
   - Веб-сервер Nignx будет проксировать запросы на 8000 порт приложения. Приложение также доступно на этом порту.
   - Данные будут выведены на небольшом html.
   - Документация OpenAPI (документация в формате Swаggеr) проекта, доступна по адресу: <http://127.0.0.1:80/api/openapi> с помощью которой, есть возможность вручную ввести данные на вход приложению.
   - Также для удобства просмотра коллекций с данными, хранящимися в базе данных MongoDB, в проекте присутствует интерактивный и легковесный веб-инструмент [mongo-express](https://github.com/mongo-express/mongo-express) для эффективного управления базами данных MongoDB, который доступен по адресу <http://127.0.0.1:8081>

# Остановка

Команда `make stop` остановит и удалит все контейнеры, вместе со всеми созданными файлами(volumes).
