from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class CalculateNSRMultipleAPI(BaseAPI):
    def get_calculate_nsr_multiple(
        self,
        token: str,
        year_ids: list[int],
        feature: str,
        control_plot: str,
        control_plot_year_id: int,
        sort_by: Optional[str] = None,
        sort_by__key: Optional[str] = None,
        sort_by__value: Optional[str] = None,
        name_of_multiple: Optional[str] = None,
        value_of_multiple: Optional[str] = None,
        filter_name: Optional[str] = None,
        filter_value: Optional[str] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {
            'year_ids': year_ids,
            'feature': feature,
            'control_plot': control_plot,
            'control_plot_year_id': control_plot_year_id,
            'sort_by': sort_by,
            f'sort_by__{sort_by__key}': sort_by__value,
            f'{name_of_multiple}_multiple': value_of_multiple,
            filter_name: filter_value,
        }

        params = APIHelper.filter_none_values(params)
        return self.context.get(
            API_ENDPOINTS['plastilin_db']['calculate_nsr_multiple'],
            params=params,
            headers=headers,
        )