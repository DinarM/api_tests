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
        'employee_company_1': {
            'username': 'QA_user_1_div_1',
            'password': 'x1210Lozcw0yEwxYuyjg',
        },
        'employee_2_company_1': {
            'username': 'QA_user_2_div_1',
            'password': 'g5dsLfRVu6EAf5WEl3h3',
        },
        'head_of_division_company_1': {
            'username': 'QA_head_of_div_1',
            'password': 'R5YDvyMJeDYI88cpRFe0',
        },
        'head_of_company_company_1': {
            'username': 'QA_head_of_company',
            'password': 'XgdcDzc5oj0owLN2pAti',
        },
        'super_admin': {'username': 'aqa_admin', 'password': 'q1w2e3r4T%'},
        'standalone_user': {'username': 'dinar_test', 'password': 'q1w2e3r4T%'},
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
        role: Роль пользователя (employee, head, ceo)

    Returns:
        dict: креды с ключами username и password
    """
    env = env or CURRENT_ENV
    if env not in CREDENTIALS:
        raise ValueError(f'Нет кредов для окружения {env}')
    if role not in CREDENTIALS[env]:
        raise ValueError(f'Нет кредов для роли {role} в окружении {env}')
    return CREDENTIALS[env][role]
