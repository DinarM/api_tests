from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class DeleteFastqcFileAPI(BaseAPI):
    def delete_fastqc_file(self, token: str, archive_id: int) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        return self.context.delete(
            API_ENDPOINTS['plastilin_db']['delete_fastqc_file'] + f'{archive_id}/',
            headers=headers,
        )