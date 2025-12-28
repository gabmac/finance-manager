from datetime import datetime
from time import timezone
from typing import TYPE_CHECKING

from pydantic import Field

from src.entities.base_entity import BaseEntity

if TYPE_CHECKING:
	from src.enums.transaction import TransactionType


class Transaction(BaseEntity):
	"""Transaction entity."""

	amount: float = Field(description='Transaction amount')
	description: str | None = Field(default=None, description='Transaction description')
	type: TransactionType = Field(description='Transaction type')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(timezone.utc),
		description='Transaction created at',
	)
