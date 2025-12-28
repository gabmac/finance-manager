from datetime import UTC, datetime
from decimal import Decimal

from pydantic import Field

from src.entities.base_entity import BaseEntity
from src.enums.transaction import TransactionType


class Transaction(BaseEntity):
	"""Transaction entity."""

	amount: Decimal = Field(description='Transaction amount')
	description: str | None = Field(default=None, description='Transaction description')
	type: TransactionType = Field(description='Transaction type')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='Transaction created at',
	)
