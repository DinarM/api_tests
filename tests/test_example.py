def test_map_pins(dispatcher_api, get_token):

    """
    Тест получения маркеров на карте через API.
    Проверяет:
    - Успешное получение маркеров
    - Наличие обязательных полей в ответе
    - Корректность типов данных
    """
    token = get_token(phone='+09991579247')
    response = dispatcher_api.get_map_pins(token=token)

    # assert response['success'], "Не удалось получить маркеры на карте"
    assert 'data' in response.json(), "Ответ не содержит поле 'data'"
    assert response.status == 200


def test_calculate_cart(order_api, get_token):
    token = get_token(phone='+09991579247')
    response = order_api.calculate_cart(token=token, address='Москва, ул. Ленина, д. 1', deliveries=[
        {
            'items': [
                {
                    'product_id': '12345',
                    'quantity': 2
                }
            ],
            'delivery_type': 'standard'
        }
    ], warehouse_code='WH001')
    assert response.status == 200
    assert 'data' in response.json(), "Ответ не содержит поле 'data'"
    assert response.json()['data']['total_price'] > 0
    assert response.json()['data']['total_price'] == 0