FROM python:3

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install celery

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=config.settings
