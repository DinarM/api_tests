from api.base_api import BaseAPI
from typing import Dict
from utils.api.constants import API_ENDPOINTS


class UsersByCompanyIdApi(BaseAPI):
    def get_users_by_company_id(self, company_id: int, token: str) -> Dict:
        """
        Получение списка пользователей по ID компании
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['users_by_company_id'], params={'company_id': company_id}, headers=headers)
