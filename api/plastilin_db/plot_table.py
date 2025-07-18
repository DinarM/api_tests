from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class PlotTableAPI(BaseAPI):
    def create_plot_table(
        self,
        token: str,
        plot_name: str,
        field: int,
        year: int,
        spec_id: int,
        line_name: str,
        comment: Optional[str] = None,
        mother: Optional[str] = None,
        father: Optional[str] = None,
        repetitions: Optional[int] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            "plot_name": plot_name,
            "field": field,
            "year": year,
            "spec_id": spec_id,
            "line_name": line_name,
            "comment": comment,
            "mother": mother,
            "father": father,
            "repetitions": repetitions,
        }
        payload = APIHelper.filter_none_values(payload)
        return self.context.post(
            API_ENDPOINTS['plastilin_db']['plot_table'],
            data=payload,
            headers=headers,
        )