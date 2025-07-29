from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class UsersGroupsApi(BaseAPI):
    def create_users_groups(
        self,
        token: str,
        name: str,
        read: Optional[bool] = None,
        write: Optional[bool] = None,
        add_yourself: Optional[bool] = None,
        user_ids: Optional[list[int]] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'name': name,
            'read': read,
            'write': write,
            'add_yourself': add_yourself,
            'user_ids': user_ids,
        }

        payload = APIHelper.filter_none_values(payload)

        return self.context.post(
            API_ENDPOINTS['users']['users_groups'], headers=headers, data=payload
        )

    def get_users_groups(
        self,
        token: str,
        name: Optional[str] = None,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company_name: Optional[str] = None,
        creator_id: Optional[int] = None,
        ordering: Optional[str] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        params = {
            'name': name,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'company_name': company_name,
            'creator_id': creator_id,
            'ordering': ordering,
        }
        params = APIHelper.filter_none_values(params)
        return self.context.get(API_ENDPOINTS['users']['users_groups'], headers=headers, params=params)

    def get_users_group_by_id(self, token: str, group_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(
            API_ENDPOINTS['users']['users_groups'] + f'{group_id}/', headers=headers
        )

    def update_users_group(
        self,
        token: str,
        group_id: int,
        name: str,
        read: Optional[bool] = None,
        write: Optional[bool] = None,
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {'name': name, 'read': read, 'write': write}
        payload = APIHelper.filter_none_values(payload)

        return self.context.put(
            API_ENDPOINTS['users']['users_groups'] + f'{group_id}/', headers=headers, data=payload
        )

    def delete_users_group(self, token: str, group_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.delete(
            API_ENDPOINTS['users']['users_groups'] + f'{group_id}/', headers=headers
        )

    def invite_user_to_group(
        self,
        token: str,
        user_group_id: int,
        user_ids: list[int],
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {'user_group_id': user_group_id, 'user_ids': user_ids}
        return self.context.post(
            API_ENDPOINTS['users']['users_groups'] + 'invite/', headers=headers, data=payload
        )
