from http import HTTPStatus

from utils.api.constants import FIELDS, TEST_CULTURES


class TestF1Analyze:
    def test_f1_analyze_success(self, get_token, plastilin_db_api, data_helper, schema_validator):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )

        qualitative_features_response = plastilin_db_api.qualitative_features(
            token=token,
            year_id=year_id,
        )
        qualitative_features_data = qualitative_features_response.json()
        feature = qualitative_features_data[0]['feature']

        response = plastilin_db_api.f1_analyze(
            token=token,
            year_id=year_id,
            feature=feature,
        )
        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/f1_analyze/get_response.json'
        )