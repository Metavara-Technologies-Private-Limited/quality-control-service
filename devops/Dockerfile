FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/restapi/log \
    && touch /app/restapi/log/api.log

EXPOSE 8000

CMD ["gunicorn" , "django_rest_main.wsgi:application" , "--bind", "0.0.0.0:8000"]

