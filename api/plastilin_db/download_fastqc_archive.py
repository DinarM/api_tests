from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class DownloadFastqcArchiveAPI(BaseAPI):
    def download_fastqc_archive(self, token: str, archive_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['download_fastqc_archive'] + f'{archive_id}/',
            headers=headers,
        )
