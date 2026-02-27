FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PORT=8000
EXPOSE $PORT

# ASGI server for Django
CMD ["uvicorn", "coaching_system_be.asgi:application", "--host", "0.0.0.0", "--port", "8000"]