from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class AncovaAPI(BaseAPI):
    def ancova(
        self, 
        token: str, 
        year_id: str, 
        dependent_var: str, 
        group_var: str, 
        covariate_var: str
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
            'dependent_var': dependent_var,
            'group_var': group_var,
            'covariate_var': covariate_var,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['ancova'],
            headers=headers,
            params=params,
        )