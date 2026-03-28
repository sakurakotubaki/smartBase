#!/bin/bash
set -e

echo "Waiting for database..."
sleep 2

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print('Superuser created: admin / adminpass')
else:
    print('Superuser already exists')
EOF

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting development server..."
exec python manage.py runserver 0.0.0.0:8000
