from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class StatisticsVisualisationAPI(BaseAPI):
    def statistics_visualisation(self, token: str, year_id: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['statistics_visualisation'],
            headers=headers,
            params=params,
        )