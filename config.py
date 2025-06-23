"""
Конфигурационный файл для API тестов
"""

# Базовые URL для разных окружений
ENVIRONMENTS = {
    'stage': 'domain',
    'dev': 'domain',
    'testing': 'domain'
}

# Конфигурация компаний
COMPANIES = {
    'CD': {
        'testing': {
            'warehouses': ['VAN1', 'VAN2'],
            'teams': ['267068b0-1b5c-4255-832a-96d42c42c1ee'],
            'zones': ['zone1', 'zone2']
        },
        'stage': {
            'warehouses': ['DEV_VAN1'],
            'teams': ['dev_team_id'],
            'zones': ['dev_zone1']
        }
    },
}

# Токены для разных ролей и окружений
TOKENS = {
    'stage': {
        'admin': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',  # Токен админа
        'dispatcher': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',  # Токен диспетчера
        'courier': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',  # Токен курьера
    },
    'dev': {
        'admin': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',
        'dispatcher': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',
        'courier': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',
    },
    'prod': {
        'admin': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',
        'dispatcher': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',
        'courier': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...',
    }
}

CURRENT_ENV = 'stage'
CURRENT_COMPANY = 'CD'

def get_company_config(company=None, env=None):
    """
    Получение конфигурации для компании и окружения
    
    Args:
        company: Название компании (если None, используется CURRENT_COMPANY)
        env: Окружение (если None, используется CURRENT_ENV)
    
    Returns:
        dict: Конфигурация компании
    """
    company = company or CURRENT_COMPANY
    env = env or CURRENT_ENV
    
    if company not in COMPANIES:
        raise ValueError(f'Компания {company} не найдена в конфигурации')
        
    if env not in COMPANIES[company]:
        raise ValueError(f'Окружение {env} не найдено для компании {company}')
        
    return COMPANIES[company][env]

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