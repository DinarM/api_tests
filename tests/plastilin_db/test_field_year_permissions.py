from http import HTTPStatus
import pytest
from utils.api.constants import TEST_CULTURES
from utils.api.constants import FIELDS

class TestFieldYearPermissionsGet:
    """
    Тесты для получения разрешений на полевые годы
    """
    def test_get_field_year_permissions_success(self, get_token, plastilin_db_api, schema_validator):
        """
        Тест успешного получения разрешений на полевые годы
        """
        token = get_token('head_of_company_company_1')
        response = plastilin_db_api.get_field_year_permissions(token=token)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'plastilin_db/field_year_permissions/get_response.json'
        )

    def test_get_field_year_permissions_by_id_success(self, get_token, plastilin_db_api, schema_validator, data_helper):
        """
        Тест успешного получения разрешений на полевые годы по ID
        """
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=token, name=data_helper.generate_random_string(name='Тестовая группа'), year_id=year_id).json()['id']
        response = plastilin_db_api.get_field_year_permissions_by_id(token=token, field_year_permission_id=field_year_permission_id)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'plastilin_db/field_year_permissions/get_by_id_response.json'
        )


class TestFieldYearPermissionsCreate:
    """
    Тесты для создания разрешений на полевые годы
    """
    def test_create_field_year_permissions_success(self, get_token, plastilin_db_api, schema_validator, data_helper):
        """
        Тест успешного создания разрешений на полевые годы
        """
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        response = plastilin_db_api.create_field_year_permissions(token=token, name=data_helper.generate_random_string(name='Тестовая группа'), year_id=year_id)
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'plastilin_db/field_year_permissions/create_response.json'
        )

class TestFieldYearPermissionsCreateInvite:
    """
    Тесты для создания приглашения в группу пользователей
    """
    def test_add_user_to_field_year_permissions_success(self, get_token, plastilin_db_api, schema_validator, data_helper):
        """
        Тест успешного создания приглашения в группу пользователей
        """
        token = get_token('head_of_company_company_1')
        employee_token = get_token('employee_company_1')
        user_id = data_helper.get_user_id(token=employee_token)
        spec_id, field_id, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=token, name=data_helper.generate_random_string(name='Тестовая группа'), year_id=year_id).json()['id']
        response = plastilin_db_api.add_user_to_field_year_permissions(token=token, field_year_permission_id=field_year_permission_id, user_id=user_id)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'plastilin_db/field_year_permissions/create_invite_response.json'
        )
        users = response_data.get('users', [])
        assert any(user['id'] == user_id for user in users), f"Пользователь с id {user_id} не найден в списке пользователей"


class TestFieldYearPermissionsUpdate:
    """
    Тесты для обновления разрешений на полевые годы
    """
    @pytest.mark.skip(reason='Баг в API')
    def test_update_field_year_permissions_success(self, get_token, plastilin_db_api, schema_validator, data_helper):
        """
        Тест успешного обновления разрешений на полевые годы
        """
        token = get_token('head_of_company_company_1')
        spec_id, field_id, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=token, name=data_helper.generate_random_string(name='Тестовая группа'), year_id=year_id).json()['id']
        new_name = data_helper.generate_random_string(name='Новая тестовая группа_')
        response = plastilin_db_api.update_field_year_permissions(token=token, field_year_permission_id=field_year_permission_id, name=new_name)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'plastilin_db/field_year_permissions/update_response.json',
        )
        response_data.get('name') == new_name

class TestFieldYearPermissionsDelete:
    """
    Тесты для удаления разрешений на полевые годы
    """
    @pytest.mark.skip(reason='Баг в API')
    def test_delete_field_year_permissions_success(self, get_token, plastilin_db_api, schema_validator, data_helper):
        """
        Тест успешного удаления разрешений на полевые годы
        """
        token = get_token('head_of_company_company_1')
        spec_id, field_id, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=token, name=data_helper.generate_random_string(name='Тестовая группа'), year_id=year_id).json()['id']
        response = plastilin_db_api.delete_field_year_permissions(token=token, field_year_permission_id=field_year_permission_id)
        assert response.status == HTTPStatus.OK
        # response_data = response.json()
        # schema_validator.assert_valid_response(
        #     response_data, 
        #     'plastilin_db/field_year_permissions/delete_response.json'
        # )

class TestFieldYearPermissionsPermissions:

    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_get_field_year_permissions_by_role(self, plastilin_db_api, schema_validator, data_helper, role, expected_status, get_token):
        """
        Тест успешного получения разрешений на полевые годы по роли
        """
        token = get_token(role)
        response = plastilin_db_api.get_field_year_permissions(token=token)
        assert response.status == expected_status

    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_get_field_year_permissions_by_id_by_role(self, plastilin_db_api, schema_validator, data_helper, role, expected_status, get_token):
        token = get_token(role)
        head_of_company_token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=head_of_company_token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=head_of_company_token, name=data_helper.generate_random_string(name='Тестовая группа_'), year_id=year_id).json()['id']
        response = plastilin_db_api.get_field_year_permissions_by_id(token=token, field_year_permission_id=field_year_permission_id)
        assert response.status == expected_status

    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.CREATED),
        ('head_of_division_company_1', HTTPStatus.CREATED),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_create_field_year_permissions_by_role(self, plastilin_db_api, schema_validator, data_helper, role, expected_status, get_token):
        token = get_token(role)
        head_of_company_token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=head_of_company_token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        response = plastilin_db_api.create_field_year_permissions(token=token, name=data_helper.generate_random_string(name='Тестовая группа_'), year_id=year_id)
        assert response.status == expected_status

    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_add_user_to_field_year_permissions_by_role(self, plastilin_db_api, schema_validator, data_helper, role, expected_status, get_token):
        token = get_token(role)
        employee_token = get_token('employee_company_1')
        user_id = data_helper.get_user_id(token=employee_token)
        head_of_company_token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=head_of_company_token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=head_of_company_token, name=data_helper.generate_random_string(name='Тестовая группа_'), year_id=year_id).json()['id']
        response = plastilin_db_api.add_user_to_field_year_permissions(token=token, field_year_permission_id=field_year_permission_id, user_id=user_id)
        assert response.status == expected_status

    @pytest.mark.skip(reason='Баг в API')
    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_update_field_year_permissions_by_role(self, plastilin_db_api, schema_validator, data_helper, role, expected_status, get_token):
        token = get_token(role)
        head_of_company_token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=head_of_company_token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=head_of_company_token, name=data_helper.generate_random_string(name='Тестовая группа_'), year_id=year_id).json()['id']
        response = plastilin_db_api.update_field_year_permissions(token=token, field_year_permission_id=field_year_permission_id, name=data_helper.generate_random_string(name='Новая тестовая группа_'))
        assert response.status == expected_status

    @pytest.mark.skip(reason='Баг в API')
    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_delete_field_year_permissions_by_role(self, plastilin_db_api, schema_validator, data_helper, role, expected_status, get_token):
        token = get_token(role)
        head_of_company_token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=head_of_company_token, spec_name=TEST_CULTURES['wheat']['russian_name'], field_name=FIELDS['field_1']['field_name'], year=FIELDS['field_1']['year'], region=FIELDS['field_1']['region'])
        field_year_permission_id = plastilin_db_api.create_field_year_permissions(token=head_of_company_token, name=data_helper.generate_random_string(name='Тестовая группа_'), year_id=year_id).json()['id']
        response = plastilin_db_api.delete_field_year_permissions(token=token, field_year_permission_id=field_year_permission_id)
        assert response.status == expected_status


