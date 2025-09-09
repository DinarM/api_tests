from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class QualitativeFeaturesAPI(BaseAPI):
    def qualitative_features(self, token: str, year_id: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['qualitative_features'],
            headers=headers,
            params=params,
        )
