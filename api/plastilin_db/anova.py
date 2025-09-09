from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class AnovaAPI(BaseAPI):
    def anova(self, token: str, year_id: str, dependent_var: str, group_vars: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'year_id': year_id,
            'dependent_var': dependent_var,
            'group_vars': group_vars,
        }

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['anova'],
            headers=headers,
            params=params,
        )