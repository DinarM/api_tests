from http import HTTPStatus

import pytest


@pytest.mark.skip(reason='Not implemented')
class TestDeleteFastqcFile:
    def test_delete_fastqc_file_success(self, get_token, plastilin_db_api):
        token = get_token('company_1.head_of_company')

        response = plastilin_db_api.delete_fastqc_file(
            token=token,
            archive_id=1,
        )
        assert response.status == HTTPStatus.NO_CONTENT