from sqlalchemy import Column, func, select
from sqlalchemy.orm import Session

from meow_bank.core.constants import UUIDStr
from meow_bank.db.models import Account, Transfer


class BalanceService:
    def __init__(self, db: Session):
        self.db = db

    def _aggregate_transfers_by_direction(
        self, account_id: UUIDStr | list[UUIDStr], column: Column[UUIDStr]
    ) -> float:
        """Helper method to aggregate transfers by direction."""
        if isinstance(account_id, list):
            return (
                select(
                    column,
                    func.sum(Transfer.amount).label("total"),
                )
                .filter(column.in_(account_id))
                .group_by(column)
                .subquery()
            )
        else:
            return (
                select(func.sum(Transfer.amount).label("total"))
                .filter(column == account_id)
                .scalar_subquery()
            )

    def get_balance_by_account_id(self, account_id: UUIDStr) -> float:
        """Calculate the current balance of an account."""
        incoming = self._aggregate_transfers_by_direction(
            account_id, Transfer.to_account_id
        )

        outgoing = self._aggregate_transfers_by_direction(
            account_id, Transfer.from_account_id
        )

        stmt = select(func.coalesce(incoming, 0) - func.coalesce(outgoing, 0))
        result = self.db.execute(stmt).scalar_one()
        return float(result)

    def get_balances_by_account_ids(
        self, account_ids: list[UUIDStr]
    ) -> dict[UUIDStr, float]:
        """Get balances for multiple accounts in a single query."""
        if not account_ids:
            return {}

        incoming = self._aggregate_transfers_by_direction(
            account_ids, Transfer.to_account_id
        )

        outgoing = self._aggregate_transfers_by_direction(
            account_ids, Transfer.from_account_id
        )

        stmt = (
            select(
                Account.id,
                (
                    func.coalesce(incoming.c.total, 0)
                    - func.coalesce(outgoing.c.total, 0)
                ).label("balance"),
            )
            .outerjoin(incoming, Account.id == incoming.c.to_account_id)
            .outerjoin(outgoing, Account.id == outgoing.c.from_account_id)
            .filter(Account.id.in_(account_ids))
        )
        balances = self.db.execute(stmt).all()
        return {account_id: float(balance) for account_id, balance in balances}
