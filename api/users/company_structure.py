from api.base_api import BaseAPI
from typing import Dict
from utils.api.constants import API_ENDPOINTS

class CompanyStructureApi(BaseAPI):
    def get_company_structure(self, token: str, is_active: bool = True) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['company_structure'], headers=headers, params={'is_active': is_active})