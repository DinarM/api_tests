from api.base_api import BaseAPI
import uuid
from typing import Dict


class SpeciesTableAPI(BaseAPI):

    def get_species_table(self, token: str) -> Dict:
        """
        Получение species_table через GET-запрос
        Args:
            token: Bearer токен
        Returns:
            dict: Ответ сервера
        """
        headers = self.headers.copy()
        headers['Authorization'] = token
        return self.context.get('/api/v1/plastilin_db/species_table/', headers=headers)

    def create_species_table(
        self, 
        token: str, 
        english_name: str = f'Сulture_{uuid.uuid4().hex[:8]}', 
        russian_name: str = f'Культура_{uuid.uuid4().hex[:8]}'
        ) -> Dict:
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
        
        return self.context.post('/api/v1/plastilin_db/species_table/', data=payload, headers=headers)
