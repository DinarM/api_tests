from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class ProfileApi(BaseAPI):
    def get_profile(self, token: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['profile'], headers=headers)
