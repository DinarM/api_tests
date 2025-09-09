from http import HTTPStatus


class TestGetFastqcArchives:
    def test_get_fastqc_archives_success(self, get_token, plastilin_db_api, schema_validator):
        token = get_token('company_1.head_of_company')

        response = plastilin_db_api.get_fastqc_archives(
            token=token,
        )
        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/get_fastqc_archives/get_response.json'
        )