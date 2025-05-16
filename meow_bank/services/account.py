from traceback import format_exc

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from meow_bank.api.exceptions import BusinessLogicError, ResourceNotFoundError
from meow_bank.core.constants import UUIDStr
from meow_bank.core.logging import log
from meow_bank.db.models import Account, Customer
from meow_bank.schemas import (
    AccountCreate,
    AccountResponse,
    AccountWithTransfers,
)
from meow_bank.services.balance import BalanceService
from meow_bank.services.transfer import TransferService


class AccountService:
    def __init__(self, db: Session):
        self.db = db
        self.transfer_service = TransferService(db)
        self.balance_service = BalanceService(db)

    def create_account(self, account_data: AccountCreate) -> AccountResponse:
        """Create a new account with an initial deposit."""
        try:
            customer = self.db.get(Customer, account_data.customer_id)
            if not customer:
                raise ResourceNotFoundError("Customer not found")

            account = Account(customer_id=account_data.customer_id)
            self.db.add(account)
            self.db.flush()

            # Create initial deposit as a system transfer
            if account_data.initial_deposit > 0:
                self.transfer_service.create_system_transfer(
                    account.id,
                    account_data.initial_deposit,
                )

            self.db.commit()

            balance = self.balance_service.get_balance_by_account_id(account.id)

            return AccountResponse(
                id=account.id,
                customer_id=account.customer_id,
                created_at=account.created_at,
                balance=balance,
            )
        except ResourceNotFoundError:
            raise
        except Exception as e:
            log.error(
                "Failed to create account",
                extra={
                    "error": str(format_exc(e)),
                    "account_data": account_data.model_dump(),
                },
            )
            raise BusinessLogicError(f"Failed to create account: {str(e)}") from e

    def get_account_by_id(self, account_id: UUIDStr) -> AccountResponse | None:
        """Get account details by ID."""
        account = self.db.get(Account, account_id)
        if not account:
            return None

        balance = self.balance_service.get_balance_by_account_id(account_id)
        return AccountResponse(
            id=account.id,
            customer_id=account.customer_id,
            created_at=account.created_at,
            balance=balance,
        )

    def get_account_with_transfers_by_id(
        self, account_id: UUIDStr
    ) -> AccountWithTransfers | None:
        """Get account details with transfer history."""

        stmt = (
            select(Account)
            .options(
                selectinload(Account.sent_transfers),
                selectinload(Account.received_transfers),
            )
            .where(Account.id == account_id)
        )
        account = self.db.execute(stmt).scalars().first()
        if not account:
            return None

        balance = self.balance_service.get_balance_by_account_id(account_id)

        return AccountWithTransfers(
            id=account.id,
            customer_id=account.customer_id,
            created_at=account.created_at,
            balance=balance,
            sent_transfers=account.sent_transfers,
            received_transfers=account.received_transfers,
        )

    def get_accounts_by_ids(self, account_ids: list[UUIDStr]) -> list[AccountResponse]:
        stmt = (
            select(Account)
            .filter(Account.id.in_(account_ids))
            .order_by(Account.created_at.desc())
        )
        accounts = self.db.execute(stmt).scalars().all()
        if not accounts:
            return []

        balance_map = self.balance_service.get_balances_by_account_ids(account_ids)

        return [
            AccountResponse(
                id=account.id,
                customer_id=account.customer_id,
                created_at=account.created_at,
                balance=balance_map.get(account.id, 0),
            )
            for account in accounts
        ]
