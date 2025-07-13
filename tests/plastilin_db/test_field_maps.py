from http import HTTPStatus

import pytest

from utils.api.constants import FIELDS, TEST_CULTURES


class TestFieldMapsGet:
    def test_field_maps_get_success(self, get_token, plastilin_db_api, data_helper, schema_validator):
        token = get_token('head_of_company_company_1')
        _, field_id, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        response = plastilin_db_api.get_field_maps(token=token, year_id=year_id, field_id=field_id)
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/field_maps/get_response.json'
        )