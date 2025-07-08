from http import HTTPStatus
import pytest


class TestUsersGroupsGet:
    """
    Тесты для получения списка групп пользователей
    """
    
    def test_get_users_groups_success(self, get_token, users_api, schema_validator):
        """
        Тест успешного получения списка групп пользователей
        """
        token = get_token('head_of_company_company_1')
        response = users_api.get_users_groups(token=token)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'users/users_groups/list_response.json'
        )

    def test_get_users_groups_by_id_success(self, get_token, users_api, schema_validator, data_helper):
        """
        Тест успешного получения группы пользователей по ID
        """
        token = get_token('head_of_company_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.get_users_group_by_id(token=token, group_id=group_id)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'users/users_groups/get_by_id_response.json'
        )


class TestUsersGroupsCreate:
    """
    Тесты для создания групп пользователей
    """
    
    def test_create_users_groups_success_required_fields(self, get_token, users_api, schema_validator, data_helper):
        """
        Тест успешного создания группы пользователей с обязательными полями
        """
        token = get_token('head_of_company_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        response = users_api.create_users_groups(token=token, name=name)
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'users/users_groups/create_response.json'
        )

class TestUsersGroupsCreateInvite:
    """
    Тесты для создания приглашения в группу пользователей
    """
    # TODO: дописать тест
    def test_create_users_groups_invite_success(self, get_token, users_api, schema_validator, data_helper):
        """
        Тест успешного создания приглашения в группу пользователей
        """
        token = get_token('head_of_company_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.create_users_groups_invite(token=token, group_id=group_id)
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'users/users_groups/create_invite_response.json'
        )



class TestUsersGroupsUpdate:
    """
    Тесты для обновления групп пользователей
    """
    @pytest.mark.skip(reason="Этот тест временно отключен из-за бага")
    def test_update_users_groups_success(self, get_token, users_api, schema_validator, data_helper):
        """
        Тест успешного обновления группы пользователей
        """
        token = get_token('head_of_company_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        new_name = data_helper.generate_random_string(name='New Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.update_users_group(token=token, group_id=group_id, name=new_name)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 
            'users/users_groups/update_response.json'
        )
        assert response_data['name'] == new_name


class TestUsersGroupsDelete:
    """
    Тесты для удаления групп пользователей
    """
    @pytest.mark.skip(reason="Этот тест временно отключен из-за бага")
    def test_delete_users_groups_success(self, get_token, users_api, schema_validator, data_helper):
        """
        Тест успешного удаления группы пользователей
        """
        token = get_token('head_of_company_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.delete_users_group(token=token, group_id=group_id)
        assert response.status == HTTPStatus.OK


class TestUsersGroupsPermissions:
    """
    Тесты для проверки прав доступа к группам пользователей
    """
    
    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.CREATED),  # баг
        ('head_of_company_company_1', HTTPStatus.CREATED),
        ('head_of_division_company_1', HTTPStatus.CREATED),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_create_users_groups_permissions(self, users_api, role, expected_status, data_helper, get_token):
        """
        Тест проверки прав доступа к созданию групп пользователей   
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        response = users_api.create_users_groups(token=token, name=name)
        assert response.status == expected_status

    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_get_users_groups_permissions(self, users_api, role, expected_status, get_token):
        """
        Тест проверки прав доступа к получению списка групп пользователей
        """
        token = get_token(role)
        response = users_api.get_users_groups(token=token)
        assert response.status == expected_status

    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_get_users_groups_by_id_permissions(self, users_api, role, expected_status, get_token, data_helper):
        """
        Тест проверки прав доступа к получению группы пользователей по ID
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.get_users_group_by_id(token=token, group_id=group_id)
        assert response.status == expected_status

    @pytest.mark.skip(reason="Этот тест временно отключен из-за бага")
    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_update_users_groups_permissions(self, users_api, role, expected_status, get_token, data_helper):
        """
        Тест проверки прав доступа к обновлению группы пользователей
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        new_name = data_helper.generate_random_string(name='New Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.update_users_group(token=token, group_id=group_id, name=new_name)
        assert response.status == expected_status

    @pytest.mark.skip(reason="Этот тест временно отключен из-за бага")
    @pytest.mark.parametrize('role,expected_status', [
        # ('super_admin', HTTPStatus.OK),  # баг
        ('head_of_company_company_1', HTTPStatus.OK),
        ('head_of_division_company_1', HTTPStatus.OK),
        ('employee_company_1', HTTPStatus.FORBIDDEN),
        ('standalone_user', HTTPStatus.FORBIDDEN),
    ])
    def test_delete_users_groups_permissions(self, users_api, role, expected_status, get_token, data_helper):
        """
        Тест проверки прав доступа к удалению группы пользователей
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.delete_users_group(token=token, group_id=group_id)
        assert response.status == expected_status