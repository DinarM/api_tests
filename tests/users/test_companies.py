from http import HTTPStatus

import pytest


class TestCompaniesGet:
    """
    Тесты для получения данных компаний
    """

    def test_get_companies_success(self, get_token, users_api, schema_validator):
        """
        Тест успешного получения списка компаний
        """
        token = get_token('head_of_company_company_1')

        response = users_api.get_companies(token=token)

        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(response_data, 'users/companies/list_response.json')


class TestCompaniesCreate:
    """
    Тесты для создания компаний
    """

    pass


class TestCompaniesPermissions:
    """
    Тесты ролевой модели и прав доступа к компаниям
    """

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            # ('super_admin', HTTPStatus.OK),  # баг
            ('head_of_company_company_1', HTTPStatus.OK),
            ('head_of_division_company_1', HTTPStatus.OK),
            ('employee_company_1', HTTPStatus.FORBIDDEN),
            ('standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_get_companies_by_role(self, users_api, role, expected_status, get_token):
        token = get_token(role)
        response = users_api.get_companies(token=token)
        assert response.status == expected_status
