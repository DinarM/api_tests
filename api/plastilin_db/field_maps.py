from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class FieldMapsAPI(BaseAPI):
    def get_field_maps(self, token: str, year_id: int, field_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {
            'year_id': year_id,
            'field_id': field_id,
        }
        return self.context.get(
            API_ENDPOINTS['plastilin_db']['field_maps'],
            params=params,
            headers=headers,
        )
