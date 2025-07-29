"""
Хелперы для API операций
"""

import functools
import logging
import os
import time
from datetime import datetime


class NullValue:
    """
    Специальный класс для явного указания null значений в API запросах
    """

    def __repr__(self):
        return 'NullValue()'


class APIHelper:
    """
    Класс с полезными методами для API операций
    """
    
    # Настройка логирования в файл
    _logger_configured = False
    
    # Атрибуты для детального логирования
    _debug_logger_configured = False
    _debug_logger = None
    _debug_log_path = None
    
    @staticmethod
    def _setup_logging():
        """
        Настраивает логирование в файл
        """
        if not APIHelper._logger_configured:
            # Создаем папку для логов если её нет
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Создаем имя файла с датой
            log_filename = f'api_performance_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
            log_path = os.path.join(log_dir, log_filename)
            
            # Настраиваем логирование
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_path, encoding='utf-8'),
                    logging.StreamHandler()  # Также выводим в консоль
                ],
                force=True
            )
            
            APIHelper._logger_configured = True
            logging.info(f'Логирование API производительности запущено: {log_path}')

    @staticmethod
    def filter_none_values(data: dict) -> dict:
        """
        Удаляет из словаря все ключи со значением None, но оставляет NullValue

        Args:
            data: Исходный словарь

        Returns:
            dict: Словарь без None значений, но с NullValue
        """
        result = {}
        for key, value in data.items():
            if value is None:
                continue  # Пропускаем None
            elif isinstance(value, NullValue):
                result[key] = None  # NullValue превращаем в None для JSON
            else:
                result[key] = value
        return result

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

    @staticmethod
    def measure_response_time(max_time: float = 1.0):
        """
        Декоратор для измерения времени ответа API
        
        Args:
            max_time: Максимальное допустимое время ответа в секундах
            
        Returns:
            Декоратор для оборачивания API методов
        """
        # Настраиваем логирование при первом использовании
        APIHelper._setup_logging()
        
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    response_time = time.time() - start_time
                    
                    # Логируем все запросы
                    logging.info(f'API запрос: {func.__name__} - {response_time:.3f}с')
                    
                    if response_time > max_time:
                        logging.warning(
                            f'Медленный API запрос: {func.__name__} '
                            f'выполнился за {response_time:.3f}с '
                            f'(максимум {max_time}с)'
                        )
                    
                    return result
                except Exception as e:
                    response_time = time.time() - start_time
                    logging.error(
                        f'API запрос завершился с ошибкой: {func.__name__} '
                        f'за {response_time:.3f}с - {str(e)}'
                    )
                    raise
                    
            return wrapper
        return decorator

