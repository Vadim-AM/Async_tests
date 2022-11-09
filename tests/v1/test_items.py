import asyncio
from unittest.mock import patch, MagicMock

import pytest
from httpx import AsyncClient
from tests.data_test import Activate, ItemData


class TestItems:
    ITEM_DATA = ItemData.DATA_LIST
    ACTIVATE_DATA = Activate.DATA_LIST

    @patch('app.routers.items.orders')
    @patch('app.routers.items.database_access_check')
    @pytest.mark.parametrize('db_check_value, item_status, code, expected_response', ITEM_DATA)
    @pytest.mark.asyncio
    async def test_check_status(self, mock_db_check: MagicMock, status: MagicMock, tokens: dict, db_check_value: bool,
                                item_status: any, code: int, expected_response: tuple, a_client: AsyncClient):
        access_token = tokens['access_token']
        mock_db_check.return_value = db_check_value
        mock_orders = MagicMock()
        mock_orders.return_value = item_status
        status.find_one.return_value = asyncio.Future()
        status.find_one.return_value.set_result(mock_orders.return_value)
        response = await a_client.get(f'check_status?item_number=129',
                                      headers={'Authorization': f'Bearer {access_token}'})

        assert response.status_code == code, f'Server returned {response.status_code} code'
        assert response.json() == expected_response, response.json()

    @patch('app.routers.items.datetime.datetime')
    @patch('app.routers.items.orders')
    @patch('app.routers.items.call_producer')
    @patch('app.routers.items.database_access_check')
    @pytest.mark.parametrize('item, db_check_value, item_status, code, expected_response', ACTIVATE_DATA)
    @pytest.mark.asyncio
    async def test_activate_item(self, db_check: MagicMock, mock_producer: MagicMock, status: MagicMock,
                                 mock_time: MagicMock, tokens: dict, db_check_value: bool, item_status: any,
                                 item: dict, code: int, expected_response: tuple, a_client: AsyncClient):
        access_token = tokens['access_token']
        db_check.return_value = db_check_value
        mock_producer.return_value = True
        mock_orders = MagicMock()
        mock_orders.return_value = item_status
        status.find_one.return_value = asyncio.Future()
        status.find_one.return_value.set_result(mock_orders.return_value)
        mock_time.now.return_value = '1945-07-16'
        response = await a_client.post('activate', headers={'Authorization': f'Bearer {access_token}'},
                                       json=item)
        assert response.status_code == code, response.text
        assert response.json() == expected_response, response.json()
