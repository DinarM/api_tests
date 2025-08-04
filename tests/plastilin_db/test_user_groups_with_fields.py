from http import HTTPStatus

import pytest


class TestUserGroupsWithFieldsGet:
    """
    Тесты для получения списка групп пользователей с полями
    """

    def test_get_user_groups_with_fields_success(
        self, get_token, plastilin_db_api, schema_validator
    ):
        """
        Тест успешного получения списка групп пользователей с полями
        """
        token = get_token('company_1.head_of_company')
        response = plastilin_db_api.get_user_groups_with_fields(token=token)

        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/user_groups_with_fields/list_response.json'
        )


class TestUserGroupsWithFieldsGetPermissions:
    """
    Тесты для проверки прав доступа к получению списка групп пользователей с полями
    """

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('other.super_admin', HTTPStatus.OK),
            ('company_1.head_of_company', HTTPStatus.OK),
            ('company_1.division_1.head_of_division', HTTPStatus.OK),
            ('company_1.division_1.employee_1', HTTPStatus.FORBIDDEN),
            ('other.standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_get_user_groups_with_fields_permissions(
        self, plastilin_db_api, schema_validator, role, expected_status, get_token
    ):
        """
        Тест проверки прав доступа к получению списка групп пользователей с полями
        """
        token = get_token(role)
        response = plastilin_db_api.get_user_groups_with_fields(token=token)
        assert response.status == expected_status
