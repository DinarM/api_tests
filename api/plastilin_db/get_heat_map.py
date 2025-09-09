from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class GetHeatMapAPI(BaseAPI):
    def get_heat_map(self, token: str, year_id: str, feature: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
            'feature': feature,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['get_heat_map'],
            headers=headers,
            params=params,
        )