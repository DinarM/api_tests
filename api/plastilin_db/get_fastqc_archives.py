from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class GetFastqcArchivesAPI(BaseAPI):
    def get_fastqc_archives(self, token: str) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['get_fastqc_archives'],
            headers=headers,
        )