import uuid
from http import HTTPStatus
from typing import Optional, Tuple

from api.plastilin_db.plastilin_db_api import PlastilinDbApi
from api.users.users_api import UsersApi


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
        response = self.plastilin_db_api.get_species_table(token=token)

        if response.status != HTTPStatus.OK:
            raise Exception(f'Ошибка получения списка культур: {response.status}')

        data = response.json()
        species_list = data.get('data', [])

        for item in species_list:
            if item.get('russian_name') == russian_name:
                return item['spec_id']

        response = self.plastilin_db_api.create_species_table(
            token=token, russian_name=russian_name
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
        if response.status != HTTPStatus.OK:
            raise Exception(f'Ошибка получения списка компаний: {response.status}')
        return response.json().get('id')

    def generate_random_string(self, name: Optional[str] = None, length: int = 10) -> str:
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

    def get_or_create_year_id(
        self, token: str, year: int, spec_id: int, field_id: int, region: str
    ) -> Optional[int]:
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
            for year_data in data[year_key]:
                if year_data.get('field_id') == field_id:
                    return year_data.get('year_id')

        response = self.plastilin_db_api.add_field_year(
            token=token, year=year, spec_id=spec_id, field_id=field_id
        )

        if response.status == HTTPStatus.CREATED:
            created_data = response.json()
            return created_data.get('id')
        else:
            raise Exception(f'Ошибка создания года: {response.status}')

    def get_or_create_field_id_by_name(
        self, token: str, spec_id: int, field_name: str, region: str
    ) -> Optional[int]:
        """
        Получает ID питомника для текущего пользователя
        """
        if not token or not spec_id or not field_name:
            raise ValueError('Token, spec_id и field_name обязательны')

        response = self.plastilin_db_api.get_field_table(token=token, spec_id=spec_id)

        if response.status != HTTPStatus.OK:
            raise Exception(f'Ошибка получения списка полей: {response.status}')

        data = response.json()
        field_list = data

        for item in field_list:
            if item.get('field_name') == field_name and item.get('region') == region:
                return item.get('field_id')

        response = self.plastilin_db_api.create_field_table(
            token=token, spec_id=spec_id, field_name=field_name, region=region
        )

        if response.status == HTTPStatus.OK:
            created_data = response.json()
            return created_data.get('field_id')
        else:
            raise Exception(f'Ошибка создания питомника: {response.status}')

    def get_or_create_spec_field_year_id(
        self, token: str, spec_name: str, field_name: str, year: int, region: str
    ) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        """
        Получает ID культуры, питомника и года для текущего пользователя
        """
        spec_id = self.get_or_create_spec_id_by_name(token=token, russian_name=spec_name)
        if spec_id is None:
            raise Exception(f'Не удалось получить или создать spec для имени {spec_name}')
        field_id = self.get_or_create_field_id_by_name(
            token=token, spec_id=spec_id, field_name=field_name, region=region
        )
        if field_id is None:
            raise Exception(f'Не удалось получить или создать field для имени {field_name}')
        year_id = self.get_or_create_year_id(
            token=token, year=year, spec_id=spec_id, field_id=field_id, region=region
        )
        if year_id is None:
            raise Exception(f'Не удалось получить или создать year для имени {year}')
        return spec_id, field_id, year_id

    @staticmethod
    def universal_sort_key(s, reverse=False):
        """
        Возвращает ключ для универсальной сортировки строк, чисел и None значений.
        Поддерживает естественную сортировку строк с цифрами.

        Args:
            s: Строка, число или None для сортировки
            reverse: Если True, None значения будут в начале, иначе в конце

        Returns:
            tuple: (буквенная_часть, числовая_часть) для сортировки
        """
        if s is None:
            if reverse:
                return ('', -999999)
            else:
                return ('zzzzzzzzzz', 999999)

        # Обрабатываем числовые значения
        if isinstance(s, (int, float)):
            return ('', s)

        # Нормализуем строку (заменяем ё на е)
        s_norm = s.replace('ё', 'е').replace('Ё', 'Е')

        # # Пока решили не использовать сортировку по цифрам в конце строки
        # m = re.match(r'(\D+?)(\d+)$', s_norm.strip())
        # if m:
        #     prefix, num = m.groups()
        #     num_val = int(num)
        #     if reverse:
        #         return (prefix.lower(), -num_val)
        #     else:
        #         return (prefix.lower(), num_val)

        return (s_norm.lower(), 0)

    def get_multiple_values_from_response(
        self, response_data: list, name_of_multiple: str, feature: str
    ) -> list:
        """
        Извлекает значения из ответа API для фильтрации multiple параметров

        Args:
            response_data: Данные ответа от API
            name_of_multiple: Название поля для извлечения
            feature: Название feature для поиска в features

        Returns:
            list: Список значений для проверки
        """
        if name_of_multiple in ['line_name', 'plot_name']:
            return [item[name_of_multiple] for item in response_data]
        else:
            return [
                next(
                    feat[name_of_multiple]
                    for feat in item['features']
                    if feat.get('feature') == feature
                )
                for item in response_data
            ]
