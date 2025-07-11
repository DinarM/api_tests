from http import HTTPStatus


class TestProfileGet:
    """
    Тесты для получения профиля пользователя
    """

    def test_get_profile_success(self, get_token, users_api, schema_validator):
        """
        Тест успешного получения профиля пользователя
        """
        token = get_token()
        response = users_api.get_profile(token=token)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(response_data, 'users/profile/get_response.json')
