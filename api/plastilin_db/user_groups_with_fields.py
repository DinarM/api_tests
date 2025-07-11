from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class UserGroupsWithFieldsApi(BaseAPI):
    def get_user_groups_with_fields(
        self,
        token: str,
        user_group_id: Optional[int] = None,
        user_group_name: Optional[str] = None,
        user_group_read: Optional[bool] = None,
        user_group_write: Optional[bool] = None,
        user_group_creator_id: Optional[int] = None,
        field_id: Optional[int] = None,
        field_name: Optional[str] = None,
        year_id: Optional[int] = None,
        year: Optional[str] = None,
        spec_id: Optional[int] = None,
        users_user_id: Optional[int] = None,
        users_username: Optional[str] = None,
        users_company_id: Optional[int] = None,
        users_company_name: Optional[str] = None,
        ordering: Optional[str] = None,
        ordering_by_users: Optional[str] = None,
        ordering_by_fields: Optional[str] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {
            'user_group_id': user_group_id,
            'user_group_name': user_group_name,
            'user_group_read': user_group_read,
            'user_group_write': user_group_write,
            'user_group_creator_id': user_group_creator_id,
            'field_id': field_id,
            'field_name': field_name,
            'year_id': year_id,
            'year': year,
            'spec_id': spec_id,
            'users_user_id': users_user_id,
            'users_username': users_username,
            'users_company_id': users_company_id,
            'users_company_name': users_company_name,
            'ordering': ordering,
            'ordering_by_users': ordering_by_users,
            'ordering_by_fields': ordering_by_fields,
        }

        params = APIHelper.filter_none_values(params)

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['user_groups_with_fields'],
            headers=headers,
            params=params,
        )
