FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=config.settings

RUN python manage.py collectstatic --no-input

CMD ["celery", "-A", "config", "worker", "-l", "info"]