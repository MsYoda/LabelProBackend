# Базовый образ
FROM python:3.11-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV RUN_ENV=docker

# Установка рабочих директорий
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

# Копирование проекта
COPY . .

# Указание пути к статике
ENV DJANGO_SETTINGS_MODULE=label_pro.settings

# Сборка статики
RUN python manage.py collectstatic --noinput

RUN mkdir -p /app/local_data/

RUN chmod +x /app/docker_entrypoint.sh

# Открываем порт
EXPOSE 8000

ENTRYPOINT ["/app/docker_entrypoint.sh"]
# Запуск Gunicorn
CMD ["gunicorn", "label_pro.wsgi:application", "--bind", "0.0.0.0:8000"]
