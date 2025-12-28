from datetime import UTC, datetime

from pydantic import Field

from src.entities.base_entity import BaseEntity
from src.enums.transaction import TransactionType


class Transaction(BaseEntity):
	"""Transaction entity."""

	amount: float = Field(description='Transaction amount')
	description: str | None = Field(default=None, description='Transaction description')
	type: TransactionType = Field(description='Transaction type')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='Transaction created at',
	)
