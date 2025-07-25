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
            response_data, 'users/users_groups/list_response.json'
        )

    @pytest.mark.skip(reason='TODO: дописать, если фронт реально будет использовать параметры')
    @pytest.mark.parametrize(
        'name,username,first_name,last_name,company_name,creator_id,ordering',
        [
            ('Test Group', None, None, None, None, None, None),
            (None, 'QA_user_1_div_1', None, None, None, None, None),
        ],
    )
    def test_get_users_groups_success_with_params(
        self,
        get_token,
        users_api,
        schema_validator,
        data_helper,
        name,
        username,
        first_name,
        last_name,
        company_name,
        creator_id,
        ordering,
    ):
        """
        Тест успешного получения списка групп пользователей с параметрами
        """
        token = get_token('head_of_company_company_1')
        response = users_api.get_users_groups(
            token=token, 
            name=name, 
            username=username, 
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            creator_id=creator_id,
            ordering=ordering,
        )
        assert response.status == HTTPStatus.OK
        # response_data = response.json()


    def test_get_users_groups_by_id_success(
        self, get_token, users_api, schema_validator, data_helper
    ):
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
            response_data, 'users/users_groups/get_by_id_response.json'
        )


class TestUsersGroupsCreate:
    """
    Тесты для создания групп пользователей
    """

    def test_create_users_groups_success_required_fields(
        self, get_token, users_api, schema_validator, data_helper
    ):
        """
        Тест успешного создания группы пользователей с обязательными полями
        """
        token = get_token('head_of_company_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        response = users_api.create_users_groups(token=token, name=name)
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'users/users_groups/create_response.json'
        )

    @pytest.mark.parametrize(
        'read,write,add_yourself,user_ids',
        [
            (True, True, True, ['employee_company_1']),
            (True, False, False, ['employee_company_1', 'employee_2_company_1']),
            (False, True, False, None),
            (False, False, True, None),
            (True, True, False, None),
        ],
    )
    def test_create_users_groups_success_all_fields(
        self, get_token, users_api, data_helper, read, write, add_yourself, user_ids
    ):
        """
        Тест успешного создания группы пользователей с всеми полями
        """
        token = get_token('head_of_company_company_1')
        self_user_id = data_helper.get_user_id(token=token)
        ids = data_helper.get_user_ids_by_usernames(get_token, user_ids)
        name = data_helper.generate_random_string(name='Test Group')
        response = users_api.create_users_groups(
            token=token,
            name=name,
            read=read,
            write=write,
            add_yourself=add_yourself,
            user_ids=ids,
        )
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()

        if read:
            assert response_data['read'] == read
        if write:
            assert response_data['write'] == write
        if add_yourself:
            assert self_user_id in [user['id'] for user in response_data['users']]
        if user_ids:
            assert all(
                user_id in [user['id'] for user in response_data['users']] for user_id in ids
            )



class TestUsersGroupsCreateInvite:
    """
    Тесты для создания приглашения в группу пользователей
    """

    def test_create_users_groups_invite_success(
        self, get_token, users_api, schema_validator, data_helper
    ):
        """
        Тест успешного создания приглашения в группу пользователей
        """
        token = get_token('head_of_company_company_1')
        employee_token = get_token('employee_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        employee_user_id = data_helper.get_user_id(token=employee_token)
        response = users_api.invite_user_to_group(
            token=token, user_group_id=group_id, user_ids=[employee_user_id]
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'users/users_groups/create_invite_response.json'
        )


class TestUsersGroupsUpdate:
    """
    Тесты для обновления групп пользователей
    """
    def test_update_users_groups_success(
        self, get_token, users_api, schema_validator, data_helper
    ):
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
            response_data, 'users/users_groups/update_response.json'
        )
        assert response_data['name'] == new_name


class TestUsersGroupsDelete:
    """
    Тесты для удаления групп пользователей
    """

    def test_delete_users_groups_success(
        self, get_token, users_api, data_helper
    ):
        """
        Тест успешного удаления группы пользователей
        """
        token = get_token('head_of_company_company_1')
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.delete_users_group(token=token, group_id=group_id)
        assert response.status == HTTPStatus.NO_CONTENT


