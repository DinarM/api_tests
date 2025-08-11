from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class ExportToExcelAPI(BaseAPI):
    def export_to_excel(self, token: str, field_id: str, year_id: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'field_id': field_id,
            'year_id': year_id,
        }

        return self.context.get(
            API_ENDPOINTS["plastilin_db"]["export_to_excel"],
            headers=headers,
            params=params,
        )