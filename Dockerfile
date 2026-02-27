FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PORT=8000
EXPOSE $PORT

# Render provides a dynamic PORT; bind Gunicorn to it.
CMD ["sh", "-c", "gunicorn coaching_system_be.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