class TestUsersGroupsPermissions:
    """
    Тесты для проверки прав доступа к группам пользователей
    """

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('super_admin', HTTPStatus.CREATED),
            ('head_of_company_company_1', HTTPStatus.CREATED),
            ('head_of_division_company_1', HTTPStatus.CREATED),
            ('employee_company_1', HTTPStatus.FORBIDDEN),
            ('standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_create_users_groups_permissions(
        self, users_api, role, expected_status, data_helper, get_token
    ):
        """
        Тест проверки прав доступа к созданию групп пользователей
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        response = users_api.create_users_groups(token=token, name=name)
        assert response.status == expected_status

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('super_admin', HTTPStatus.OK),
            ('head_of_company_company_1', HTTPStatus.OK),
            ('head_of_division_company_1', HTTPStatus.OK),
            ('employee_company_1', HTTPStatus.FORBIDDEN),
            ('standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_get_users_groups_permissions(self, users_api, role, expected_status, get_token):
        """
        Тест проверки прав доступа к получению списка групп пользователей
        """
        token = get_token(role)
        response = users_api.get_users_groups(token=token)
        assert response.status == expected_status

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('super_admin', HTTPStatus.OK),
            ('head_of_company_company_1', HTTPStatus.OK),
            ('head_of_division_company_1', HTTPStatus.OK),
            ('employee_company_1', HTTPStatus.FORBIDDEN),
            ('standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_get_users_groups_by_id_permissions(
        self, users_api, role, expected_status, get_token, data_helper
    ):
        """
        Тест проверки прав доступа к получению группы пользователей по ID
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.get_users_group_by_id(token=token, group_id=group_id)
        assert response.status == expected_status

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('super_admin', HTTPStatus.OK),
            ('head_of_company_company_1', HTTPStatus.OK),
            ('head_of_division_company_1', HTTPStatus.OK),
            ('employee_company_1', HTTPStatus.FORBIDDEN),
            ('standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_update_users_groups_permissions(
        self, users_api, role, expected_status, get_token, data_helper
    ):
        """
        Тест проверки прав доступа к обновлению группы пользователей
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        new_name = data_helper.generate_random_string(name='New Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.update_users_group(token=token, group_id=group_id, name=new_name)
        assert response.status == expected_status

    @pytest.mark.parametrize(
        'role,expected_status',
        [
            ('super_admin', HTTPStatus.NO_CONTENT),
            ('head_of_company_company_1', HTTPStatus.NO_CONTENT),
            ('head_of_division_company_1', HTTPStatus.NO_CONTENT),
            ('employee_company_1', HTTPStatus.FORBIDDEN),
            ('standalone_user', HTTPStatus.FORBIDDEN),
        ],
    )
    def test_delete_users_groups_permissions(
        self, users_api, role, expected_status, get_token, data_helper
    ):
        """
        Тест проверки прав доступа к удалению группы пользователей
        """
        token = get_token(role)
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        response = users_api.delete_users_group(token=token, group_id=group_id)
        assert response.status == expected_status

    @pytest.mark.parametrize(
        'role,expected_status,employee_role',
        [
            ('super_admin', HTTPStatus.OK, 'standalone_user'),
            ('head_of_company_company_1', HTTPStatus.OK, 'employee_company_1'),
            ('head_of_division_company_1', HTTPStatus.OK, 'employee_company_1'),
            ('employee_company_1', HTTPStatus.FORBIDDEN, 'employee_company_1'),
            ('standalone_user', HTTPStatus.FORBIDDEN, 'employee_company_1'),
        ],
    )
    def test_invite_user_to_group_permissions(
        self, users_api, role, expected_status, get_token, data_helper, employee_role
    ):
        """
        Тест проверки прав доступа к приглашению пользователя в группу
        """
        token = get_token(role)
        employee_token = get_token(employee_role)
        name = data_helper.generate_random_string(name='Test Group')
        group_id = users_api.create_users_groups(token=token, name=name).json().get('id')
        employee_user_id = data_helper.get_user_id(token=employee_token)
        response = users_api.invite_user_to_group(
            token=token, user_group_id=group_id, user_ids=[employee_user_id]
        )
        assert response.status == expected_status
