from http import HTTPStatus

from utils.api.constants import FIELDS, TEST_CULTURES


class TestCorrelation:
    def test_correlation_success(self, get_token, plastilin_db_api, data_helper, schema_validator):
        token = get_token('company_1.head_of_company')

        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )

        features = []

        quantitative_features = plastilin_db_api.quantitative_features(
            token=token,
            year_id=year_id,
        )
        quantitative_features_data = quantitative_features.json()
        features.extend([feature['feature'] for feature in quantitative_features_data[:2]])

        features_str = ','.join(features)

        response = plastilin_db_api.correlation(
            token=token,
            year_id=year_id,
            features=features_str,
        )
        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/correlation/get_response.json'
        )