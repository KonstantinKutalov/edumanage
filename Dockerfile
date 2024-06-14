FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV STATIC_ROOT=/app/staticfiles
ENV PATH="/usr/local/bin:${PATH}"

RUN apt-get update -qq && apt-get install -y libpq-dev

RUN python manage.py collectstatic --no-input
