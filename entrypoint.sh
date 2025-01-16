#!/bin/bash

# Wait for Postgres to start
echo "Esperando a PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL iniciado"

# Execute migrations
python manage.py migrate

# Load initial data
python manage.py loaddata initial_data.json

# Create superuser
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
END

# Start server
python manage.py runserver 0.0.0.0:8000
