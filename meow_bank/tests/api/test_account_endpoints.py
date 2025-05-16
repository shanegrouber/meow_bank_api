from fastapi import status

from meow_bank.db.models import Account, Customer


def test_create_account(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account_data = {"customer_id": str(customer.id), "initial_deposit": 100.0}

    response = test_client.post("/accounts/", json=account_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["customer_id"] == str(customer.id)
    assert data["balance"] == 100.0  # noqa: PLR2004
    assert "id" in data
    assert "created_at" in data


def test_create_account_invalid_customer(test_client):
    account_data = {
        "customer_id": "00000000-0000-0000-0000-000000000000",
        "initial_deposit": 100.0,
    }

    response = test_client.post("/accounts/", json=account_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_account(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    response = test_client.get(f"/accounts/{account.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(account.id)
    assert data["customer_id"] == str(customer.id)
    assert "balance" in data


def test_get_account_not_found(test_client):
    response = test_client.get("/accounts/00000000-0000-0000-0000-000000000000")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_account_with_transfers(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    response = test_client.get(f"/accounts/{account.id}/transfers")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(account.id)
    assert data["customer_id"] == str(customer.id)
    assert "balance" in data
    assert "sent_transfers" in data
    assert "received_transfers" in data
    assert isinstance(data["sent_transfers"], list)
    assert isinstance(data["received_transfers"], list)
