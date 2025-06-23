from api.base_api import BaseAPI
import uuid

class DispatcherJobsAPI(BaseAPI):
    def get_jobs_list(self, token: str, allowed_states: list = None, page_size: int = 50, 
                     current_page: int = 1, warehouses: list = None, team_ids: list = None):
        """
        Получение списка заданий
        
        Args:
            token: Токен для авторизации
            allowed_states: Список разрешенных статусов
            page_size: Размер страницы
            current_page: Текущая страница
            warehouses: Список складов
            team_ids: Список ID команд
        """
        payload = {
            'allowedStates': allowed_states or [],
            'page': {
                'size': page_size,
                'current': current_page
            }
        }
        
        if warehouses:
            payload['warehouses'] = warehouses
            
        if team_ids:
            payload['teamIds'] = team_ids

        headers = self.headers.copy()
        headers['Authorization'] = token

        response = self.context.post('url', 
                                   data=payload, 
                                   headers=headers)
        return response.json()

    def get_map_pins(self, token: str, allowed_states: list = [], page_size: int = 10000,
                    current_page: int = 1, warehouse_ids: list = None, team_ids: list = None):
        """
        Получение маркеров на карте
        
        Args:
            token: Токен для авторизации
            allowed_states: Список разрешенных статусов
            page_size: Размер страницы
            current_page: Текущая страница
            warehouse_ids: Список ID складов
            team_ids: Список ID команд
        """
        payload = {
            'allowedStates': allowed_states or ['UNASSIGNED', 'ASSIGNED', 'IN_PROGRESS'],
            'page': {
                'size': page_size,
                'current': current_page
            }
        }
        
        if warehouse_ids:
            payload['warehouseIds'] = warehouse_ids
            
        if team_ids:
            payload['teamIds'] = team_ids

        headers = self.headers.copy()
        headers['Authorization'] = token

        response = self.context.post('url',
                                   data=payload,
                                   headers=headers)
        return response

