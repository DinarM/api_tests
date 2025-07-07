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
            error_msg = f'Валидация по схеме {schema_path} не прошла: {e.message}'
            if message:
                error_msg += f' | {message}'
            raise AssertionError(error_msg) 