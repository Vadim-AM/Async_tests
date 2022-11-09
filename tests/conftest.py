# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Generator, Dict

import pytest
import pytest_asyncio
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient
from main import app


@pytest_asyncio.fixture()
async def a_client() -> Generator:
    async with AsyncClient(app=app, base_url='http://localhost:8081/api/v1/') as async_client:
        yield async_client


@pytest.fixture()
def tokens() -> Dict:
    data = {
        'pincode': 111222333,  # correct pin
    }
    access_token = AuthJWT.create_access_token(AuthJWT(), data['pincode'], user_claims=data)
    refresh_token = AuthJWT.create_refresh_token(AuthJWT(), data['pincode'], user_claims=data)
    return {"access_token": access_token, "refresh_token": refresh_token}
