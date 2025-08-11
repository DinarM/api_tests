"""
Конфигурационный файл для API тестов
"""

# Базовые URL для разных окружений
ENVIRONMENTS = {
    'stage': 'https://test.plastilindev.ru',
}

CURRENT_ENV = 'stage'


def get_base_url(env=None):
    """
    Получение базового URL для окружения

    Args:
        env: Окружение (если None, используется CURRENT_ENV)

    Returns:
        str: Базовый URL
    """
    env = env or CURRENT_ENV
    if env not in ENVIRONMENTS:
        raise ValueError(f'Окружение {env} не найдено')
    return ENVIRONMENTS[env]


CREDENTIALS = {
    'stage': {
        'company_1': {
            'head_of_company': {
                'username': 'QA_head_of_company',
                'password': 'XgdcDzc5oj0owLN2pAti',
            },
            'division_1': {
                'employee_1': {
                    'username': 'QA_user_1_div_1',
                    'password': 'x1210Lozcw0yEwxYuyjg',
                },
                'employee_2': {
                    'username': 'QA_user_2_div_1',
                    'password': 'g5dsLfRVu6EAf5WEl3h3',
                },
                'head_of_division': {
                    'username': 'QA_head_of_div_1',
                    'password': 'R5YDvyMJeDYI88cpRFe0',
                },
            },
            'division_2': {
                'employee_1': {
                    'username': 'QA_user_1_div_2',
                    'password': 'hrV3V4BbpBrPkKxgzERe',
                },
                'head_of_division': {
                    'username': 'QA_head_of_div_2',
                    'password': 'AEHIX3VaVzCKHr6Ig37z',
                },
            },
        },
        'other': {
            'super_admin': {'username': 'aqa_admin', 'password': 'q1w2e3r4T%'},
            'standalone_user': {'username': 'dinar_test', 'password': 'q1w2e3r4T%'},
        }
    },
    'dev': {
        'employee': {'username': 'employee_dev', 'password': 'employee_pass'},
        'head': {'username': 'head_dev', 'password': 'head_pass'},
        'ceo': {'username': 'ceo_dev', 'password': 'ceo_pass'},
    },
    # Добавляйте другие окружения по необходимости
}


def get_credentials(env=None, role='employee'):
    """
    Получение кредов для окружения и роли

    Args:
        env: Окружение (если None, используется CURRENT_ENV)
        role: Роль пользователя (может быть простой строкой или путем через точку, например: 'other.super_admin' или 'company_1.head_of_company')

    Returns:
        dict: креды с ключами username и password
    """
    env = env or CURRENT_ENV
    if env not in CREDENTIALS:
        raise ValueError(f'Нет кредов для окружения {env}')
    
    # Разбиваем роль на части по точкам
    role_parts = role.split('.')
    
    # Начинаем с уровня окружения
    current_level = CREDENTIALS[env]
    
    # Проходим по всем частям пути
    for part in role_parts:
        if part not in current_level:
            raise ValueError(f'Нет кредов для роли {role} в окружении {env}')
        current_level = current_level[part]
    
    return current_level
