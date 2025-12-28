from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid7

from pydantic import Field

from src.entities.base_entity import BaseEntity


class Balance(BaseEntity):
	"""Balance entity."""

	id: UUID = Field(default_factory=uuid7)
	amount: Decimal = Field(description='Balance amount')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='Balance created at',
	)
	updated_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='Balance updated at',
	)
