from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from meow_bank.api.exceptions import (
    BusinessLogicError,
    ResourceNotFoundError,
    ValidationError,
)
from meow_bank.core.constants import UUIDStr
from meow_bank.db.database import get_db
from meow_bank.schemas import TransferCreate, TransferResponse
from meow_bank.services import TransferService

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("/", response_model=TransferResponse)
def create_transfer(
    transfer_data: TransferCreate,
    db: Session = Depends(get_db),
) -> TransferResponse:
    """Create a new transfer between accounts."""
    try:
        transfer_service = TransferService(db)
        return transfer_service.create_transfer(transfer_data)
    except ResourceNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
    except (ValidationError, BusinessLogicError) as err:
        raise HTTPException(status_code=400, detail=str(err)) from err


@router.get("/{transfer_id}", response_model=TransferResponse)
def get_transfer_by_id(
    transfer_id: UUIDStr,
    db: Session = Depends(get_db),
) -> TransferResponse:
    """Get transfer details by ID."""
    transfer_service = TransferService(db)
    transfer = transfer_service.get_transfer_by_id(transfer_id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return transfer
