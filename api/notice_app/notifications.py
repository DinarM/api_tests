from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class NotificationsApi(BaseAPI):
    """API для работы с уведомлениями"""

    def get_notifications(self, token: str, status__neq: str = 'pending') -> APIResponse:
        """Получить уведомления"""
        headers = self.headers.copy()
        headers['Authorization'] = token
        
        params = {'status__neq': status__neq}

        return self.context.get(
            API_ENDPOINTS['notice_app']['notifications'],
            headers=headers,
            params=params,
        )