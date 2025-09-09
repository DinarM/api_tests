from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class F1AnalyzeAPI(BaseAPI):
    def f1_analyze(self, token: str, year_id: str, feature: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
            'feature': feature,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['f1_analyze'],
            headers=headers,
            params=params,
        )