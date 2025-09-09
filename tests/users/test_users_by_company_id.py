from http import HTTPStatus

import pytest


class TestUsersByCompanyIdGet:
    """
    Тесты для получения списка пользователей по ID компании
    """

    def test_get_users_by_company_id_success(
        self, get_token, users_api, schema_validator
    ):
        """
        Тест успешного получения списка пользователей по ID компании
        """
        token = get_token('company_1.head_of_company')

        response = users_api.get_users_by_company_id(token=token)

        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data, 'users/users_by_company_id/list_response.json'
        )

    @pytest.mark.skip(reason='Разобраться, используется ли этот фильтр на фронте')
    @pytest.mark.parametrize(
        'username,role,group_name',
        [
            (None, 'head_of_division', None),
            (None, None, 'Test Group'),
            ('QA_head_of_div', None, None),
            ('QA_user_2_div', 'employee', None),
            (None, 'employee', 'Test Group'),
            ('QA_user_2_div', 'employee', 'Test Group'),
        ],
    )
    def test_get_users_by_company_id_with_filter(
        self, get_token, users_api, username, role, group_name
    ):
        """
        Тест успешного получения списка пользователей по ID компании
        """
        token = get_token('company_1.head_of_company')

        response = users_api.get_users_by_company_id(
            token=token,
            username=username,
            role=role,
            group_name=group_name,
        )

        assert response.status == HTTPStatus.OK

        response_data = response.json()

        if username:
            assert any(username in user['username'] for user in response_data)
        if role:
            assert any(role in user['role'] for user in response_data)
        if group_name:
            assert any(
                group_name in group['name']
                for user in response_data
                for group in user.get('permission_groups', [])
            )

    @pytest.mark.parametrize(
        'ordering,ordering_by_groups,reverse',
        [
            ('id', None, False),
            ('-id', None, True),
            ('username', None, False),
            ('-username', None, True),
            (None, 'id', False),
            (None, '-id', True),
            # (None, 'name', False), # TODO: fix есть разница между сортировкой в апи и питоне
            (None, '-name', True),
        ],
    )
    def test_get_users_by_company_id_with_ordering(
        self, get_token, users_api, ordering, ordering_by_groups, reverse
    ):
        """
        Тест успешного получения списка пользователей по ID компании
        """
        token = get_token('company_1.head_of_company')

        response = users_api.get_users_by_company_id(
            token=token,
            ordering=ordering,
            ordering_by_groups=ordering_by_groups,
        )

        assert response.status == HTTPStatus.OK

        response_data = response.json()
        assert response_data, 'Ответ пустой!'


        if ordering in ('id', 'username'):
            key = ordering.lstrip('-')
            values = [user[key] for user in response_data]
            sorted_values = sorted(values, reverse=reverse)
            assert values == sorted_values, f'Пользователи не отсортированы по {ordering}!'

        if ordering_by_groups == 'name':
            for user in response_data:
                group_names = [group['name'] for group in user.get('permission_groups', [])]
                sorted_names = sorted(group_names, reverse=reverse)
                assert group_names == sorted_names, (
                    f'Группы пользователя {user.get("username")} не отсортированы по name!'
                )
        elif ordering_by_groups == 'id':
            for user in response_data:
                group_ids = [group['id'] for group in user.get('permission_groups', [])]
                sorted_ids = sorted(group_ids, reverse=reverse)
                assert group_ids == sorted_ids, (
                    f'Группы пользователя {user.get("username")} не отсортированы по id!'
                )


class TestUsersByCompanyIdGetPermissions:
    """
    Тесты для проверки прав доступа к получению списка пользователей по ID компании
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
    def test_get_users_by_company_id_permissions(
        self, users_api, role, expected_status, get_token
    ):
        """
        Тест проверки прав доступа к получению списка пользователей по ID компании
        """
        token = get_token(role)
        response = users_api.get_users_by_company_id(token=token)
        assert response.status == expected_status
