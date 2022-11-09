from unittest.mock import patch, MagicMock

import pytest
from app.core.models import accounts_schemas
from httpx import AsyncClient

from tests.data_test import SignUp, LogIn, MainPage


class TestAccounts:
    LOG_IN_DATA_LIST = LogIn.DATA_LIST
    SIGN_UP_DATA_LIST = SignUp.DATA_LIST
    MAIN_DATA_LIST = MainPage.DATA_LIST

    @pytest.mark.parametrize('url, code, expected_response', MAIN_DATA_LIST)
    @pytest.mark.asyncio
    async def test_read_main(self, url: str, code: int, expected_response: tuple, a_client: AsyncClient):
        """takes variables and list of tuples as params and calling them one by one"""
        response = await a_client.get(url)
        assert response.status_code == code, f'Server returned {response.status_code} code'
        assert response.json() == expected_response, response.json()

    @patch('app.routers.accounts.create_user')
    @patch('app.routers.accounts.get_terminal_by_pincode')
    @pytest.mark.parametrize('data, code, expected_response', SIGN_UP_DATA_LIST)
    @pytest.mark.asyncio
    async def test_create_terminal(self, get_terminal_by_pin_mock: MagicMock, mock_create_user: MagicMock, data: dict,
                                   code: int, expected_response: tuple,
                                   a_client: AsyncClient):
        if code == 200:  # mock patches for creating terminal
            get_terminal_by_pin_mock.return_value = None
            mock_create_user.return_value = True

        response = await a_client.post('signup', json=data)

        assert response.status_code == code, f'Server returned {response.status_code} code'
        assert response.json() == expected_response, response.json()

    @patch('app.routers.accounts.get_terminal_by_pincode')
    @pytest.mark.asyncio
    async def test_login_positive(self, get_terminal_by_pin_mock: MagicMock, a_client: AsyncClient):
        data = {
            'pincode': '111222333',  # correct
        }
        get_terminal_by_pin_mock.return_value = accounts_schemas.LoginUser  # mock User instance
        get_terminal_by_pin_mock.return_value.is_active = True  # add field to User
        get_terminal_by_pin_mock.return_value.terminal = data['pincode']  # create .terminal in User

        response = await a_client.post('login', json=data)

        assert response.status_code == 200, response.text
        assert isinstance(response.json()['access_token'], str), response.json()['access_token']
        assert isinstance(response.json()['refresh_token'], str), response.json()['refresh_token']

    @patch('app.routers.accounts.get_terminal_by_pincode')
    @pytest.mark.parametrize('data, code, expected_response', LOG_IN_DATA_LIST)
    @pytest.mark.asyncio
    async def test_login_negative(self, get_terminal_by_pin_mock: MagicMock, data: dict, code: int,
                                  expected_response: tuple,
                                  a_client: AsyncClient):
        if expected_response == {'detail': 'Pin-code not found'}:  # pin code does not exist in DB
            get_terminal_by_pin_mock.return_value = False
        if expected_response == {'detail': 'Inactive terminal'}:  # pin exist but isn't active
            get_terminal_by_pin_mock.return_value = accounts_schemas.LoginUser
            get_terminal_by_pin_mock.return_value.is_active = False

        response = await a_client.post('login', json=data)

        assert response.status_code == code, response.text
        assert response.json() == expected_response, response.json()

    @pytest.mark.asyncio
    async def test_refresh(self, tokens: dict, a_client: AsyncClient):
        response = await a_client.post('refresh',
                                       headers={'Authorization': f"Bearer {tokens['refresh_token']}"})

        assert response.status_code == 200, response.text
        assert response.json()['access_token'] is not None, response.json()
