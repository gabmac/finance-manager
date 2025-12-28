from datetime import datetime
from time import timezone
from uuid import UUID, uuid7

from pydantic import Field

from src.entities.base_entity import BaseEntity


class Balance(BaseEntity):
	"""Balance entity."""

	id: UUID = Field(default_factory=uuid7)
	amount: float = Field(description='Balance amount')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(timezone.utc),
		description='Balance created at',
	)
	updated_at: datetime = Field(
		default_factory=lambda: datetime.now(timezone.utc),
		description='Balance updated at',
	)
