from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.constants import API_ENDPOINTS


class SaveFastqFileAPI(BaseAPI):
    def save_fastq_file(
        self, 
        token: str, 
        key: str, 
        original_name: str, 
        plot_id: int, 
        paired: bool
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        payload = {
            "key": key,
            "original_name": original_name,
            "plot_id": plot_id,
            "paired": paired,
        }

        return self.context.post(
            API_ENDPOINTS['plastilin_db']['save_fastq_file'],
            headers=headers,
            data=payload,
        )