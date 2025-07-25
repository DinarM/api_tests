from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class PlotTableAPI(BaseAPI):
    def create_plot_table(
        self,
        token: Optional[str] = None,
        plot_name: Optional[str] = None,
        field: Optional[int] = None,
        year: Optional[int] = None,
        spec_id: Optional[int] = None,
        line_name: Optional[str] = None,
        comment: Optional[str] = None,
        mother: Optional[str] = None,
        father: Optional[str] = None,
        repetitions: Optional[int] = None,
        width: Optional[int] = None,
        length: Optional[int] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        if token:
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
            "width": width,
            "length": length,
        }
        payload = APIHelper.filter_none_values(payload)
        return self.context.post(
            API_ENDPOINTS['plastilin_db']['plot_table'],
            data=payload,
            headers=headers,
        )