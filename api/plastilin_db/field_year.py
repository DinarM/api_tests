from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class FieldYearAPI(BaseAPI):
    def get_field_year(self, token: str, spec_id: int) -> APIResponse:
        """
        Получение field_year по spec_id через GET-запрос
        Args:
            token: Bearer токен
            spec_id: ID спецификации
        Returns:
            dict: Ответ сервера
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {'spec_id': spec_id}
        return self.context.get(
            API_ENDPOINTS['plastilin_db']['field_year'], headers=headers, params=params
        )
