import pytest
from playwright.sync_api import sync_playwright
from api.dispatcher.dispatcher_api import DispatcherAPI
from api.order.order_api import OrderAPI
from config import get_base_url, get_company_config

def pytest_addoption(parser):
    """
    Добавление параметров командной строки для pytest
    """
    parser.addoption(
        '--env',
        action='store',
        default='stage',
        help='Окружение для тестов (stage, dev, prod)'
    )
    parser.addoption(
        '--company',
        action='store',
        default='jiffy',
        help='Компания для тестов'
    )
    parser.addoption(
        '--token',
        action='store',
        help='Токен для авторизации'
    )

@pytest.fixture(scope='session')
def env(request):
    """
    Фикстура для получения текущего окружения
    """
    return request.config.getoption('--env')

@pytest.fixture(scope='session')
def company(request):
    """
    Фикстура для получения текущей компании
    """
    return request.config.getoption('--company')

@pytest.fixture(scope='session')
def company_config(env, company):
    """
    Фикстура для получения конфигурации компании
    """
    return get_company_config(company, env)


@pytest.fixture(scope='session')
def api_context(env):
    playwright = sync_playwright().start()
    context = playwright.request.new_context(
        base_url=get_base_url(env),
        extra_http_headers={
            'Content-Type': 'application/json'
        }
    )
    yield context
    context.dispose()
    playwright.stop()


@pytest.fixture
def dispatcher_api(api_context):
    return DispatcherAPI(api_context)

@pytest.fixture
def order_api(api_context):
    return OrderAPI(api_context)

@pytest.fixture
def get_token(api_context):
    """
    Фикстура, возвращающая функцию для получения токена
    
    Returns:
        function: Функция для получения токена
    """
    def _get_token(phone: str, code: str = '0000') -> str:
        """
        Подтверждение OTP кода и получение Bearer токена
        
        Args:
            phone: Номер телефона в формате +7XXXXXXXXXX
            code: Код подтверждения (по умолчанию '0000')
            
        Returns:
            str: Bearer токен для авторизации
        """
        payload = {
            'phone': phone,
            'code': code
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = api_context.post('/auth/v1/auth/otp/confirm',
                                    data=payload,
                                    headers=headers)
        
        response_data = response.json()
        print(response_data)
        return f"Bearer {response_data['data']['access_token']}"
    
    return _get_token

