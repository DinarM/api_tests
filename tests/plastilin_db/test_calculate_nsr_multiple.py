from http import HTTPStatus

import pytest

from utils.api.constants import FIELDS, STATISTICAL_FEATURES, TEST_CULTURES


class TestCalculateNSRMultipleGet:
    def test_calculate_nsr_multiple_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        year_ids = year_id
        feature = STATISTICAL_FEATURES['NSR']['feature']
        control_plot = STATISTICAL_FEATURES['NSR']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_calculate_nsr_multiple(
            token=token,
            year_ids=year_ids,
            feature=feature,
            control_plot=control_plot,
            control_plot_year_id=control_plot_year_id,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/calculate_nsr_multiple/get_response.json'
        )

    @pytest.mark.parametrize(
        'sort_by, reverse',
        [('line_name', False), ('-line_name', True), ('plot_name', False), ('-plot_name', True)],
    )
    def test_calculate_nsr_multiple_get_with_sort_by(
        self, get_token, plastilin_db_api, data_helper, sort_by, reverse
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        year_ids = year_id
        feature = STATISTICAL_FEATURES['NSR']['feature']
        control_plot = STATISTICAL_FEATURES['NSR']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_calculate_nsr_multiple(
            token=token,
            year_ids=year_ids,
            feature=feature,
            control_plot=control_plot,
            control_plot_year_id=control_plot_year_id,
            sort_by=sort_by,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой'

        key = sort_by.lstrip('-')
        sorted_data = [item[key] for item in response_data]
        assert sorted_data == sorted(
            sorted_data,
            key=lambda x: data_helper.universal_sort_key(x, reverse=reverse),
            reverse=reverse,
        ), f'Данные по ключу {sort_by} не отсортированы!'

    @pytest.mark.parametrize(
        'sort_by__key, sort_by__value, reverse',
        [
            ('avg', f'{STATISTICAL_FEATURES["NSR"]["feature"]}', False),
            ('avg', f'-{STATISTICAL_FEATURES["NSR"]["feature"]}', True),
            ('nsr', f'{STATISTICAL_FEATURES["NSR"]["feature"]}', False),
            ('nsr', f'-{STATISTICAL_FEATURES["NSR"]["feature"]}', True),
        ],
    )
    def test_calculate_nsr_multiple_get_with_sort_by__key(
        self, get_token, plastilin_db_api, data_helper, sort_by__key, sort_by__value, reverse
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        feature = STATISTICAL_FEATURES['NSR']['feature']
        year_ids = year_id
        control_plot = STATISTICAL_FEATURES['NSR']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_calculate_nsr_multiple(
            token=token,
            year_ids=year_ids,
            feature=feature,
            control_plot=control_plot,
            control_plot_year_id=control_plot_year_id,
            sort_by__key=sort_by__key,
            sort_by__value=sort_by__value,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой'

        key = (
            f'{sort_by__key}_value'.lstrip('-')
            if sort_by__key == 'avg'
            else sort_by__key.lstrip('-')
        )
        data_values = data_helper.get_multiple_values_from_response(
            response_data, key, feature
        )
        assert data_values == sorted(
            data_values,
            key=lambda x: data_helper.universal_sort_key(x, reverse=reverse),
            reverse=reverse,
        ), f'Данные по ключу {sort_by__key} не отсортированы!'


    @pytest.mark.parametrize(
        'filter_name, filter_value',
        [
            ('line_name', 'Аквамарин'),
            ('plot_name', 'Д 100'),
        ],

    )
    def test_calculate_nsr_multiple_get_with_filter(
        self, get_token, plastilin_db_api, data_helper, filter_name, filter_value
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        feature = STATISTICAL_FEATURES['NSR']['feature']
        year_ids = year_id
        control_plot = STATISTICAL_FEATURES['NSR']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_calculate_nsr_multiple(
            token=token,
            year_ids=year_ids,
            feature=feature,
            control_plot=control_plot,
            control_plot_year_id=control_plot_year_id,
            filter_name=filter_name,
            filter_value=filter_value,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой'

        data_values = data_helper.get_multiple_values_from_response(
            response_data, filter_name, STATISTICAL_FEATURES['NSR']['feature']
        )

        if filter_name == 'avg_value' and filter_value == '0':
            for data_value in data_values:
                assert float(filter_value) == float(data_value), (
                    f'Значение {filter_value} в фильтре {filter_name} '
                    f'не равно {data_value}!'
                )
        else:
            for data_value in data_values:
                assert str(filter_value).lower() in str(data_value).lower(), (
                    f'Значение {filter_value} в фильтре {filter_name} '
                    f'не найдено в {data_value}!'
                )

    @pytest.mark.parametrize(
            'name_of_multiple, value_of_multiple',
            [
                ('nsr', '1.3'),
                ('avg_value', '5.1'),
                ('avg_value', '0'),
            ],

        )
    def test_calculate_nsr_multiple_get_with_filter_multiple(
        self, get_token, plastilin_db_api, data_helper, name_of_multiple, value_of_multiple
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        feature = STATISTICAL_FEATURES['NSR']['feature']
        year_ids = year_id
        control_plot = STATISTICAL_FEATURES['NSR']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_calculate_nsr_multiple(
            token=token,
            year_ids=year_ids,
            feature=feature,
            control_plot=control_plot,
            control_plot_year_id=control_plot_year_id,
            name_of_multiple=name_of_multiple,
            value_of_multiple=value_of_multiple,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой'

        data_values = data_helper.get_multiple_values_from_response(
            response_data, name_of_multiple, STATISTICAL_FEATURES['NSR']['feature']
        )

        if name_of_multiple == 'avg_value' and value_of_multiple == '0':
            for data_value in data_values:
                assert float(value_of_multiple) == float(data_value), (
                    f'Значение {value_of_multiple} в фильтре {name_of_multiple} '
                    f'не равно {data_value}!'
                )
        else:
            for data_value in data_values:
                assert str(value_of_multiple).lower() in str(data_value).lower(), (
                    f'Значение {value_of_multiple} в фильтре {name_of_multiple} '
                    f'не найдено в {data_value}!'
                )