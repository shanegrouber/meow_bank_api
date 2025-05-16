from datetime import datetime

from pydantic import Field

from meow_bank.core.constants import UUIDStr
from meow_bank.schemas import AccountResponse
from meow_bank.schemas.base import ORMBase


class CustomerBase(ORMBase):
    name: str = Field(..., min_length=1, max_length=100)


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: UUIDStr
    created_at: datetime


class CustomerWithAccountIds(CustomerResponse):
    account_ids: list[UUIDStr] = Field(default_factory=list)


class CustomerWithAccounts(CustomerResponse):
    accounts: list[AccountResponse] = Field(default_factory=list)
