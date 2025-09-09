from http import HTTPStatus


class TestHarvestTechnologyAddMultiple:
    def test_harvest_technology_add_multiple_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('company_1.head_of_company')

        response = plastilin_db_api.harvest_technology_add_multiple(
            token=token,
            plot=206471,
            feature='test',
            date_planned=None,
            date_real=None,
            comment='test',
        )
        assert response.status == HTTPStatus.CREATED

        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/harvest_technology_add_multiple/create_response.json'
        )
