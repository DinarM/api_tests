from typing import Dict

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class CompaniesApi(BaseAPI):
    def get_companies(self, token: str) -> Dict:
        """
        Получение списка компаний через GET-запрос
        Args:
            token: Bearer токен
        Returns:
            dict: Ответ сервера
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['companies'], headers=headers)
