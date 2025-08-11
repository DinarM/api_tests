from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class DownloadFieldFileAPI(BaseAPI):
    def download_field_file(self, token: str, spec_id: str, year_id: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'spec_id': spec_id,
            'year_id': year_id,
        }

        return self.context.get(
            API_ENDPOINTS["plastilin_db"]["download_field_file"],
            headers=headers,
            params=params,
        )