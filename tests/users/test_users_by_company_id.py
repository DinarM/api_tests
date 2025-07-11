from http import HTTPStatus

import pytest


class TestUsersByCompanyIdGet:
    """
    Тесты для получения списка пользователей по ID компании
    """

    def test_get_users_by_company_id_success(
        self, get_token, users_api, schema_validator, data_helper
    ):
        """
        Тест успешного получения списка пользователей по ID компании
        """
        token = get_token('head_of_company_company_1')
        company_id = data_helper.get_my_company_id(token=token)

        response = users_api.get_users_by_company_id(token=token, company_id=company_id)

        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data, 'users/users_by_company_id/list_response.json'
        )


class TestUsersByCompanyIdGetPermissions:
    """
    Тесты для проверки прав доступа к получению списка пользователей по ID компании
    """

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            # ('super_admin', HTTPStatus.OK), # баг
            ('head_of_company_company_1', HTTPStatus.OK),
            ('head_of_division_company_1', HTTPStatus.OK),
            ('employee_company_1', HTTPStatus.FORBIDDEN),
            ('standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_get_users_by_company_id_permissions(
        self, users_api, role, expected_status, get_token, data_helper
    ):
        """
        Тест проверки прав доступа к получению списка пользователей по ID компании
        """
        token = get_token(role)
        company_id = data_helper.get_my_company_id(token=token)
        response = users_api.get_users_by_company_id(token=token, company_id=company_id)
        assert response.status == expected_status
