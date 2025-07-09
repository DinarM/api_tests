from api.base_api import BaseAPI
from typing import Dict, Optional
from utils.api.constants import API_ENDPOINTS
from utils.api.api_helpers import APIHelper


class UsersGroupsApi(BaseAPI):

    def create_users_groups(self, token: str, name: str, read: Optional[bool] = None, write: Optional[bool] = None) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'name': name,
            'read': read,
            'write': write
        }

        payload = APIHelper.filter_none_values(payload)

        return self.context.post(API_ENDPOINTS['users']['users_groups'], headers=headers, data=payload)

    def get_users_groups(self, token: str) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['users_groups'], headers=headers)
    
    def get_users_group_by_id(self, token: str, group_id: int) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['users']['users_groups'] + f'{group_id}/', headers=headers)

    def update_users_group(self, token: str, group_id: int, name: str, read: Optional[bool] = None, write: Optional[bool] = None) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'name': name,
            'read': read,
            'write': write
        }
        payload = APIHelper.filter_none_values(payload)

        return self.context.put(API_ENDPOINTS['users']['users_groups'] + f'{group_id}/', headers=headers, data=payload)
    
    def delete_users_group(self, token: str, group_id: int) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.delete(API_ENDPOINTS['users']['users_groups'] + f'{group_id}/', headers=headers)

    def invite_user_to_group(self, token: str, user_group_id: int, user_id: int) -> Dict:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'user_group_id': user_group_id,
            'user_id': user_id
        }
        return self.context.post(API_ENDPOINTS['users']['users_groups'] + 'invite/', headers=headers, data=payload)