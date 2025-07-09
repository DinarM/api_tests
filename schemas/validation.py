"""
Утилита для валидации JSON по схеме
"""
import json
from jsonschema import validate, ValidationError
from typing import Dict, Any
import os


class SchemaValidator:
    """
    Класс для валидации JSON по схеме
    """
    
    def __init__(self, schemas_dir: str = 'schemas'):
        self.schemas_dir = schemas_dir
        self._schemas_cache = {}
    
    def load_schema(self, schema_path: str) -> Dict:
        """
        Загрузка схемы из файла
        
        Args:
            schema_path: Путь к файлу схемы
            
        Returns:
            dict: Загруженная схема
        """
        if schema_path not in self._schemas_cache:
            full_path = os.path.join(self.schemas_dir, schema_path)
            with open(full_path, 'r', encoding='utf-8') as f:
                self._schemas_cache[schema_path] = json.load(f)
        
        return self._schemas_cache[schema_path]
    
    def validate_response(self, data: Any, schema_path: str) -> bool:
        """
        Валидация данных по схеме
        
        Args:
            data: Данные для валидации
            schema_path: Путь к файлу схемы
            
        Returns:
            bool: True если валидация прошла успешно
            
        Raises:
            ValidationError: Если валидация не прошла
        """
        schema = self.load_schema(schema_path)
        validate(instance=data, schema=schema)
        return True
    
    def assert_valid_response(self, data: Any, schema_path: str, message: str = None):
        """
        Assert для валидации с понятным сообщением об ошибке
        
        Args:
            data: Данные для валидации
            schema_path: Путь к файлу схемы
            message: Дополнительное сообщение
        """
        try:
            self.validate_response(data, schema_path)
        except ValidationError as e:
            # Формируем детальное сообщение об ошибке
            error_details = []
            
            # Путь к проблемному полю
            if e.path:
                field_path = ' -> '.join(str(p) for p in e.path)
                error_details.append(f'Поле: {field_path}')
            
            # Сообщение об ошибке
            error_details.append(f'Ошибка: {e.message}')
            
            # Ожидаемое значение (если есть)
            if hasattr(e, 'validator_value') and e.validator_value is not None:
                error_details.append(f'Ожидалось: {e.validator_value}')
            
            # Фактическое значение (если есть)
            if hasattr(e, 'instance') and e.instance is not None:
                error_details.append(f'Получено: {e.instance}')
            
            # Тип валидатора (что проверялось)
            if hasattr(e, 'validator') and e.validator:
                validator_name = e.validator
                if validator_name == 'required':
                    error_details.append('Проверка: обязательное поле')
                elif validator_name == 'type':
                    error_details.append('Проверка: тип данных')
                elif validator_name == 'format':
                    error_details.append('Проверка: формат данных')
                elif validator_name == 'pattern':
                    error_details.append('Проверка: регулярное выражение')
                elif validator_name == 'minLength':
                    error_details.append('Проверка: минимальная длина')
                elif validator_name == 'maxLength':
                    error_details.append('Проверка: максимальная длина')
                elif validator_name == 'minimum':
                    error_details.append('Проверка: минимальное значение')
                elif validator_name == 'maximum':
                    error_details.append('Проверка: максимальное значение')
                elif validator_name == 'enum':
                    error_details.append('Проверка: допустимые значения')
                else:
                    error_details.append(f'Проверка: {validator_name}')
            
            # Собираем все детали
            detailed_error = f'Валидация по схеме {schema_path} не прошла:\n' + '\n'.join(f'  • {detail}' for detail in error_details)
            
            if message:
                detailed_error += f'\n  • Контекст: {message}'
            
            raise AssertionError(detailed_error) 