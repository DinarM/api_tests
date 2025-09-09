from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class CorrelationAPI(BaseAPI):
    def correlation(self, token: str, year_id: str, features: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
            'features': features,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['correlation'],
            headers=headers,
            params=params,
        )