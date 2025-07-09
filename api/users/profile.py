from api.base_api import BaseAPI
from typing import Dict
from utils.api.constants import API_ENDPOINTS

class ProfileApi(BaseAPI):
    def get_profile(self, token: str) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['profile'], headers=headers)