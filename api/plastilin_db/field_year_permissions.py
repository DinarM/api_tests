from api.base_api import BaseAPI
from typing import Dict, Optional
from utils.api.constants import API_ENDPOINTS
from utils.api.api_helpers import APIHelper
from playwright.sync_api import APIResponse


class FieldYearPermissionsApi(BaseAPI):

    def create_field_year_permissions(
        self, 
        token: str, 
        year_id: int, 
        user_group_id: Optional[int] = None, 
        name: Optional[str] = None, 
        read: Optional[bool] = None, 
        write: Optional[bool] = None
    ) -> APIResponse:
        """
        Создание разрешений для полевого года
        
        Args:
            token: Bearer токен
            year_id: ID года (обязательное)
            user_group_id: ID группы пользователей (None = не передавать, NullValue() = передать null)
            name: Название (None = не передавать, NullValue() = передать null)
            read: Право на чтение (None = не передавать, NullValue() = передать null)
            write: Право на запись (None = не передавать, NullValue() = передать null)
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        
        payload = {
            'year_id': year_id,
            'user_group_id': user_group_id,
            'name': name,
            'read': read,
            'write': write
        }
        payload = APIHelper.filter_none_values(payload)
            
        return self.context.post(API_ENDPOINTS['plastilin_db']['field_year_permissions'], headers=headers, data=payload)
    
    def get_field_year_permissions(self, token: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['plastilin_db']['field_year_permissions'], headers=headers)
    
    def get_field_year_permissions_by_id(self, token: str, field_year_permission_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['plastilin_db']['field_year_permissions'] + f'{field_year_permission_id}/', headers=headers)

    def update_field_year_permissions(self, token: str, field_year_permission_id: int, name: Optional[str] = None, read: Optional[bool] = None, write: Optional[bool] = None) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'name': name,
            'read': read,
            'write': write
        }
        payload = APIHelper.filter_none_values(payload)
        return self.context.put(API_ENDPOINTS['plastilin_db']['field_year_permissions'] + f'{field_year_permission_id}/', headers=headers, data=payload)

    def delete_field_year_permissions(self, token: str, field_year_permission_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.delete(API_ENDPOINTS['plastilin_db']['field_year_permissions'] + f'{field_year_permission_id}/', headers=headers)
    
    def add_user_to_field_year_permissions(self, token: str, field_year_permission_id: int, user_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        payload = {
            'user_id': user_id
        }
        return self.context.post(API_ENDPOINTS['plastilin_db']['field_year_permissions'] + f'{field_year_permission_id}/invite/', headers=headers, data=payload)