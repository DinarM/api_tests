from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class CombinedPlotFieldLineGenealogyAPI(BaseAPI):
    def get_combined_plot_field_line_genealogy(
        self, token: str, year_id: int, page: int, page_size: int
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {
            'year_id': year_id,
            'page': page,
            'page_size': page_size,
        }
        return self.context.get(
            API_ENDPOINTS['plastilin_db']['combined_plot_field_line_genealogy'],
            params=params,
            headers=headers,
        )
