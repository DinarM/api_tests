from api.base_api import BaseAPI
from typing import Dict
from utils.api.constants import API_ENDPOINTS

class FieldYearAddApi(BaseAPI):
    def add_field_year(self, token: str, field_id: int, year: int, spec_id: int) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'field_id': field_id,
            'year': year,
            'spec_id': spec_id,
        }
        return self.context.post(API_ENDPOINTS['plastilin_db']['field_year_add'], headers=headers, data=payload)