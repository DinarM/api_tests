from utils.api.constants import TEST_CULTURES, FIELDS
from http import HTTPStatus


class TestDownloadPlotData:
    def test_download_plot_data_success(self, get_token, plastilin_db_api, data_helper):
        token = get_token('company_1.head_of_company')

        spec_id, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        response = plastilin_db_api.download_plot_data(
            token=token,
            spec_id=spec_id,
            year_id=year_id,
        )
        assert response.status == HTTPStatus.OK

        assert response.headers.get('content-type', '').startswith(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        assert len(response.body()) > 0  
        assert response.headers.get('content-disposition', '').startswith('attachment') 