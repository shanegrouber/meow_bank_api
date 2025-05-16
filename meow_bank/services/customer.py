from traceback import format_exc

from sqlalchemy import select
from sqlalchemy.orm import Session

from meow_bank.core.constants import UUIDStr
from meow_bank.core.logging import log
from meow_bank.db.models import Account, Customer
from meow_bank.schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerWithAccountIds,
)


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        """Create a new customer."""
        try:
            customer = Customer(name=customer_data.name)
            self.db.add(customer)
            self.db.flush()
            self.db.commit()

            return CustomerResponse(
                id=str(customer.id),
                name=str(customer.name),
                created_at=customer.created_at,
            )
        except Exception as e:
            log.error(
                "Failed to create customer",
                extra={
                    "error": str(format_exc()),
                    "customer_data": customer_data.model_dump(),
                },
            )
            raise ValueError(f"Failed to create customer: {str(e)}") from e

    def get_customer(self, customer_id: UUIDStr) -> CustomerWithAccountIds | None:
        """Get customer details by ID."""
        customer = self.db.get(Customer, customer_id)
        if not customer:
            return None

        stmt = select(Account.id).filter(Account.customer_id == customer_id)
        account_ids = self.db.execute(stmt).scalars().all()

        return CustomerWithAccountIds(
            id=customer.id,
            name=customer.name,
            created_at=customer.created_at,
            account_ids=account_ids,
        )
