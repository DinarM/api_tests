from http import HTTPStatus

import pytest


# TODO доделать тест после фиксов на стейдже
@pytest.mark.skip(reason='Not implemented')
class TestPlotStage:
    def test_plot_stage_success(self, get_token, plastilin_db_api, data_helper):
        token = get_token('company_1.head_of_company')

        response = plastilin_db_api.create_plot_stage(
            token=token,
            plot=206471,
            stage_of_vegetation='test',
            date_of_stage=None,
        )

        assert response.status == HTTPStatus.CREATED

        response_data = response.json()
        
        assert response_data['message'] == 'Этапы участков успешно созданы.'