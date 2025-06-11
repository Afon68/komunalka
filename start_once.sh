#!/usr/bin/env bash
set -e

echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt

echo "🎯 Собираем статику..."
python manage.py collectstatic --no-input
echo "✅ Статика собрана"

echo "🚀 Применяем миграции..."
python manage.py migrate

echo "👤 Проверяем наличие суперпользователя..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
email = 'admin@example.com'
password = 'admin123'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Суперпользователь создан")
else:
    print("ℹ️ Суперпользователь уже существует")
END

echo "✅ Всё готово, можно запускать gunicorn"
