"""
Константы для тестов
"""

API_ENDPOINTS = {
    'auth': {'login': '/api/v1/login/'},
    'users': {
        'companies': '/api/v1/users/companies/',
        'users_by_company_id': '/api/v1/users/users_by_company_id/',
        'users_groups': '/api/v1/users/users_groups/',
        'company_structure': '/api/v1/users/company_structure/',
        'profile': '/api/v1/users/profile/',
    },
    'plastilin_db': {
        'field_year': '/api/v1/plastilin_db/field_year/',
        'species_table': '/api/v1/plastilin_db/species_table/',
        'field_year_permissions': '/api/v1/plastilin_db/field_year_permissions/',
        'user_groups_with_fields': '/api/v1/plastilin_db/user_groups_with_fields/',
        'field_year_add': '/api/v1/plastilin_db/field_year_add/',
        'field_table': '/api/v1/plastilin_db/field_table/',
        'perform_t_test_multiple': '/api/v1/plastilin_db/perform_t_test_multiple/',
    },
}

YEARS = {
    '2023': 2023,
    '2025': 2025,
    '2026': 2026,
}


# Тестовые данные
TEST_CULTURES = {
    'wheat': {'english_name': 'Wheat', 'russian_name': 'Пшеница'},
    'barley': {
        'english_name': 'Barley',
        'russian_name': 'Ячмень',  # для массива данных
    },
}

REGIONS = {
    'Амурская область': 'Амурская область',
    'Краснодарский край': 'Краснодарский край',
}

FIELDS = {
    'field_1': {
        'field_name': 'Тестовый питомник',
        'region': REGIONS['Амурская область'],
        'year': YEARS['2025'],
    },
    'field_2': {  # для массива данных
        'field_name': 'Конкурсный питомник',
        'region': REGIONS['Краснодарский край'],
        'year': YEARS['2023'],
    },
}


# Таймауты
TIMEOUTS = {'short': 5.0, 'medium': 15.0, 'long': 30.0}

# Статусы ответов
STATUS_CODES = {
    'ok': 200,
    'created': 201,
    'no_content': 204,
    'bad_request': 400,
    'unauthorized': 401,
    'not_found': 404,
    'server_error': 500,
}
