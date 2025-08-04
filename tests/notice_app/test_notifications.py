from http import HTTPStatus


class TestNotificationsGet:
    def test_notifications_get_success(self, get_token, notice_app_api, schema_validator):
        token = get_token('company_1.head_of_company')

        response = notice_app_api.get_notifications(token)

        assert response.status == HTTPStatus.OK
        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data, 'notice_app/notifications/get_response.json'
        )