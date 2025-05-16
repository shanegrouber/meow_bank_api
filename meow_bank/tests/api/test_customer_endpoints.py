from fastapi import status

from meow_bank.db.models import Customer


def test_create_customer(test_client):
    customer_data = {"name": "Test Customer"}

    response = test_client.post("/customers/", json=customer_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Customer"
    assert "id" in data
    assert "created_at" in data


def test_create_customer_invalid_name(test_client):
    customer_data = {"name": ""}  # Empty name should fail

    response = test_client.post("/customers/", json=customer_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_customer(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    response = test_client.get(f"/customers/{customer.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Test Customer"
    assert data["id"] == str(customer.id)
    assert "account_ids" in data


def test_get_customer_not_found(test_client):
    response = test_client.get("/customers/00000000-0000-0000-0000-000000000000")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_customer_with_accounts(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    response = test_client.get(f"/customers/{customer.id}/accounts")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Test Customer"
    assert data["id"] == str(customer.id)
    assert "accounts" in data
    assert isinstance(data["accounts"], list)
