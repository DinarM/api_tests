from http import HTTPStatus

from utils.api.constants import FIELDS, TEST_CULTURES


class TestExportToExcel:
    def test_export_to_excel_success(self, get_token, plastilin_db_api, data_helper):
        token = get_token('company_1.head_of_company')

        _, field_id, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )

        response = plastilin_db_api.export_to_excel(
            token=token,
            field_id=field_id,
            year_id=year_id,
        )

        assert response.status == HTTPStatus.OK

        assert response.headers.get('content-type', '').startswith(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        assert len(response.body()) > 0