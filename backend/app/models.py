from sqlalchemy import Boolean, DateTime, Numeric, String, Integer, JSON, func, Date
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from datetime import date

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_subscription: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    transaction_date: Mapped[date | None] = mapped_column(Date, nullable=True)


class CategorizationRule(Base):
    __tablename__ = "categorization_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(100), nullable=False)
    is_subscription: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_keywords: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    amount_sign: Mapped[str] = mapped_column(String(10), default="any")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )