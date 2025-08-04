from http import HTTPStatus

import pytest

from utils.api.constants import FIELDS, TEST_CULTURES


@pytest.fixture(scope='function', autouse=True)
def cleanup_once_per_module(get_token, data_helper):
    yield
    token = get_token('company_1.head_of_company')
    data_helper.delete_all_field_year_permissions(token=token)


class TestFieldYearPermissionsGet:
    """
    Тесты для получения разрешений на полевые годы
    """

    def test_get_field_year_permissions_success(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест успешного получения разрешений на полевые годы
        """
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        plastilin_db_api.create_field_year_permissions(
            token=token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        )
        response = plastilin_db_api.get_field_year_permissions(token=token)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/field_year_permissions/get_response.json'
        )

    def test_get_field_year_permissions_by_id_success(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест успешного получения разрешений на полевые годы по ID
        """
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(
            token=token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        ).json()[0]['id']
        response = plastilin_db_api.get_field_year_permissions_by_id(
            token=token, field_year_permission_id=field_year_permission_id
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/field_year_permissions/get_by_id_response.json'
        )


class TestFieldYearPermissionsCreate:
    """
    Тесты для создания разрешений на полевые годы
    """

    def test_create_field_year_permissions_success(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест успешного создания разрешений на полевые годы
        """
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_field_year_permissions(
            token=token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        )
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/field_year_permissions/create_response.json'
        )



class TestFieldYearPermissionsUpdate:
    """
    Тесты для обновления разрешений на полевые годы
    """

    def test_update_field_year_permissions_success(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест успешного обновления разрешений на полевые годы
        """
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(
            token=token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        ).json()[0]['id']
        new_name = data_helper.generate_random_string(name='Новая тестовая группа_')
        response = plastilin_db_api.update_field_year_permissions(
            token=token, field_year_permission_id=field_year_permission_id, name=new_name
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/field_year_permissions/update_response.json',
        )
        assert response_data.get('user_group_name') == new_name


class TestFieldYearPermissionsDelete:
    """
    Тесты для удаления разрешений на полевые годы
    """

    def test_delete_field_year_permissions_success(
        self, get_token, plastilin_db_api, data_helper
    ):
        """
        Тест успешного удаления разрешений на полевые годы
        """
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(
            token=token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        ).json()[0]['id']
        response = plastilin_db_api.delete_field_year_permissions(
            token=token, field_year_permission_id=field_year_permission_id
        )
        assert response.status == HTTPStatus.NO_CONTENT


class TestFieldYearPermissionsPermissions:
    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('other.super_admin', HTTPStatus.OK),  # баг
            ('company_1.head_of_company', HTTPStatus.OK),
            ('company_1.division_1.head_of_division', HTTPStatus.OK),
            ('company_1.division_1.employee_1', HTTPStatus.FORBIDDEN),
            ('other.standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_get_field_year_permissions_by_role(
        self, plastilin_db_api, role, expected_status, get_token
    ):
        """
        Тест успешного получения разрешений на полевые годы по роли
        """
        token = get_token(role)
        response = plastilin_db_api.get_field_year_permissions(token=token)
        assert response.status == expected_status

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
    def test_get_field_year_permissions_by_id_by_role(
        self, plastilin_db_api, data_helper, role, expected_status, get_token
    ):
        token = get_token(role)
        head_of_company_token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=head_of_company_token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(
            token=head_of_company_token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        ).json()[0]['id']
        response = plastilin_db_api.get_field_year_permissions_by_id(
            token=token, field_year_permission_id=field_year_permission_id
        )
        assert response.status == expected_status

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('other.super_admin', HTTPStatus.CREATED),
            ('company_1.head_of_company', HTTPStatus.CREATED),
            ('company_1.division_1.head_of_division', HTTPStatus.CREATED),
            ('company_1.division_1.employee_1', HTTPStatus.FORBIDDEN),
            ('other.standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_create_field_year_permissions_by_role(
        self, plastilin_db_api, data_helper, role, expected_status, get_token
    ):
        token = get_token(role)
        head_of_company_token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=head_of_company_token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_field_year_permissions(
            token=token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        )
        assert response.status == expected_status


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
    def test_update_field_year_permissions_by_role(
        self, plastilin_db_api, data_helper, role, expected_status, get_token
    ):
        token = get_token(role)
        head_of_company_token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=head_of_company_token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(
            token=head_of_company_token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        ).json()[0]['id']
        response = plastilin_db_api.update_field_year_permissions(
            token=token,
            field_year_permission_id=field_year_permission_id,
            name=data_helper.generate_random_string(name='Новая тестовая группа_'),
        )
        assert response.status == expected_status

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('other.super_admin', HTTPStatus.NO_CONTENT),
            ('company_1.head_of_company', HTTPStatus.NO_CONTENT),
            ('company_1.division_1.head_of_division', HTTPStatus.NO_CONTENT),
            ('company_1.division_1.employee_1', HTTPStatus.FORBIDDEN),
            ('other.standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_delete_field_year_permissions_by_role(
        self, plastilin_db_api, data_helper, role, expected_status, get_token
    ):
        token = get_token(role)
        head_of_company_token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=head_of_company_token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(
            token=head_of_company_token,
            name=data_helper.generate_random_string(name='Тестовая группа'),
            year_ids=[year_id],
        ).json()[0]['id']
        response = plastilin_db_api.delete_field_year_permissions(
            token=token, field_year_permission_id=field_year_permission_id
        )
        assert response.status == expected_status
