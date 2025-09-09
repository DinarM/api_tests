from http import HTTPStatus

from utils.api.constants import FIELDS, TEST_CULTURES


# TODO тело запроса доделать после фиксов на стейдже
class TestAddMultiple:
    def test_add_multiple_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_3']['field_name'],
            year=FIELDS['field_3']['year'],
            region=FIELDS['field_3']['region'],
        )

        response = plastilin_db_api.plot_final_results_add_multiple(
            token=token,
            plot=206471,
            feature='test',
            unit='test',
            value='100',
            year_id=year_id,
        )
        assert response.status == HTTPStatus.CREATED

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/add_multiple/create_response.json'
        )