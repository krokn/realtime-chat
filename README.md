# Сервис обмена мгновенными сообщениями

## Описание
Это простой сервис для обмена мгновенными сообщениями в реальном времени между пользователями. Он поддерживает регистрацию, аутентификацию, отправку сообщений, хранение истории переписки, а также уведомления через Telegram-бота для пользователей, которые находятся в офлайне.

## Технологии
- **Backend**: FastAPI (Python 3.12)
- **Database**: Postgres 16, Redis
- **ORM**: SQLAlchemy, Alembic (для миграций)
- **WebSockets**: Для обмена сообщениями в реальном времени
- **Celery**: Для обработки фоновых задач (уведомления через Telegram, сохранение сообщений)
- **Telegram Bot**: Aiogram
- **Docker**: Контейнеризация
- **Nginx**: Обратное проксирование

## Функциональность
### 1. Регистрация и аутентификация пользователей
- Регистрация и Авторизация пользователей.
- Аутентификация через токены.

### 2. Отправка и получение сообщений
- Пользователи могут отправлять и получать сообщения в реальном времени с использованием WebSockets.

### 3. Сохранение истории сообщений
- Сообщения сохраняются в базе данных.
- Возможность просмотра истории переписки, при попощи Swagger.

### 4. Уведомления через Telegram-бота
- Telegram-бот сообщает его ID и уведомляет пользователя о новых сообщениях, если тот находится в офлайне.

### 5. Веб-интерфейс для тестирования
- Простой веб-интерфейс для взаимодействия с сервисом находится по адресу https://github.com/krokn/realtime-chat-front.
- Поддержка регистрации, входа и отправки сообщений.

## Запуск проекта

### Шаги по запуску с Docker:
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/krokn/realtime-chat

2. В корне проекта создать файл .env пример:
   ```bash
   DB_HOST=postgres
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=user
   DB_PASS=123
   BOT_TOKEN=токен телеграмм бота
   ```

3. Создание Виртуального Окружения:
    ```bash
    python -m venv venv

4. Активация Виртуального Окружения CMD:
    ```bash
    venv\Scripts\activate.bat

5. Активация Виртуального Окружения PowerShell:
    ```bash
    .\venv\Scripts\Activate.ps1
   
6. Запуск docker-compose файла:
    ```bash
    docker-compose up --build -d
   
7. Поиск ID контейнера FastAPI для проведения миграции (ID нужно скопировать)
    ```bash
    docker ps
   
8. Проваливаемся в контейнер FastAPI
    ```bash
    docker exec -it id контейнера fastapi bash

9. Запускаем миграции alembic
   ```bash
    alembic upgrade head
    exit