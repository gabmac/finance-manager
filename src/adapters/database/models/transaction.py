from datetime import UTC, datetime
from decimal import Decimal

from sqlmodel import Field

from src.adapters.database.models.base_model import BaseModel
from src.enums.transaction import TransactionType


class TransactionModel(BaseModel, table=True):
	"""Transaction model."""

	__tablename__ = 'transaction'

	amount: Decimal = Field(nullable=False)
	description: str | None = Field(nullable=True)
	type: TransactionType = Field(nullable=False)
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
	)
