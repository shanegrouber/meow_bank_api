from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from meow_bank.api.exceptions import BusinessLogicError, ResourceNotFoundError
from meow_bank.core.constants import UUIDStr
from meow_bank.db.database import get_db
from meow_bank.schemas import (
    AccountCreate,
    AccountResponse,
    AccountWithTransfers,
)
from meow_bank.services import AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/", response_model=AccountResponse)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
) -> AccountResponse:
    """Create a new account with an initial deposit."""
    try:
        account_service = AccountService(db)
        return account_service.create_account(account_data)
    except ResourceNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except BusinessLogicError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err


@router.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(
    account_id: UUIDStr,
    db: Session = Depends(get_db),
) -> AccountResponse:
    """Get account details with current balance."""
    account_service = AccountService(db)
    account = account_service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("/{account_id}/transfers", response_model=AccountWithTransfers)
def get_account_with_transfers_by_id(
    account_id: UUIDStr,
    db: Session = Depends(get_db),
) -> AccountWithTransfers:
    """Get account details with transfer history."""
    account_service = AccountService(db)
    account = account_service.get_account_with_transfers_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
