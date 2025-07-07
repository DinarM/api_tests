"""
Хелперы для API операций
"""
from typing import Dict, Any
import time


class APIHelper:
    """
    Класс с полезными методами для API операций
    """
    
    @staticmethod
    def retry_request(func, max_retries: int = 3, delay: float = 1.0):
        """
        Повторяет запрос при ошибке
        
        Args:
            func: Функция для выполнения
            max_retries: Максимальное количество попыток
            delay: Задержка между попытками в секундах
            
        Returns:
            Результат выполнения функции
        """
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(delay)
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: float = 30.0, interval: float = 1.0):
        """
        Ожидает выполнения условия
        
        Args:
            condition_func: Функция, возвращающая True когда условие выполнено
            timeout: Таймаут в секундах
            interval: Интервал проверки в секундах
            
        Returns:
            bool: True если условие выполнено, False если истек таймаут
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False
    