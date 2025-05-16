import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import relationship

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    accounts = relationship("Account", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name})>"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="accounts")
    sent_transfers = relationship(
        "Transfer",
        foreign_keys="Transfer.from_account_id",
        back_populates="from_account",
    )
    received_transfers = relationship(
        "Transfer",
        foreign_keys="Transfer.to_account_id",
        back_populates="to_account",
    )

    def __repr__(self):
        return f"<Account(id={self.id}, customer_id={self.customer_id})>"


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    from_account_id = Column(String, ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    from_account = relationship(
        "Account",
        foreign_keys=[from_account_id],
        back_populates="sent_transfers",
    )
    to_account = relationship(
        "Account",
        foreign_keys=[to_account_id],
        back_populates="received_transfers",
    )

    def __repr__(self):
        return (
            f"<Transfer(id={self.id}, "
            f"from_account_id={self.from_account_id}, "
            f"to_account_id={self.to_account_id}, "
            f"amount={self.amount})>"
        )
