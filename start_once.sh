#!/bin/bash
set -e  # Прерывает выполнение при любой ошибке
echo "DATABASE_URL=$DATABASE_URL"
env  # покажет все переменные окружения

echo "🔥 Переменные окружения:"
printenv | grep DATABASE

echo "🚀 Применяем миграции..."
python3 manage.py migrate

echo "👤 Проверяем наличие суперпользователя..."
python << END
from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    print("✅ Суперпользователь не найден. Создаём...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("ℹ️ Суперпользователь уже существует.")
END

echo "✅ Готово! Запускаем сервер..."
exec gunicorn komunalka.wsgi:application
