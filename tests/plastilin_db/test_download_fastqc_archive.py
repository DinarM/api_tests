from http import HTTPStatus

import pytest


@pytest.mark.skip(reason='Not implemented')
class TestDownloadFastqcArchive:
    def test_download_fastqc_archive_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('company_1.head_of_company')

        response = plastilin_db_api.download_fastqc_archive(
            token=token,
            archive_id=1,
        )
        assert response.status == HTTPStatus.OK