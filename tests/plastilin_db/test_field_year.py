from http import HTTPStatus

from utils.api.constants import TEST_CULTURES


class TestFieldYearGet:
    """
    Тесты получения данных о полевых годах (field_year)
    """
    
    def test_get_field_year(self, get_token, plastilin_db_api, schema_validator, data_helper):
        """
        Тест получения полевого года по spec_id
        """
        token = get_token()
        
        spec_id = data_helper.get_or_create_spec_id_by_name(token=token, russian_name=TEST_CULTURES['wheat']['russian_name'])

        response = plastilin_db_api.get_field_year(token=token, spec_id=spec_id)

        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data, 
            'plastilin_db/field_year/list_response.json',
            'Получение списка полевых годов'
        )

