from api.base_api import BaseAPI
from typing import Optional
from utils.api.constants import API_ENDPOINTS
from utils.api.api_helpers import APIHelper
from playwright.sync_api import APIResponse

class SpeciesTableAPI(BaseAPI):

    def get_species_table(self, token: str) -> APIResponse:
        """
        Получение species_table через GET-запрос
        Args:
            token: Bearer токен
        Returns:
            dict: Ответ сервера
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get(API_ENDPOINTS['plastilin_db']['species_table'], headers=headers)

    def create_species_table(
        self, 
        token: str, 
        russian_name: str,
        english_name: Optional[str] = None, 
        ) -> APIResponse:
        """
        Создание записи в species_table через POST-запрос
        Args:
            token: Bearer токен
            spec_id: ID спецификации
            english_name: Английское название
            russian_name: Русское название
            species: Вид (опционально)
        Returns:
            dict: Ответ сервера
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        
        payload = {
            'english_name': english_name,
            'russian_name': russian_name
        }  

        payload = APIHelper.filter_none_values(payload)

        return self.context.post(API_ENDPOINTS['plastilin_db']['species_table'], data=payload, headers=headers)
