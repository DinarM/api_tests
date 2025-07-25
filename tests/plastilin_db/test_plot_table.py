import uuid
from http import HTTPStatus

import pytest

from utils.api.constants import FIELDS, REPETITIONS, TEST_CULTURES


class TestPlotTableCreate:
    def test_plot_table_create_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=data_helper.generate_random_string('Тестовая делянка'),
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=data_helper.generate_random_string('Тестовый сорт'),
        )
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/plot_table/create_response.json'
        )

    def test_plot_table_create_with_all_fields(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=data_helper.generate_random_string('Тестовая делянка'),
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=data_helper.generate_random_string('Тестовый сорт'),
            comment=data_helper.generate_random_string('Тестовый комментарий'),
            mother=data_helper.generate_random_string('Тестовая мать'),
            father=data_helper.generate_random_string('Тестовый отец'),
            repetitions=REPETITIONS['10'],
        )
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/plot_table/create_response.json'
        )
        assert len(response_data) == REPETITIONS['10']


    def test_plot_table_create_with_space_in_plot_name(
        self, get_token, plastilin_db_api, data_helper
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        plot_name = f' Тестовая делянка с пробелом_{uuid.uuid4()} '
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=plot_name,
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=data_helper.generate_random_string('Тестовый сорт'),
        )
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        assert response_data[0]['plot_name'] == f'{plot_name.strip()}/1', (
            f'Имя делянки {plot_name.strip()} не соответствует '
            f'имени делянки в ответе {response_data[0]["plot_name"]}!'
        )

    def test_plot_table_create_with_space_in_line_name(
        self, get_token, plastilin_db_api, data_helper
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        line_name = f' Тестовый сорт с пробелом_{uuid.uuid4()} '
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=data_helper.generate_random_string('Тестовая делянка'),
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=line_name,
        )
        assert response.status == HTTPStatus.CREATED
        response_data = response.json()
        assert response_data[0]['line_name'] == f'{line_name.strip()}', (
            f'Имя сорта {line_name.strip()} не соответствует '
            f'имени сорта в ответе {response_data[0]["line_name"]}!'
        )


class TestPlotTableCreateNegative:
    @pytest.mark.parametrize(
        'plot_name, expected_error',
        [
            ('', 'This field may not be blank.'),
            (None, 'This field is required.'),
        ],
    )
    def test_plot_table_create_with_invalid_plot_name(
        self, get_token, plastilin_db_api, data_helper, plot_name, expected_error
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=plot_name,
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=data_helper.generate_random_string('Тестовый сорт'),
        )
        assert response.status == HTTPStatus.BAD_REQUEST
        assert response.json()['plot_name'] == [expected_error]

    @pytest.mark.parametrize(
        'line_name, expected_error',
        [
            ('', 'This field may not be blank.'),
            (None, 'This field is required.'),
            ('a' * 256, 'Ensure this field has no more than 255 characters.'),
            ('!№;;/*-+', 'The line name cannot consist only of special characters.')
        ],
    )
    def test_plot_table_create_with_invalid_line_name(
        self, get_token, plastilin_db_api, data_helper, line_name, expected_error
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=data_helper.generate_random_string('Тестовая делянка'),
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=line_name,
        )
        assert response.status == HTTPStatus.BAD_REQUEST
        if expected_error == 'The line name cannot consist only of special characters.':
            assert response.json()['line_name']['message'] == expected_error
        else:
            assert response.json()['line_name'] == [expected_error]

    @pytest.mark.parametrize(
        'repetitions, expected_error',
        [
            (0, 'Ensure this value is greater than or equal to 1.'),
            (101, 'Ensure this value is less than or equal to 100.'),
        ],
    )
    def test_plot_table_create_with_invalid_repetitions(
        self, get_token, plastilin_db_api, data_helper, repetitions, expected_error 
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=data_helper.generate_random_string('Тестовая делянка'),
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=data_helper.generate_random_string('Тестовый сорт'),
            repetitions=repetitions,
        )
        assert response.status == HTTPStatus.BAD_REQUEST
        assert response.json()['repetitions'] == [expected_error]


    @pytest.mark.parametrize(
        'width, length, expected_error',
        [
            ('one', 'two', 'A valid number is required.'),
        ],
    )
    def test_plot_table_create_with_invalid_width_and_length(
        self, get_token, plastilin_db_api, data_helper, width, length, expected_error
    ):
        token = get_token('standalone_user')
        spec_id, field_id, _ = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['wheat']['russian_name'],
            field_name=FIELDS['field_1']['field_name'],
            year=FIELDS['field_1']['year'],
            region=FIELDS['field_1']['region'],
        )
        response = plastilin_db_api.create_plot_table(
            token=token,
            plot_name=data_helper.generate_random_string('Тестовая делянка'),
            field=field_id,
            year=FIELDS['field_1']['year'],
            spec_id=spec_id,
            line_name=data_helper.generate_random_string('Тестовый сорт'),
            width=width,
            length=length,
        )
        assert response.status == HTTPStatus.BAD_REQUEST

        assert response.json()['width'] == [expected_error]
        assert response.json()['length'] == [expected_error]