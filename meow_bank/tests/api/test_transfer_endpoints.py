from fastapi import status

from meow_bank.db.models import Account, Customer
from meow_bank.services.transfer import TransferService


def test_create_transfer(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    source_account = Account(customer_id=customer.id)
    dest_account = Account(customer_id=customer.id)
    db_session.add_all([source_account, dest_account])
    db_session.commit()

    transfer_service = TransferService(db_session)
    transfer_service.create_system_transfer(source_account.id, 100.0)

    transfer_data = {
        "from_account_id": str(source_account.id),
        "to_account_id": str(dest_account.id),
        "amount": 50.0,
    }

    response = test_client.post("/transfers/", json=transfer_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["from_account_id"] == str(source_account.id)
    assert data["to_account_id"] == str(dest_account.id)
    assert data["amount"] == 50.0  # noqa: PLR2004
    assert "id" in data
    assert "created_at" in data


def test_create_transfer_same_account(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    transfer_data = {
        "from_account_id": str(account.id),
        "to_account_id": str(account.id),
        "amount": 50.0,
    }

    response = test_client.post("/transfers", json=transfer_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Cannot transfer to the same account" in response.json()["detail"]


def test_create_transfer_account_not_found(test_client):
    transfer_data = {
        "from_account_id": "00000000-0000-0000-0000-000000000000",
        "to_account_id": "00000000-0000-0000-0000-000000000000",
        "amount": 50.0,
    }

    response = test_client.post("/transfers/", json=transfer_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Sender account not found" in response.json()["detail"]


def test_get_transfer(test_client, db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    source_account = Account(customer_id=customer.id)
    dest_account = Account(customer_id=customer.id)
    db_session.add_all([source_account, dest_account])
    db_session.commit()

    transfer_service = TransferService(db_session)
    transfer_service.create_system_transfer(source_account.id, 100.0)

    transfer_data = {
        "from_account_id": str(source_account.id),
        "to_account_id": str(dest_account.id),
        "amount": 50.0,
    }
    create_response = test_client.post("/transfers/", json=transfer_data)
    transfer_id = create_response.json()["id"]
    response = test_client.get(f"/transfers/{transfer_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == transfer_id
    assert data["from_account_id"] == str(source_account.id)
    assert data["to_account_id"] == str(dest_account.id)
    assert data["amount"] == 50.0  # noqa: PLR2004
    assert "created_at" in data


def test_get_transfer_not_found(test_client):
    response = test_client.get("/transfers/00000000-0000-0000-0000-000000000000")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Transfer not found" in response.json()["detail"]
