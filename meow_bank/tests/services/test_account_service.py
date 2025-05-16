from datetime import datetime
from uuid import UUID

import pytest

from meow_bank.api.exceptions import ResourceNotFoundError
from meow_bank.db.models import Account, Customer
from meow_bank.schemas import AccountCreate
from meow_bank.services.account import AccountService


def test_create_account(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account_service = AccountService(db_session)
    account_data = AccountCreate(customer_id=str(customer.id), initial_deposit=100)

    result = account_service.create_account(account_data)

    assert result.customer_id == str(customer.id)
    assert result.balance == 100  # noqa: PLR2004
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)

    db_account = db_session.query(Account).filter(Account.id == result.id).first()
    assert db_account is not None
    assert db_account.customer_id == customer.id


def test_create_account_invalid_customer(db_session):
    account_service = AccountService(db_session)
    non_existent_customer_id = str(UUID(int=0))
    account_data = AccountCreate(
        customer_id=non_existent_customer_id, initial_deposit=100.0
    )

    with pytest.raises(ResourceNotFoundError):
        account_service.create_account(account_data)


def test_get_account_by_id(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    account_service = AccountService(db_session)
    result = account_service.get_account_by_id(str(account.id))

    assert result is not None
    assert result.id == str(account.id)
    assert result.customer_id == str(customer.id)


def test_get_account_by_id_not_found(db_session):
    account_service = AccountService(db_session)
    non_existent_id = str(UUID(int=0))

    result = account_service.get_account_by_id(non_existent_id)

    assert result is None


def test_get_account_with_transfers(db_session):
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    account = Account(customer_id=customer.id)
    db_session.add(account)
    db_session.commit()

    account_service = AccountService(db_session)

    result = account_service.get_account_with_transfers_by_id(str(account.id))

    assert result is not None
    assert result.id == str(account.id)
    assert result.customer_id == str(customer.id)
    assert isinstance(result.sent_transfers, list)
    assert isinstance(result.received_transfers, list)
