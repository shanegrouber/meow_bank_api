from traceback import format_exc

from sqlalchemy.orm import Session

from meow_bank.api.exceptions import (
    BusinessLogicError,
    ResourceNotFoundError,
    ValidationError,
)
from meow_bank.core.constants import UUIDStr
from meow_bank.core.logging import log
from meow_bank.db.models import Account, Transfer
from meow_bank.schemas import TransferCreate, TransferResponse
from meow_bank.services.balance import BalanceService


class TransferService:
    def __init__(self, db: Session):
        self.db = db
        self.balance_service = BalanceService(db)

    def create_transfer(self, transfer_data: TransferCreate) -> TransferResponse:
        """Create a new transfer between accounts."""
        try:
            with self.db.begin_nested():
                source_account = self.db.get(Account, transfer_data.from_account_id)
                if not source_account:
                    raise ResourceNotFoundError("Sender account not found")

                if transfer_data.from_account_id == transfer_data.to_account_id:
                    raise ValidationError("Cannot transfer to the same account")

                dest_account = self.db.get(Account, transfer_data.to_account_id)
                if not dest_account:
                    raise ResourceNotFoundError("Recipient account not found")

                source_balance = self.balance_service.get_balance_by_account_id(
                    transfer_data.from_account_id
                )

                if source_balance < transfer_data.amount:
                    raise BusinessLogicError("Insufficient funds")

                transfer = Transfer(
                    from_account_id=transfer_data.from_account_id,
                    to_account_id=transfer_data.to_account_id,
                    amount=transfer_data.amount,
                )
                self.db.add(transfer)
                self.db.flush()

                log.info(
                    "Transfer created",
                    extra={
                        "transfer_id": transfer.id,
                        "from_account_id": transfer.from_account_id,
                        "to_account_id": transfer.to_account_id,
                        "amount": transfer.amount,
                    },
                )

                return TransferResponse(
                    id=transfer.id,
                    from_account_id=transfer.from_account_id,
                    to_account_id=transfer.to_account_id,
                    amount=transfer.amount,
                    created_at=transfer.created_at,
                )
        except (ValidationError, ResourceNotFoundError, BusinessLogicError):
            raise
        except Exception as e:
            log.error(
                "Failed to create transfer",
                extra={
                    "error": str(format_exc()),
                    "from_account_id": transfer_data.from_account_id,
                    "to_account_id": transfer_data.to_account_id,
                    "amount": transfer_data.amount,
                },
            )
            raise BusinessLogicError(f"Failed to create transfer: {str(e)}") from e

    def create_system_transfer(
        self, to_account_id: UUIDStr, amount: float
    ) -> TransferResponse:
        """Create a system transfer (e.g., for initial deposits)."""
        try:
            transfer = Transfer(
                from_account_id=None,  # System account
                to_account_id=to_account_id,
                amount=amount,
            )
            self.db.add(transfer)
            self.db.flush()

            log.info(
                "System transfer created",
                extra={
                    "transfer_id": transfer.id,
                    "to_account_id": transfer.to_account_id,
                    "amount": transfer.amount,
                },
            )

            return TransferResponse(
                id=transfer.id,
                from_account_id=None,
                to_account_id=transfer.to_account_id,
                amount=transfer.amount,
                created_at=transfer.created_at,
            )
        except Exception as e:
            log.error(
                "Failed to create system transfer",
                extra={
                    "error": str(format_exc()),
                    "to_account_id": to_account_id,
                    "amount": amount,
                },
            )
            raise BusinessLogicError(
                f"Failed to create system transfer: {str(e)}"
            ) from e

    def get_transfer_by_id(self, transfer_id: UUIDStr) -> TransferResponse | None:
        """Get transfer details by ID."""
        transfer = self.db.get(Transfer, transfer_id)
        if not transfer:
            return None

        return TransferResponse(
            id=transfer.id,
            from_account_id=(
                transfer.from_account_id if transfer.from_account_id else None
            ),
            to_account_id=transfer.to_account_id,
            amount=transfer.amount,
            created_at=transfer.created_at,
        )
