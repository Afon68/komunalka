#!/usr/bin/env bash



echo "📦 Собираем статику..."
pip install -r requirements.txt
python manage.py collectstatic --noinput

