from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field, Relationship

from src.adapters.database.models.base_model import BaseModel


class BalanceModel(BaseModel, table=True):
	"""Balance model."""

	__tablename__ = 'balance'

	amount: Decimal = Field(nullable=False)
	user_id: UUID = Field(nullable=False, foreign_key='user.id')
	user: 'UserModel' = Relationship(back_populates='balance')  # noqa: F821
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
	)
	updated_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
	)
