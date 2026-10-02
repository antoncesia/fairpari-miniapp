#!/bin/sh
# Запуск бота локально: создаёт окружение, ставит зависимости, запускает.
# Токен — в bot/.env (BOT_TOKEN=...), файл в репозиторий не попадает.
set -e
cd "$(dirname "$0")"
[ -f .env ] || { echo "Нет bot/.env — скопируйте .env.example в .env и впишите BOT_TOKEN"; exit 1; }
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
exec .venv/bin/python bot.py
