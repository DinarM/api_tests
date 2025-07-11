from http import HTTPStatus

from utils.api.constants import REGIONS, TEST_CULTURES


class TestFieldTableGet:
    """
    Тесты для получения таблицы полей
    """

    def test_get_field_table_success(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест успешного получения таблицы полей
        """
        token = get_token('head_of_company_company_1')
        spec_id = data_helper.get_or_create_spec_id_by_name(
            token=token, russian_name=TEST_CULTURES['wheat']['russian_name']
        )
        response = plastilin_db_api.get_field_table(token=token, spec_id=spec_id)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/field_table/get_response.json'
        )


class TestFieldTableCreate:
    """
    Тесты для создания таблицы полей
    """

    def test_create_field_table_success(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест успешного создания таблицы полей
        """
        token = get_token('head_of_company_company_1')
        spec_id = data_helper.get_or_create_spec_id_by_name(
            token=token, russian_name=TEST_CULTURES['wheat']['russian_name']
        )
        field_name = data_helper.generate_random_string(name='Тестовое поле')
        response = plastilin_db_api.create_field_table(
            token=token, spec_id=spec_id, field_name=field_name, region=REGIONS['Амурская область']
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/field_table/create_response.json'
        )
