from http import HTTPStatus

import pytest

from utils.api.constants import FIELDS, STATISTICAL_FEATURES, TEST_CULTURES


class TestCrossAvgValuesMultipleGet:
    @pytest.mark.parametrize(
        'control_plot',
        [STATISTICAL_FEATURES['CROSS_AVG']['control_plot'], None]
    )
    def test_cross_avg_values_multiple_get( 
        self, get_token, plastilin_db_api, data_helper, schema_validator, control_plot
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

        if control_plot is None:
            control_plot_year_id = None
            year_ids = year_id
        else:
            control_plot_year_id = year_id
            year_ids = year_id

        response = plastilin_db_api.get_cross_avg_values_multiple(
            token=token,
            year_ids=year_ids,
            control_plot=control_plot,
            control_plot_year_id=control_plot_year_id,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/cross_avg_values_multiple/get_response.json'
        )

    @pytest.mark.skip(
        reason=(
            'Пропускаем сортировку по -line_name, '
            'пока не пофиксим сортировку в человеко-читаемом виде'
        )
    )
    @pytest.mark.parametrize(
        'sort_by, reverse',
        [
            ('-line_name', False),
            ('-line_name', True),
            ('plot_name', False),
            ('-plot_name', True),
        ],
    )
    def test_cross_avg_values_multiple_get_with_sort_by(
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
        control_plot = STATISTICAL_FEATURES['CROSS_AVG']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_cross_avg_values_multiple(
            token=token,
            year_ids=year_ids,
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
            ('avg', f'{STATISTICAL_FEATURES["CROSS_AVG"]["feature"]}', False),
            ('avg', f'-{STATISTICAL_FEATURES["CROSS_AVG"]["feature"]}', True),
            ('rank', f'{STATISTICAL_FEATURES["CROSS_AVG"]["feature"]}', False),
            ('rank', f'-{STATISTICAL_FEATURES["CROSS_AVG"]["feature"]}', True),
        ],
    )
    def test_cross_avg_values_multiple_get_with_sort_by__key(
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
        feature = STATISTICAL_FEATURES['CROSS_AVG']['feature']
        year_ids = year_id
        control_plot = STATISTICAL_FEATURES['CROSS_AVG']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_cross_avg_values_multiple(
            token=token,
            year_ids=year_ids,
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
        'name_of_multiple, value_of_multiple, feature_name_of_multiple, feature_value_of_multiple',
        [
            ('plot_name', '14', None, None),
            ('plot_name', 'Д 147', None, None),
            ('line_name', 'Аквамарин', None, None),
            ('avg_value', '20', 'avg', f'{STATISTICAL_FEATURES["CROSS_AVG"]["feature"]}'),
            ('avg_value', '0', 'avg', f'{STATISTICAL_FEATURES["CROSS_AVG"]["feature"]}'),
            ('rank', '1', 'rank', f'{STATISTICAL_FEATURES["CROSS_AVG"]["feature"]}'),
        ],
    )
    def test_cross_avg_values_multiple_get_value_of_multiple(
        self,
        get_token,
        plastilin_db_api,
        data_helper,
        name_of_multiple,
        value_of_multiple,
        feature_name_of_multiple,
        feature_value_of_multiple,
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
        control_plot = STATISTICAL_FEATURES['CROSS_AVG']['control_plot']
        control_plot_year_id = year_id
        response = plastilin_db_api.get_cross_avg_values_multiple(
            token=token,
            year_ids=year_ids,
            control_plot=control_plot,
            control_plot_year_id=control_plot_year_id,
            name_of_multiple=name_of_multiple,
            value_of_multiple=value_of_multiple,
            feature_name_of_multiple=feature_name_of_multiple,
            feature_value_of_multiple=feature_value_of_multiple,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой'

        data_values = data_helper.get_multiple_values_from_response(
            response_data, name_of_multiple, STATISTICAL_FEATURES['CROSS_AVG']['feature']
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


    def test_cross_avg_values_multiple_get_with_multiple_year_ids(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('head_of_company_company_1')
        _, _, year_id_1 = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        _, _, year_id_2 = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_3']['field_name'],
            year=FIELDS['field_3']['year'],
            region=FIELDS['field_3']['region'],
        )
        year_ids = [year_id_1, year_id_2]
        response = plastilin_db_api.get_cross_avg_values_multiple(
            token=token,
            year_ids=year_ids,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой'
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/cross_avg_values_multiple/get_response.json'
        )

    @pytest.mark.parametrize(
        'sort_by, reverse',
        [('field_name', False), ('-field_name', True), ('year', False), ('-year', True)],
    )
    def test_cross_avg_values_multiple_get_with_multiple_year_ids_and_sort_by(
        self, get_token, plastilin_db_api, data_helper, sort_by, reverse
    ):
        token = get_token('head_of_company_company_1')
        _, _, year_id_1 = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        _, _, year_id_2 = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_3']['field_name'],
            year=FIELDS['field_3']['year'],
            region=FIELDS['field_3']['region'],
        )
        year_ids = [year_id_1, year_id_2]
        response = plastilin_db_api.get_cross_avg_values_multiple(
            token=token,
            year_ids=year_ids,
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