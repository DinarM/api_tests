import inspect

from utils.api.api_helpers import APIHelper


class BaseAPI:
    def __init__(self, context):
        """
        Инициализация базового API клиента

        Args:
            context: Контекст запросов
        """
        self.context = context
        self.headers = {'Content-Type': 'application/json', 'Authorization': ''}

        self._auto_decorate_methods()

    def _auto_decorate_methods(self):
        """
        Автоматически применяет декоратор измерения времени ко всем методам
        """
        for method_name in dir(self):
            if not method_name.startswith('_'):
                method = getattr(self, method_name)
                if inspect.ismethod(method) or inspect.isfunction(method):
                    decorated = APIHelper.measure_response_time(max_time=1.0)(method)
                    setattr(self, method_name, decorated)
