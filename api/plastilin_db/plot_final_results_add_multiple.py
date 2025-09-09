from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class PlotFinalResultsAddMultipleAPI(BaseAPI):
    def plot_final_results_add_multiple(
        self, 
        token: str, 
        plot: Optional[int] = None, 
        feature: Optional[str] = None, 
        unit: Optional[str] = None, 
        value: Optional[str] = None, 
        year_id: Optional[int] = None
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        payload = {
            'results': [{
                'plot': plot,
                'feature': feature,
                'unit': unit,
                'value': value,
                'year_id': year_id,
            }]
        }

        payload = APIHelper.filter_none_values(payload)

        return self.context.post(
            API_ENDPOINTS['plastilin_db']['plot_final_results_add_multiple'],
            data=payload,
            headers=headers,
        )