from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class UsersByCompanyIdApi(BaseAPI):
    def get_users_by_company_id(
        self,
        token: str,
        username: Optional[str] = None,
        role: Optional[str] = None,
        group_name: Optional[str] = None,
        ordering: Optional[str] = None,
        ordering_by_groups: Optional[str] = None,
    ) -> APIResponse:
        """
        Получение списка пользователей по ID компании
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {
            'username': username,
            'role': role,
            'group_name': group_name,
            'ordering': ordering,
            'ordering_by_groups': ordering_by_groups,
        }
        params = APIHelper.filter_none_values(params)
        return self.context.get(
            API_ENDPOINTS['users']['users_by_company_id'],
            headers=headers,
            params=params,
        )
