FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV STATIC_ROOT=/app/staticfiles
ENV PATH="/usr/local/bin:${PATH}"

# Устанавливаем libpq-dev для Postgres
RUN apt-get update -qq && apt-get install -y libpq-dev

# Собираем статические файлы
RUN python manage.py collectstatic --no-input

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]