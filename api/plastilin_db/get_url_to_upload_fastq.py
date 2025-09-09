from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class GetUrlToUploadFastqAPI(BaseAPI):
    def get_url_to_upload_fastq(self, token: str, name: Optional[str] = None) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token

        params = {
            'name': name,
        }

        APIHelper.filter_none_values(params)

        return self.context.get(
            API_ENDPOINTS['plastilin_db']['get_url_to_upload_fastq'],
            params=params,
            headers=headers,
        )