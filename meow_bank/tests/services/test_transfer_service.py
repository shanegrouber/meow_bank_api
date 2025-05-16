from datetime import datetime
from uuid import UUID

import pytest

from meow_bank.api.exceptions import (
    BusinessLogicError,
    ResourceNotFoundError,
    ValidationError,
)
from meow_bank.db.models import Account, Customer, Transfer
from meow_bank.schemas import TransferCreate
from meow_bank.services.transfer import TransferService


def test_create_transfer(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    source_account = Account(customer_id=customer.id)
    dest_account = Account(customer_id=customer.id)
    db_session.add_all([source_account, dest_account])
    db_session.commit()

    transfer_service = TransferService(db_session)
    transfer_service.create_system_transfer(source_account.id, 100.0)

    transfer_data = TransferCreate(
        from_account_id=str(source_account.id),
        to_account_id=str(dest_account.id),
        amount=50.0,
    )

    result = transfer_service.create_transfer(transfer_data)

    assert result.from_account_id == str(source_account.id)
    assert result.to_account_id == str(dest_account.id)
    assert result.amount == 50.0  # noqa: PLR2004
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)

    db_transfer = db_session.query(Transfer).filter(Transfer.id == result.id).first()
    assert db_transfer is not None
    assert db_transfer.from_account_id == source_account.id
    assert db_transfer.to_account_id == dest_account.id
    assert db_transfer.amount == 50.0  # noqa: PLR2004


def test_create_transfer_same_account(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    transfer_service = TransferService(db_session)
    transfer_service.create_system_transfer(account.id, 100.0)

    transfer_data = TransferCreate(
        from_account_id=str(account.id),
        to_account_id=str(account.id),
        amount=50.0,
    )

    with pytest.raises(ValidationError) as exc_info:
        transfer_service.create_transfer(transfer_data)

    assert "Cannot transfer to the same account" in str(exc_info.value)


def test_create_transfer_insufficient_funds(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    source_account = Account(customer_id=customer.id)
    dest_account = Account(customer_id=customer.id)
    db_session.add_all([source_account, dest_account])
    db_session.commit()

    transfer_service = TransferService(db_session)
    transfer_service.create_system_transfer(source_account.id, 25.0)

    transfer_data = TransferCreate(
        from_account_id=str(source_account.id),
        to_account_id=str(dest_account.id),
        amount=50.0,
    )

    with pytest.raises(BusinessLogicError) as exc_info:
        transfer_service.create_transfer(transfer_data)

    assert "Insufficient funds" in str(exc_info.value)


def test_create_transfer_account_not_found(db_session):
    transfer_service = TransferService(db_session)
    non_existent_id = str(UUID(int=0))

    transfer_data = TransferCreate(
        from_account_id=non_existent_id, to_account_id=non_existent_id, amount=50.0
    )

    with pytest.raises(ResourceNotFoundError) as exc_info:
        transfer_service.create_transfer(transfer_data)

    assert "Sender account not found" in str(exc_info.value)


def test_create_system_transfer(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    transfer_service = TransferService(db_session)
    result = transfer_service.create_system_transfer(account.id, 100.0)

    assert result.from_account_id is None
    assert result.to_account_id == str(account.id)
    assert result.amount == 100.0  # noqa: PLR2004
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)

    db_transfer = db_session.query(Transfer).filter(Transfer.id == result.id).first()
    assert db_transfer is not None
    assert db_transfer.from_account_id is None
    assert db_transfer.to_account_id == account.id
    assert db_transfer.amount == 100.0  # noqa: PLR2004


def test_get_transfer_by_id(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    transfer_service = TransferService(db_session)
    transfer = transfer_service.create_system_transfer(account.id, 100.0)

    result = transfer_service.get_transfer_by_id(transfer.id)

    assert result is not None
    assert result.id == transfer.id
    assert result.from_account_id is None
    assert result.to_account_id == str(account.id)
    assert result.amount == 100.0  # noqa: PLR2004


def test_get_transfer_by_id_not_found(db_session):
    transfer_service = TransferService(db_session)
    non_existent_id = str(UUID(int=0))

    result = transfer_service.get_transfer_by_id(non_existent_id)

    assert result is None
