from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class PerformTTestMultipleAPI(BaseAPI):
    def get_perform_t_test_multiple(
        self,
        token: str,
        year_ids: int,
        feature: str,
        control_plot: str,
        control_plot_year_id: int,
        sort_by: Optional[str] = None,
        sort_by__key: Optional[str] = None,
        sort_by__value: Optional[str] = None,
        name_of_multiple: Optional[str] = None,
        value_of_multiple: Optional[str] = None,
    ) -> APIResponse:
        """
        Получение perform_t_test_multiple по spec_id, field_id и year_id через GET-запрос
        """
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
        }
        params = APIHelper.filter_none_values(params)
        return self.context.get(
            API_ENDPOINTS['plastilin_db']['perform_t_test_multiple'],
            headers=headers,
            params=params,
        )
