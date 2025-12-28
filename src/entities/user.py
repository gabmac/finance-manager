from datetime import UTC, datetime
from uuid import UUID, uuid7

from pydantic import EmailStr, Field

from src.entities.balance import Balance
from src.entities.base_entity import BaseEntity


class User(BaseEntity):
	"""User entity."""

	id: UUID = Field(default_factory=uuid7)
	email: EmailStr = Field(description='User email')
	first_name: str = Field(description='User first name')
	last_name: str = Field(description='User last name')
	is_active: bool = Field(description='User is active')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='User created at',
	)


class UserWithBalance(User):
	balance: Balance = Field(
		default_factory=lambda: Balance(amount=0.0),
		description='User balance',
	)
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='User created at',
	)
	updated_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='User updated at',
	)


class UserWithJWT(User):
	jwt: str = Field(
		description='User JWT',
		pattern=r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$',
	)
