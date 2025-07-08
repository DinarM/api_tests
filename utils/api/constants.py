"""
Константы для тестов
"""

API_ENDPOINTS = {
    'auth': {
        'login': '/api/v1/login/'
    },
    'users': {
        'companies': '/api/v1/users/companies/',
        'users_by_company_id': '/api/v1/users/users_by_company_id/',
        'users_groups': '/api/v1/users/users_groups/',
        'company_structure': '/api/v1/users/company_structure/',
    },
    'plastilin_db': {
        'field_year': '/api/v1/plastilin_db/field_year/',
        'species_table': '/api/v1/plastilin_db/species_table/',
        'field_year_permissions': '/api/v1/plastilin_db/field_year_permissions/',
        'user_groups_with_fields': '/api/v1/plastilin_db/user_groups_with_fields/'
    },
}


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