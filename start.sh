#!/usr/bin/env bash
set -o errexit

echo "=== Rodando migrate ==="
python manage.py migrate --run-syncdb

echo "=== Criando superusuario ==="
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@cocheira.com', 'admin123')
    print('Superusuario admin criado.')
else:
    print('Superusuario ja existe.')
"

echo "=== Iniciando servidor ==="
gunicorn config.wsgi:application
