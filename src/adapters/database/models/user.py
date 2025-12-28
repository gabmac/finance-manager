from datetime import UTC, datetime

from sqlmodel import Field, Relationship

from src.adapters.database.models.base_model import BaseModel


class UserModel(BaseModel, table=True):
	"""User model."""

	__tablename__ = 'user'

	email: str = Field(nullable=False, unique=True, index=True)
	first_name: str = Field(nullable=False)
	last_name: str = Field(nullable=False)
	is_active: bool = Field(default=True)
	balance: 'BalanceModel' = Relationship(back_populates='user')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
	)
	updated_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
	)
