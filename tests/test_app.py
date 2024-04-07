import pytest
from core.redis_handler import RedisSingleton
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from unittest import mock


expected_data = [{'id': 1, 'token': 'token1'}, {'id': 2, 'token': 'token2'},
                 {'id': 3, 'token': 'token3'}, {'id': 4, 'token': 'token4'}]

# @pytest.fixture
# async def test_client(mock_acquire):
#     # https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
#     from main import application as app
#     client = TestClient(app)

#     redis_mock = AsyncMock(spec=RedisSingleton)
#     app.dependency_overrides[RedisSingleton] = lambda: redis_mock
#     return client
# mock.patch("core.redis_handler.RedisSingleton.cache", lambda *args, **kwargs: lambda f: f).start()

def test_app_get(client):
    response = client.get("/app/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == expected_data
