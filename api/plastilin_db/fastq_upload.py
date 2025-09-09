from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper


class FastqUploadAPI(BaseAPI):
    def fastq_upload(
        self, 
        token: str, 
        fastq_url: str,
        name: str, 
        file_path: str,
        user_id: str,
        file_name: str,
        key: str = None,
        policy: str = None,
        signature: str = None,
        access_key_id: str = "plastilin-app-rw"
    ) -> APIResponse:
        """
        Загружает FASTQ файл в MinIO
        
        Args:
            token: JWT токен авторизации
            name: Имя файла
            file_path: Путь к файлу для загрузки
            user_id: ID пользователя
            key: Ключ файла в MinIO (если не указан, генерируется автоматически)
            policy: Политика доступа (если не указана, генерируется автоматически)
            signature: Подпись (если не указана, генерируется автоматически)
            access_key_id: ID ключа доступа AWS
        """
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {token}'

        multipart = {
            'key': key,
            'x-amz-meta-user_id': user_id,
            'x-amz-meta-name': name,
            'AWSAccessKeyId': access_key_id,
            'policy': policy,
            'signature': signature,
            'file': None,
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
            fastq_url,
            headers=headers,
            multipart=multipart,
        )