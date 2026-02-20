FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps needed by requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Required for Django logging (prevents crash)
RUN mkdir -p /app/restapi/log && touch /app/restapi/log/api.log

RUN python manage.py collectstatic --noinput || true

RUN python manage.py migrate --noinput || true

EXPOSE 8000

CMD [ "gunicorn", "django_rest_main.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3","--timeout", "120" ]

