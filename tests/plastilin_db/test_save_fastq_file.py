from http import HTTPStatus

import pytest


@pytest.mark.skip(reason='Not implemented')
class TestSaveFastqFile:
    def test_save_fastq_file_success(self, get_token, plastilin_db_api):
        token = get_token('company_1.head_of_company')

        response = plastilin_db_api.save_fastq_file(
            token=token,
            key='59_b341e22f-28c2-49d8-9a80-f5bc2175b1c7_test.zip',
            original_name='dasfasfsa',
            plot_id=2123,
            paired=True,
        )
        assert response.status == HTTPStatus.OK