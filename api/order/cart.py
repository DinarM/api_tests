from api.base_api import BaseAPI
import uuid
from typing import List, Dict, Optional, Union

class OrderCartAPI(BaseAPI):
    def calculate_cart(
        self,
        token: str,
        address: Dict[str, float],
        deliveries: List[Dict],
        warehouse_code: str,
        seller: str = 'jiffy',
        delivery_method: str = 'JIFFY_DELIVERY',
        should_use_loyalty_points: bool = False,
        should_use_bonuses: bool = False,
        tips_amount: int = 0
    ) -> Dict:
        """
        Расчет стоимости корзины
        
        Args:
            address: Словарь с координатами {'latitude': float, 'longitude': float}
            deliveries: Список доставок с товарами
            warehouse_code: Код склада
            seller: Продавец (по умолчанию 'jiffy')
            delivery_method: Метод доставки (по умолчанию 'JIFFY_DELIVERY')
            should_use_loyalty_points: Использовать ли бонусные баллы
            should_use_bonuses: Использовать ли бонусы
            tips_amount: Сумма чаевых
            
        Returns:
            Dict: Ответ с расчетом стоимости
        """

        headers = self.headers.copy()
        headers['Authorization'] = token

        payload = {
            'address': address,
            'delivery_method': delivery_method,
            'deliveries': deliveries,
            'seller': seller,
            'should_use_loyalty_points': should_use_loyalty_points,
            'should_use_bonuses': should_use_bonuses,
            'warehouse_code': warehouse_code,
            'tips_amount': tips_amount
        }
        
        return self.context.post('url', data=payload, headers=self.headers)
    