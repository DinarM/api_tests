from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class PlotStageAPI(BaseAPI):
    def create_plot_stage(
        self, 
        token: str, 
        plot: Optional[int] = None, 
        stage_of_vegetation: Optional[str] = None, 
        date_of_stage: Optional[str] = None
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        payload = {
            'plot': plot,
            'stage_of_vegetation': stage_of_vegetation,
            'date_of_stage': date_of_stage,
        }

        payload = APIHelper.filter_none_values(payload)

        return self.context.post(
            API_ENDPOINTS['plastilin_db']['plot_stage'],
            headers=headers,
            data=payload,
        )