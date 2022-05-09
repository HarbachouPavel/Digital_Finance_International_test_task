import pytest
from api_service_central_bank.api_service import APIService


@pytest.fixture(autouse=True)
def api_service():
    return APIService()
