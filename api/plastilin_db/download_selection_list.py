from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class DownloadSelectionListAPI(BaseAPI):
    def download_selection_list(self, token: str, field_id: str, type_of_file: int, year_id: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        payload = {
            'field_id': field_id,
            'type_of_file': type_of_file,
            'year_id': year_id,
        }

        return self.context.post(
            API_ENDPOINTS['plastilin_db']['download_selection_list'],
            headers=headers,
            data=payload,
        )