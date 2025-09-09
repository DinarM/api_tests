from http import HTTPStatus


class TestGetUrlToUploadFastq:
    def test_get_url_to_upload_fastq_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('company_1.head_of_company')

        response = plastilin_db_api.get_url_to_upload_fastq(
            token=token,
            name='test.zip',
        )
        assert response.status == HTTPStatus.OK

        response_data = response.json()
        
        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/get_url_to_upload_fastq/get_response.json'
        )