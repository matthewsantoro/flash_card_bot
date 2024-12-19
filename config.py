# Инициализация базы данных
from os import getenv


DB_CONFIG = {
    'USER': getenv('DB_USER'),
    'PASSWORD': getenv('DB_PASSWORD'),
    'HOST': getenv('DB_HOST'),
    'PORT': getenv('DB_PORT'),
    'DATABASE': getenv('DB_DATABASE')
}

BOT_TOKEN=getenv("BOT_TOKEN")