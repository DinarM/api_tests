from api.base_api import BaseAPI
from typing import Dict
from utils.api.constants import API_ENDPOINTS

class FieldTableApi(BaseAPI):
    def get_field_table(self, token: str, spec_id: int) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['plastilin_db']['field_table'], headers=headers, params={'spec_id': spec_id})

    def create_field_table(self, token: str, spec_id: int, field_name: str, region: str) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'spec_id': spec_id,
            'field_name': field_name,
            'region': region
        }
        return self.context.post(API_ENDPOINTS['plastilin_db']['field_table'], headers=headers, data=payload)