# 💡 Komunalka App

Это веб-приложение для ведения и расчёта коммунальных платежей: учёт воды, газа, электричества и других услуг, включая абонплаты и счётчики.

## 🚀 Локальный запуск

### 1. Клонируй проект

```bash
git clone https://github.com/your_username/komunalka.git
cd komunalka
2. Создай виртуальное окружение

python -m venv venv
source venv/bin/activate

3. Установи зависимости
pip install -r requirements.txt

4. Настрой .env
Создай .env на основе .env.example:
cp .env.example .env
Впиши реальные значения (например, ключ, пароль БД и т.д.)

5. Примени миграции и запусти сервер

python manage.py migrate
python manage.py runserver
📦 Стек технологий
Python 3.12

Django 5.x

PostgreSQL

Bootstrap 5

Gunicorn (на проде)

Render (дeплой)

