from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from httpx import AsyncClient
from tests.data_test import Statistics

from app.tests.data_test import ToList


class TestStatistics:
    w_date_data = Statistics.W_DATA_LIST
    wo_date_data = Statistics.DATA_WO_DATE

    @patch('app.routers.statistics.orders')
    @patch('app.routers.statistics.database_access_check')
    @pytest.mark.parametrize('db_check_value, data, code, expected_response', w_date_data)
    @pytest.mark.asyncio
    async def test_events_in_planetarium(self, db_check: MagicMock, res_orders: MagicMock, tokens: dict,
                                         db_check_value: bool,
                                         data: dict, code: int, expected_response: tuple, a_client: AsyncClient):
        access_token = tokens['access_token']
        db_check.return_value = db_check_value
        mock_orders = AsyncMock(return_value=ToList())
        res_orders.find.return_value = mock_orders

        response = await a_client.post('statistics/events_with_date',
                                       headers={'Authorization': f"Bearer {access_token}"},
                                       json=data)

        assert response.status_code == code, f'Server returned {response.status_code} code'
        assert response.json() == expected_response, response.json

    @patch('app.routers.statistics.orders')
    @patch('app.routers.statistics.database_access_check')
    @pytest.mark.parametrize('db_check_value, data, code, expected_response', w_date_data)
    @pytest.mark.asyncio
    async def test_events_without_time(self, db_check: MagicMock, res_orders: MagicMock, tokens: dict,
                                       db_check_value: bool,
                                       data: dict, code: int, expected_response: tuple, a_client: AsyncClient):
        access_token = tokens['access_token']
        db_check.return_value = db_check_value
        mock_orders = AsyncMock(return_value=ToList())
        res_orders.find.return_value = mock_orders

        response = await a_client.post('statistics/events_without_date',
                                       headers={'Authorization': f"Bearer {access_token}"},
                                       json=data)

        assert response.status_code == code, f'Server returned {response.status_code} code'
        assert response.json() == expected_response, response.json
