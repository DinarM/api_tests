from api.base_api import BaseAPI
import uuid

class DispatcherTeamAPI(BaseAPI):
    def create_team(self, name: str = None, external_id: str = None, warehouse_id: str = None, zone_ids: list = None, token: str = None):
        """
        Создает новую команду в системе.
        
        Args:
            name: Название команды
            external_id: Внешний идентификатор
            warehouse_id: ID склада
            zone_ids: Список ID зон
            token: Токен для авторизации (если не указан, используется токен из headers)
        """
        payload = {
            "name": name or f"AutoTeam_{uuid.uuid4().hex[:6]}",
            "externalId": external_id,
            "warehouseId": warehouse_id,
            "zoneIds": zone_ids or [],
        }

        headers = self.headers.copy()
        headers['Authorization'] = token

        response = self.context.post("url", data=payload, headers=headers)
        return response.json()