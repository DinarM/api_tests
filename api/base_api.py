class BaseAPI:
    def __init__(self, context):
        """
        Инициализация базового API клиента

        Args:
            context: Контекст запросов
        """
        self.context = context
        self.headers = {'Content-Type': 'application/json', 'Authorization': ''}
