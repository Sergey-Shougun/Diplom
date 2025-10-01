# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /app

# Установка зависимостей для PostgreSQL
RUN apk add --no-cache gcc musl-dev postgresql-dev linux-headers

# Копирование и установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода проекта
COPY . .

# Сборка статических файлов (для продакшена)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Запуск приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pereval_api.wsgi:application"]