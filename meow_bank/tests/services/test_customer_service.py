from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from meow_bank.db.models import Customer
from meow_bank.schemas import CustomerCreate
from meow_bank.services.customer import CustomerService


def test_create_customer(db_session):
    customer_service = CustomerService(db_session)
    customer_data = CustomerCreate(name="Test Customer")

    result = customer_service.create_customer(customer_data)

    assert result.name == "Test Customer"
    assert isinstance(result.id, str)
    assert isinstance(result.created_at, datetime)

    db_customer = db_session.query(Customer).filter(Customer.id == result.id).first()
    assert db_customer is not None
    assert db_customer.name == "Test Customer"


def test_create_customer_invalid_name(db_session):
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(name="")  # Empty name should fail

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "string_too_short"
    assert errors[0]["loc"][0] == "name"


def test_get_customer(db_session):
    customer_service = CustomerService(db_session)
    customer = Customer(name="Test Customer")
    db_session.add(customer)
    db_session.commit()

    result = customer_service.get_customer(str(customer.id))

    assert result is not None
    assert result.name == "Test Customer"
    assert result.id == str(customer.id)
    assert isinstance(result.account_ids, list)


def test_get_customer_not_found(db_session):
    customer_service = CustomerService(db_session)
    non_existent_id = str(UUID(int=0))  # Generate a UUID that won't exist

    result = customer_service.get_customer(non_existent_id)

    assert result is None
