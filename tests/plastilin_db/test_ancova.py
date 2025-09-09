from http import HTTPStatus

from utils.api.constants import FIELDS, TEST_CULTURES


class TestAncova:
    def test_ancova_success(self, get_token, plastilin_db_api, data_helper, schema_validator):
        token = get_token('company_1.head_of_company')

        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )

        quantitative_features = plastilin_db_api.quantitative_features(
            token=token,
            year_id=year_id,
        )
        quantitative_features_data = quantitative_features.json()

        dependent_var = quantitative_features_data[0]['feature']
        covariate_var = quantitative_features_data[1]['feature']

        qualitative_features = plastilin_db_api.qualitative_features(
            token=token,
            year_id=year_id,
        )
        qualitative_features_data = qualitative_features.json()
        
        group_var = qualitative_features_data[0]['feature']

        response = plastilin_db_api.ancova(
            token=token,
            year_id=year_id,
            dependent_var=dependent_var,
            group_var=group_var,
            covariate_var=covariate_var,
        )
        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/ancova/get_response.json'
        )