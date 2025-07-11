import pytest
from playwright.sync_api import sync_playwright

from api.plastilin_db.plastilin_db_api import PlastilinDbApi
from api.users.users_api import UsersApi
from config import get_base_url, get_credentials
from utils.api.api_helpers import APIHelper, NullValue
from utils.api.constants import API_ENDPOINTS
from utils.api.data_helpers import DataHelper


def pytest_addoption(parser):
    """
    Добавление параметров командной строки для pytest
    """
    parser.addoption(
        '--env', action='store', default='stage', help='Окружение для тестов (stage, dev, prod)'
    )


@pytest.fixture(scope='session')
def env(request):
    """
    Фикстура для получения текущего окружения
    """
    return request.config.getoption('--env')


@pytest.fixture(scope='session')
def api_context(env):
    playwright = sync_playwright().start()
    context = playwright.request.new_context(
        base_url=get_base_url(env), extra_http_headers={'Content-Type': 'application/json'}
    )
    yield context
    context.dispose()
    playwright.stop()


@pytest.fixture
def plastilin_db_api(api_context):
    return PlastilinDbApi(api_context)


@pytest.fixture
def users_api(api_context):
    return UsersApi(api_context)


@pytest.fixture
def get_token(api_context, env):
    def _get_token(role='standalone_user'):
        try:
            creds = get_credentials(env, role)
        except Exception as e:
            pytest.skip(f'Роль {role} недоступна: {e}')
        payload = {'username': creds['username'], 'password': creds['password']}
        headers = {'Content-Type': 'application/json'}
        response = api_context.post(API_ENDPOINTS['auth']['login'], data=payload, headers=headers)
        try:
            response_data = response.json()
        except Exception:
            print('Ошибка авторизации! Ответ сервера:')
            print(response.text())
            raise
        return f'Bearer {response_data["access"]}'

    return _get_token


@pytest.fixture
def schema_validator():
    """
    Фикстура для валидации JSON по схеме
    """
    from schemas.validation import SchemaValidator

    return SchemaValidator()


@pytest.fixture
def data_helper(plastilin_db_api, users_api):
    """
    Фикстура для работы с данными
    """
    return DataHelper(plastilin_db_api, users_api)


@pytest.fixture
def api_helper():
    """
    Фикстура для API хелперов
    """
    return APIHelper()


@pytest.fixture
def null_value():
    """
    Фикстура для создания NullValue объекта для явного указания null в API запросах

    Пример использования:
    api.create_field_year_permissions(
        token=token,
        year_id=123,
        name=null_value(),  # Передаст {"name": null}
        read=null_value()   # Передаст {"read": null}
    )
    """
    return NullValue()
