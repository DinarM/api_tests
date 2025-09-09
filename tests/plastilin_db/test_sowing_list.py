from http import HTTPStatus

import pytest

from utils.api.constants import FIELDS, TEST_CULTURES


@pytest.mark.skip(reason='Not implemented')
class TestSowingListCreate:

    @pytest.mark.parametrize('type_of_file', [1, 2, 3, 4])
    def test_sowing_list_create_success(
        self, get_token, plastilin_db_api, data_helper, type_of_file
    ):
        token = get_token('company_1.head_of_company')
        _, field_id, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )

        response = plastilin_db_api.create_sowing_list(
            token=token,
            field_id=field_id,
            type_of_file=type_of_file,
            year_id=year_id,
        )

        assert response.status == HTTPStatus.OK

        assert response.headers.get('content-type', '').startswith(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        assert len(response.body()) > 0
        assert response.headers.get('content-disposition', '').startswith('attachment') 