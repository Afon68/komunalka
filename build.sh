#!/usr/bin/env bash
set -e  # Прерывает выполнение при ошибке

echo "📦 Собираем статику..."
pip install -r requirements.txt
echo "✅ Установлены зависимости"
python manage.py collectstatic --no-input
echo "✅ Собраны статические файлы"

