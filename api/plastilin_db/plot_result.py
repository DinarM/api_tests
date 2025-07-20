from typing import Optional

from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class PlotResultAPI(BaseAPI):
    def create_plot_result(
        self,
        token: Optional[str] = None,
        file_path: Optional[str] = None,
        file_name: Optional[str] = None,
        spec_id: Optional[int] = None,
        max_length_per_list: int = 20,
        sort_method: int = 1,
    ) -> APIResponse:
        """
        Загрузка кастомного файла с результатами делянок

        Args:
            token: Bearer токен
            file_path: Путь к файлу для загрузки
            spec_id: ID культуры
            max_length_per_list: Максимальная длина списка
            sort_method: Метод сортировки
        """

        if token:
            headers = {'Authorization': token}

        multipart = {
            "spec_id": str(spec_id),
            "max_length_per_list": str(max_length_per_list),
            "sort_method": str(sort_method),
            "file": None,
        } 

        if file_path:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
                multipart['file'] = {
                    "name": file_name,
                    "mimeType": (
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    ),
                    "buffer": file_bytes,
                }
        
        multipart = APIHelper.filter_none_values(multipart)

        return self.context.post(
            API_ENDPOINTS['plastilin_db']['plot_result'],
            multipart=multipart,
            headers=headers,
        )