from api.base_api import BaseAPI
from playwright.sync_api import APIResponse
from utils.api.constants import API_ENDPOINTS

class CompanyStructureApi(BaseAPI):
    def get_company_structure(self, token: str, is_active: bool = True) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['company_structure'], headers=headers, params={'is_active': is_active})