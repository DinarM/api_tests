"""
Хелперы для работы с данными в тестах
"""
import uuid
from http import HTTPStatus
from typing import Dict, Optional, List
from api.plastilin_db.plastilin_db_api import PlastilinDbApi
from api.users.users_api import UsersApi
from utils.api.constants import REGIONS

class DataHelper:
    """
    Класс с полезными методами для работы с данными
    """
    
    def __init__(self, plastilin_db_api: PlastilinDbApi, users_api: UsersApi):
        self.plastilin_db_api = plastilin_db_api
        self.users_api = users_api

    def get_or_create_spec_id_by_name(self, token: str, russian_name: str) -> Optional[int]:
        """
        Ищет spec_id по русскому названию или создает новую запись
        
        Args:
            token: Bearer токен
            russian_name: Русское название для поиска
            
        Returns:
            int: spec_id если найден или создан, None если произошла ошибка
            
        Raises:
            Exception: При ошибке получения или создания культуры
        """
        if not token or not russian_name:
            raise ValueError('Token и russian_name обязательны')
        
        # Получаем список всех записей
        response = self.plastilin_db_api.get_species_table(token=token)
        
        if response.status != HTTPStatus.OK:
            raise Exception(f'Ошибка получения списка культур: {response.status}')
        
        data = response.json()
        species_list = data.get('data', [])
        
        # Ищем существующую запись
        for item in species_list:
            if item.get('russian_name') == russian_name:
                return item['spec_id']
        
        # Если не найдено, создаем новую запись
        response = self.plastilin_db_api.create_species_table(
            token=token, 
            russian_name=russian_name
        )
        
        if response.status == HTTPStatus.CREATED:
            created_data = response.json()
            return created_data['spec_id']
        else:
            raise Exception(f'Ошибка создания культуры: {response.status}')


    def get_my_company_id(self, token: str) -> Optional[int]:
        """
        Получает ID компании для текущего пользователя
        """
        response = self.users_api.get_company_structure(token=token)
        return response.json().get('id')

    def generate_random_string(self, name: str = None, length: int = 10) -> str:
        """
        Генерирует случайный строковый идентификатор
        """
        if name:
            return f'{name}_{str(uuid.uuid4())[:length]}'
        else:
            return str(uuid.uuid4())[:length]

    def get_user_id(self, token: str) -> Optional[int]:
        """
        Получает ID пользователя для текущего токена
        """
        response = self.users_api.get_profile(token=token)
        return response.json().get('user_data', {}).get('id')

    def get_or_create_year_id(self, token: str, year: int, spec_id: int, field_id: int) -> Optional[int]:
        """
        Получает ID года для текущего пользователя
        """
        if not token or not year or not spec_id:
            raise ValueError('Token, year и spec_id обязательны')
        
        response = self.plastilin_db_api.get_field_year(token=token, spec_id=spec_id)
        
        if response.status != HTTPStatus.OK:
            raise Exception(f'Ошибка получения списка полевых лет: {response.status}')
        
        data = response.json()

        year_key = str(year)
        if year_key in data:
            year_data = data[year_key][0]  
            return year_data.get('year_id')
        
        response = self.plastilin_db_api.add_field_year(token=token, year=year, spec_id=spec_id, field_id=field_id)

        if response.status == HTTPStatus.CREATED:
            created_data = response.json()
            return created_data.get('id')
        else:
            raise Exception(f'Ошибка создания года: {response.status}')

    def get_or_create_field_id_by_name(self, token: str, spec_id: int, field_name: str) -> Optional[int]:
        """
        Получает ID питомника для текущего пользователя
        """
        if not token or not spec_id or not field_name:
            raise ValueError('Token, spec_id и field_name обязательны')

        response = self.plastilin_db_api.get_field_table(token=token, spec_id=spec_id)
        
        if response.status != HTTPStatus.OK:
            raise Exception(f'Ошибка получения списка полей: {response.status}')
        
        data = response.json()
        field_list = data.get([])

        region = REGIONS['Амурская область']

        for item in field_list:
            if item.get('field_name') == field_name and item.get('region') == region:
                return item.get('field_id')
        
        response = self.plastilin_db_api.create_field_table(token=token, spec_id=spec_id, field_name=field_name, region=region)
        
        if response.status == HTTPStatus.OK:
            created_data = response.json()
            return created_data.get('field_id')
        else:
            raise Exception(f'Ошибка создания питомника: {response.status}')