from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class LoginApi(BaseAPI):
    """API для авторизации пользователя."""

    def login(self, username: str, password: str) -> APIResponse:
        return self.context.post(
            API_ENDPOINTS['auth']['login'],
            data={'username': username, 'password': password},
        )