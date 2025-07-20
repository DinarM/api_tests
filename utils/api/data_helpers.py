import uuid
import tempfile
import string
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple, Dict, List, Any
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from http import HTTPStatus

from api.plastilin_db.plastilin_db_api import PlastilinDbApi
from api.users.users_api import UsersApi
from utils.api.constants import TEST_DATA_PATH


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

    
    def _generate_field_value(self, field_type: str) -> Any:
        """Генерирует случайное значение для поля по типу"""
        if field_type == 'float':
            return round(random.uniform(0, 100), 2)
        elif field_type == 'date':
            # Генерируем дату в рамках текущего года
            current_year = datetime.now().year
            start_date = datetime(current_year, 1, 1)
            end_date = datetime(current_year, 12, 31)
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            random_date = start_date + timedelta(days=random_days)
            return random_date.strftime('%Y-%m-%d')
        return self.generate_random_string('Тестовое значение', length=6)

    def generate_plot_result_api_data(
        self,
        field_name: str,
        year: int,
        region: str,
        base_plot_name: str,
        row_count: int = 10,
        repeats: int = 1,
        phenotypic_fields: Optional[List[Dict[str, str]]] = None,
        dev_stage_fields: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Генерирует данные для API в формате ключ-значение
        
        Args:
            field_name: Название питомника
            year: Год
            region: Регион
            base_plot_name: Базовое название делянки
            row_count: Количество записей на повторность
            repeats: Количество повторностей
            phenotypic_fields: [{'name': 'Высота растения', 'type': 'float', 'unit': 'см'}, ...]
            dev_stage_fields: [{'name': 'Развертывание первых листьев', 'type': 'date'}, ...]
            
        Returns:
            List[Dict] с данными в формате API
        """
        phenotypic_fields = phenotypic_fields or []
        dev_stage_fields = dev_stage_fields or []
        
        api_data = []
        
        for repeat in range(1, repeats + 1):
            for plot_num in range(1, row_count + 1):
                # Генерируем данные для одной записи
                plot_results = []
                for field in phenotypic_fields:
                    value = self._generate_field_value(field['type'])
                    plot_results.append({
                        "plot_final_feature": field['name'].lower(),
                        "plot_final_value": str(value),
                        "plot_final_unit": field.get('unit', '')
                    })
                
                plot_stages = []
                for field in dev_stage_fields:
                    value = self._generate_field_value(field['type'])
                    plot_stages.append({
                        "stage_of_vegetation": field['name'].lower(),
                        "date_of_stage": value
                    })
                
                # Формируем основную запись
                record = {
                    "plot_name": f"{base_plot_name} {plot_num}/{repeat}",
                    "line_name": f"Сорт {plot_num}",
                    "plot_results": plot_results,
                    "plot_stages": plot_stages
                }
                
                api_data.append(record)
        
        return api_data

    def generate_plot_result_data(
        self,
        field_name: str,
        year: int,
        region: str,
        base_plot_name: str,
        row_count: int = 10,
        repeats: int = 1,
        phenotypic_fields: Optional[List[Dict[str, str]]] = None,
        dev_stage_fields: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Генерирует данные для результатов делянок в двух форматах
        
        Args:
            field_name: Название питомника
            year: Год
            region: Регион
            base_plot_name: Базовое название делянки
            row_count: Количество записей на повторность
            repeats: Количество повторностей
            phenotypic_fields: [{'name': 'Высота растения', 'type': 'float', 'unit': 'см'}, ...]
            dev_stage_fields: [{'name': 'Развертывание первых листьев', 'type': 'date'}, ...]
            
        Returns:
            Dict с двумя форматами данных:
            {
                'excel': {
                    'headers': [...],
                    'data': [...],
                    'total_rows': 60,
                    'field_names': [...],
                    'dev_stage_names': [...],
                    'metadata': {...}
                },
                'api': [
                    {
                        'plot_name': 'Делянка 1/1',
                        'line_name': 'Сорт 1',
                        'plot_results': [...],
                        'plot_stages': [...]
                    },
                    ...
                ]
            }
        """
        phenotypic_fields = phenotypic_fields or []
        dev_stage_fields = dev_stage_fields or []
        
        # Формируем заголовки для Excel
        headers = ['Название питомника', 'Год', 'Регион', 'Название делянки', 'Название сорта', 'Номер повторности']
        
        # Формируем заголовки фенотипов
        phenotypic_names = []
        for field in phenotypic_fields:
            if field['type'] == 'float' and 'unit' in field:
                phenotypic_names.append(f"Фенотип;{field['name']}; {field['unit']}")
            else:
                phenotypic_names.append(f"Фенотип;{field['name']};")
        
        # Формируем заголовки стадий развития
        dev_stage_names = []
        for field in dev_stage_fields:
            dev_stage_names.append(f"Стадия развития;{field['name']};")
        
        headers.extend(phenotypic_names)
        headers.extend(dev_stage_names)
        
        # Генерируем данные для обоих форматов
        excel_data = []
        api_data = []
        
        for repeat in range(1, repeats + 1):
            for plot_num in range(1, row_count + 1):
                # Генерируем значения для текущей записи
                phenotypic_values = [self._generate_field_value(f['type']) for f in phenotypic_fields]
                dev_stage_values = [self._generate_field_value(f['type']) for f in dev_stage_fields]
                
                # Формируем строку для Excel
                excel_row = [
                    field_name,
                    year,
                    region,
                    f"{base_plot_name} {plot_num}",
                    f"Сорт {plot_num}",
                    repeat
                ]
                excel_row.extend(phenotypic_values)
                excel_row.extend(dev_stage_values)
                excel_data.append(excel_row)
                
                # Формируем данные для API
                plot_results = []
                for i, field in enumerate(phenotypic_fields):
                    plot_results.append({
                        "plot_final_feature": field['name'].lower(),
                        "plot_final_value": str(phenotypic_values[i]),
                        "plot_final_unit": field.get('unit', '')
                    })
                
                plot_stages = []
                for i, field in enumerate(dev_stage_fields):
                    plot_stages.append({
                        "stage_of_vegetation": field['name'].lower(),
                        "date_of_stage": dev_stage_values[i]
                    })
                
                api_record = {
                    "plot_name": f"{base_plot_name} {plot_num}/{repeat}",
                    "line_name": f"Сорт {plot_num}",
                    "plot_results": plot_results,
                    "plot_stages": plot_stages
                }
                api_data.append(api_record)

        print(api_data)
        
        return {
            'excel': {
                'headers': headers,
                'data': excel_data,
                'total_rows': len(excel_data),
                'field_names': phenotypic_names,
                'dev_stage_names': dev_stage_names,
                'metadata': {
                    'field_name': field_name,
                    'year': year,
                    'region': region,
                    'base_plot_name': base_plot_name,
                    'row_count': row_count,
                    'repeats': repeats
                }
            },
            'api': api_data
        }

    def create_plot_result_excel(
        self,
        plot_data: Optional[Dict[str, Any]] = None,
        field_name: Optional[str] = None,
        year: Optional[int] = None,
        region: Optional[str] = None,
        base_plot_name: Optional[str] = None,
        row_count: int = 10,
        repeats: int = 1,
        phenotypic_fields: Optional[List[Dict[str, str]]] = None,
        dev_stage_fields: Optional[List[Dict[str, str]]] = None,
    ) -> Tuple[Path, str]:
        """
        Создает Excel файл для результатов делянок
        
        Args:
            plot_data: Готовые данные (если None, генерируются автоматически)
            field_name, year, region, base_plot_name: Параметры для генерации данных
            row_count, repeats, phenotypic_fields, dev_stage_fields: Параметры для генерации
        """
        # Используем готовые данные или генерируем новые
        if plot_data is None:
            plot_data = self.generate_plot_result_data(
                field_name=field_name,
                year=year,
                region=region,
                base_plot_name=base_plot_name,
                row_count=row_count,
                repeats=repeats,
                phenotypic_fields=phenotypic_fields,
                dev_stage_fields=dev_stage_fields
            )
        
        # Извлекаем Excel данные
        excel_data = plot_data['excel']
        
        # Создаем Excel
        wb = Workbook()
        ws = wb.active
        ws.title = 'Результаты'
        
        # Записываем заголовки
        for col, header in enumerate(excel_data['headers'], 1):
            ws.cell(row=1, column=col, value=header)
            ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = 20
        
        # Записываем данные
        for row_data in excel_data['data']:
            ws.append(row_data)
        
        # Сохраняем файл
        filename = f"{excel_data['metadata']['base_plot_name']}_{excel_data['metadata']['field_name']}_{excel_data['metadata']['year']}.xlsx"
        path = Path(tempfile.gettempdir()) / filename
        wb.save(path)
        wb.close()
        
        return path, filename
