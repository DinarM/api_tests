"""
Константы для тестов
"""
from typing import Dict

# Тестовые данные
TEST_CULTURES = {
    'wheat': {
        'english_name': 'Wheat',
        'russian_name': 'Пшеница'
    },
    'corn': {
        'english_name': 'Corn',
        'russian_name': 'Кукуруза'
    },
    'soybean': {
        'english_name': 'Soybean',
        'russian_name': 'Соя'
    }
}

# Таймауты
TIMEOUTS = {
    'short': 5.0,
    'medium': 15.0,
    'long': 30.0
}

# Статусы ответов
STATUS_CODES = {
    'ok': 200,
    'created': 201,
    'no_content': 204,
    'bad_request': 400,
    'unauthorized': 401,
    'not_found': 404,
    'server_error': 500
}