from datetime import datetime

from pydantic import (
    Field,
    PositiveFloat,
)

from meow_bank.core.constants import UUIDStr
from meow_bank.schemas.base import ORMBase


class TransferBase(ORMBase):
    to_account_id: UUIDStr
    amount: PositiveFloat = Field(..., description="Transfer amount (must be positive)")


class TransferCreate(TransferBase):
    from_account_id: UUIDStr


class TransferResponse(TransferBase):
    id: str
    from_account_id: UUIDStr | None
    created_at: datetime
