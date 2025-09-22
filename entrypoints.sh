#!/bin/sh
set -e

echo "▶️  Applying migrations..."
python manage.py migrate --noinput

echo "👤 Checking superuser (optional)"
python manage.py shell <<'PY'
from decouple import config
from django.contrib.auth import get_user_model
User = get_user_model()
phone = config('DJANGO_SUPERUSER_PHONE_NUMBER', default=None)
username = config('DJANGO_SUPERUSER_USERNAME', default=None)
pwd   = config('DJANGO_SUPERUSER_PASSWORD', default=None)
if phone and pwd and not User.objects.filter(phone_number=phone).exists():
    print(f"Creating superuser {phone}...")
    User.objects.create_superuser(phone_number=phone, password=pwd, username=username)
    print("Superuser created.")
else:
    print("Superuser exists or env not provided; skipping.")
PY

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2 \
    --timeout 120
