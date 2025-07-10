from api.base_api import BaseAPI
from playwright.sync_api import APIResponse
from utils.api.constants import API_ENDPOINTS


class PerformTTestMultipleAPI(BaseAPI):
    def get_perform_t_test_multiple(self, token: str, year_ids: int, feature: str, control_plot: str, control_plot_year_id: int) -> APIResponse:
        """
        Получение perform_t_test_multiple по spec_id, field_id и year_id через GET-запрос
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {'year_ids': year_ids, 'feature': feature, 'control_plot': control_plot, 'control_plot_year_id': control_plot_year_id}
        return self.context.get(API_ENDPOINTS['plastilin_db']['perform_t_test_multiple'], headers=headers, params=params)
