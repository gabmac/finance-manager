from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field, Relationship

from src.adapters.database.models.base_model import BaseModel
from src.enums.transaction import TransactionType


class TransactionModel(BaseModel, table=True):
	__tablename__ = 'transaction'

	amount: Decimal = Field(nullable=False)
	description: str | None = Field(nullable=True)
	type: TransactionType = Field(nullable=False)
	user: 'UserModel' = Relationship(back_populates='transactions')  # noqa: F821
	user_id: UUID = Field(nullable=False, foreign_key='user.id')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		nullable=False,
	)
