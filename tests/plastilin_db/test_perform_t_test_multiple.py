from http import HTTPStatus

import pytest

from utils.api.constants import FIELDS, TEST_CULTURES


class TestPerformTTestMultipleGet:
    def test_perform_t_test_multiple_get(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(
            token, year_ids, feature, control_plot, control_plot_year_id
        )
        assert response.status == HTTPStatus.OK
        schema_validator.assert_valid_response(
            response.json(), 'plastilin_db/perform_t_test_multiple/get_response.json'
        )

    # @pytest.mark.skip(reason='Не работает сортировка по plot_name')
    @pytest.mark.parametrize(
        'sort_by, reverse',
        [('line_name', False), ('-line_name', True), ('plot_name', False), ('-plot_name', True)],
    )
    def test_perform_t_test_multiple_get_sort_by(
        self, get_token, plastilin_db_api, data_helper, sort_by, reverse
    ):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(
            token, year_ids, feature, control_plot, control_plot_year_id, sort_by=sort_by
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой!'

        key = sort_by.lstrip('-')
        sorted_data = [item[key] for item in response_data]
        assert sorted_data == sorted(
            sorted_data,
            key=lambda x: data_helper.universal_sort_key(x, reverse=reverse),
            reverse=reverse,
        ), f'Данные по ключу {sort_by} не отсортированы!'

    # @pytest.mark.skip(reason='Не работает сортировка по plot_name')
    @pytest.mark.parametrize(
        'sort_by__key, sort_by__value, reverse',
        [
            ('avg', 'размер бобов', False),
            ('avg', '-размер бобов', True),
            ('lower', 'размер бобов', False),
            ('lower', '-размер бобов', True),
            ('upper', 'размер бобов', False),
            ('upper', '-размер бобов', True),
            ('p_value', 'размер бобов', False),
            ('p_value', '-размер бобов', True),
        ],
    )
    def test_perform_t_test_multiple_get_sort_by__key(
        self, get_token, plastilin_db_api, data_helper, sort_by__key, sort_by__value, reverse
    ):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(
            token,
            year_ids,
            feature,
            control_plot,
            control_plot_year_id,
            sort_by__key=sort_by__key,
            sort_by__value=sort_by__value,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой!'

        key = (
            f'{sort_by__key}_value'.lstrip('-')
            if sort_by__key == 'avg'
            else sort_by__key.lstrip('-')
        )
        sorted_data = [item['features'][0][key] for item in response_data]
        assert sorted_data == sorted(
            sorted_data,
            key=lambda x: data_helper.universal_sort_key(x, reverse=reverse),
            reverse=reverse,
        ), f'Данные по ключу {sort_by__key} не отсортированы!'

    @pytest.mark.parametrize(
        'name_of_multiple, value_of_multiple',
        [
            ('plot_name', '14'),
            ('plot_name', 'Д 147'),
            ('line_name', 'Аквамарин'),
            ('avg_value', '137'),
            ('lower', '134'),
            ('upper', '139'),
            ('p_value', '0.5'),
        ],
    )
    def test_perform_t_test_multiple_get_value_of_multiple(
        self, get_token, plastilin_db_api, data_helper, name_of_multiple, value_of_multiple
    ):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(
            token,
            year_ids,
            feature,
            control_plot,
            control_plot_year_id,
            name_of_multiple=name_of_multiple,
            value_of_multiple=value_of_multiple,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой!'

        data_values = (
            [item['features'][0][name_of_multiple] for item in response_data]
            if name_of_multiple not in ['line_name', 'plot_name']
            else [item[name_of_multiple] for item in response_data]
        )

        for data_value in data_values:
            assert str(value_of_multiple).lower() in str(data_value).lower(), (
                f'Значение {value_of_multiple} в фильтре {name_of_multiple} не найдено в {data_value}!'
            )
