from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class SowingListAPI(BaseAPI):
    def create_sowing_list(
        self,
        token: str,
        empty_columns: Optional[list] = None,
        field_id: Optional[int] = None,
        germination_date: Optional[str] = None,
        sowing_date: Optional[str] = None,
        type_of_file: Optional[str] = None,
        year_id: Optional[int] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'empty_columns': empty_columns,
            'field_id': field_id,
            'germination_date': germination_date,
            'sowing_date': sowing_date,
            'type_of_file': type_of_file,
            'year_id': year_id,
        }
        payload = APIHelper.filter_none_values(payload)

        return self.context.post(
            API_ENDPOINTS['plastilin_db']['sowing_list'],
            data=payload,
            headers=headers,
        )