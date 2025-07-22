import time
from http import HTTPStatus

from utils.api.constants import BAD_REQUEST_MESSAGE


class TestLogin:
    def test_login_invalid_credentials(self, auth_api):
        response = auth_api.login(
            username='test',
            password='test',
        )
        assert response.status == HTTPStatus.BAD_REQUEST
        assert response.json()['message'] == BAD_REQUEST_MESSAGE['invalid_credentials']
        assert response.json()['remainingAttempts'] == 2

        response = auth_api.login(
            username='test',
            password='test',
        )
        assert response.status == HTTPStatus.BAD_REQUEST
        assert response.json()['message'] == BAD_REQUEST_MESSAGE['invalid_credentials']
        assert response.json()['remainingAttempts'] == 1
        

    def test_login_auth_locked(self, auth_api):
        for _ in range(3):
            response = auth_api.login(
                username='test',
                password='test',
            )
        assert response.status == HTTPStatus.FORBIDDEN
        assert response.json()['message'] == BAD_REQUEST_MESSAGE['auth_locked']
        assert response.json()['blockTimeSeconds'] == BAD_REQUEST_MESSAGE['block_time']

        time.sleep(BAD_REQUEST_MESSAGE['block_time'])
        response = auth_api.login(
            username='test',
            password='test',
        )
        assert response.status == HTTPStatus.BAD_REQUEST
        assert response.json()['message'] == BAD_REQUEST_MESSAGE['invalid_credentials']
        assert response.json()['remainingAttempts'] == 2

