from fastapi import status

from meow_bank.core.config import settings
from meow_bank.db.models import Customer


def test_protected_endpoint_no_auth(test_client):
    """Protected endpoints should require API key."""
    test_client.headers = {}
    response = test_client.post("/api/customers/", json={"name": "Test Customer"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not validate API key" in response.json()["detail"]


def test_protected_endpoint_invalid_auth(test_client):
    """Protected endpoints should reject invalid API key."""
    test_client.headers = {"X-API-Key": "invalid_key"}
    response = test_client.post("/api/customers/", json={"name": "Test Customer"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not validate API key" in response.json()["detail"]


def test_protected_endpoint_valid_auth(test_client, db_session):
    """Protected endpoints should accept valid API key."""
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    test_client.headers = {"X-API-Key": settings.MEOW_BANK_API_KEY}
    response = test_client.get(f"/api/customers/{customer.id}")
    assert response.status_code == status.HTTP_200_OK
