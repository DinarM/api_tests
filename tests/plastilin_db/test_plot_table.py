from http import HTTPStatus

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
        assert response_data, 'Ответ пустой'
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
