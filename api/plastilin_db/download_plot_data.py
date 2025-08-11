from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class DownloadPlotDataAPI(BaseAPI):
    def download_plot_data(self, token: str, spec_id: int, year_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'spec_id': spec_id,
            'year_id': year_id,
        }

        return self.context.get(
            API_ENDPOINTS["plastilin_db"]["download_plot_data"],
            headers=headers,
            params=params,
        )