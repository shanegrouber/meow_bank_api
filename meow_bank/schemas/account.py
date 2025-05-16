from datetime import datetime

from pydantic import Field, NonNegativeFloat

from meow_bank.core.constants import UUIDStr
from meow_bank.schemas.base import ORMBase
from meow_bank.schemas.transfer import TransferResponse


class AccountBase(ORMBase):
    customer_id: UUIDStr


class AccountCreate(AccountBase):
    initial_deposit: NonNegativeFloat = Field(
        ..., description="Initial deposit amount (must be non-negative)"
    )


class AccountResponse(AccountBase):
    id: UUIDStr
    created_at: datetime
    balance: NonNegativeFloat = Field(..., description="Current account balance")


class AccountWithTransfers(AccountResponse):
    sent_transfers: list[TransferResponse] = Field(default_factory=list)
    received_transfers: list[TransferResponse] = Field(default_factory=list)
