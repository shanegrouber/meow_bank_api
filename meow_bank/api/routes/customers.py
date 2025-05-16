from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from meow_bank.core.constants import UUIDStr
from meow_bank.db.database import get_db
from meow_bank.schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerWithAccountIds,
    CustomerWithAccounts,
)
from meow_bank.services import AccountService, CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    """Create a new customer."""
    customer_service = CustomerService(db)
    try:
        return customer_service.create_customer(customer_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{customer_id}", response_model=CustomerWithAccountIds)
def get_customer(
    customer_id: UUIDStr,
    db: Session = Depends(get_db),
) -> CustomerWithAccountIds:
    """Get customer details by ID."""
    customer_service = CustomerService(db)
    customer = customer_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/{customer_id}/accounts", response_model=CustomerWithAccounts)
def get_customer_with_accounts(
    customer_id: UUIDStr,
    db: Session = Depends(get_db),
) -> CustomerWithAccounts:
    """Get customer details with their accounts."""
    customer_service = CustomerService(db)
    customer = customer_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    account_service = AccountService(db)

    accounts = account_service.get_accounts_by_ids(customer.account_ids)

    return CustomerWithAccounts(
        id=customer.id,
        name=customer.name,
        created_at=customer.created_at,
        accounts=accounts,
    )
