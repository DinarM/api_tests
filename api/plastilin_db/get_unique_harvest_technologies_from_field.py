from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class GetUniqueHarvestTechnologiesFromFieldAPI(BaseAPI):
    def get_unique_harvest_technologies_from_field(self, token: str, year_id: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['get_unique_harvest_technologies_from_field'],
            headers=headers,
            params=params,
        )