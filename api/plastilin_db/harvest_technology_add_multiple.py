from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class HarvestTechnologyAddMultipleAPI(BaseAPI):
    def harvest_technology_add_multiple(
        self, 
        token: str, 
        plot: Optional[int] = None, 
        feature: Optional[str] = None, 
        date_planned: Optional[str] = None, 
        date_real: Optional[str] = None, 
        comment: Optional[str] = None
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        payload = {
            'harvest_technologies': [
                {
                    'plot': plot,
                    'feature': feature,
                    'date_planned': date_planned,
                    'date_real': date_real,
                    'comment': comment
                }
            ]
        }

        payload = APIHelper.filter_none_values(payload)

        return self.context.post(
            API_ENDPOINTS['plastilin_db']['harvest_technology_add_multiple'],
            data=payload,
            headers=headers,
        )