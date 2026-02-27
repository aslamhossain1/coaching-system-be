## Render Deploy Guide (Backend)

### 1) Deploy Source

- Create a new **Web Service** on Render from this repo/folder: `coaching-system-be`
- Runtime: `Python`

### 2) Build & Start Command

- Build Command:
  - `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start Command:
  - `gunicorn coaching_system_be.wsgi:application --bind 0.0.0.0:$PORT`

### 3) Environment Variables

Set these in Render Web Service:

- `DJANGO_SECRET_KEY` = (generate strong random value)
- `DJANGO_DEBUG` = `False`
- `DJANGO_ALLOWED_HOSTS` = `.onrender.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS` = `https://edutrack-app-one.vercel.app`
- `CORS_ALLOWED_ORIGINS` = `https://edutrack-app-one.vercel.app`
- `SECURE_SSL_REDIRECT` = `True`
- `DATABASE_URL` = (attach Render PostgreSQL and use connection string)

### 4) Database

- Create Render PostgreSQL database
- Attach DB to web service (Render can auto-set `DATABASE_URL`)

### 5) Local Example

- Use `.env.example` as template for local `.env`
