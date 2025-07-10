from utils.api.constants import TEST_CULTURES, FIELDS
from http import HTTPStatus

class TestPerformTTestMultipleGet:
    def test_perform_t_test_multiple_get(self, get_token, plastilin_db_api, data_helper, schema_validator):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['barley']['russian_name'], field_name=FIELDS['field_2']['field_name'], year=FIELDS['field_2']['year'], region=FIELDS['field_2']['region'])
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(token, year_ids, feature, control_plot, control_plot_year_id)
        print(response)
        assert response.status == HTTPStatus.OK
        schema_validator.assert_valid_response(
            response.json(), 
            'plastilin_db/perform_t_test_multiple/get_response.json'
        )
