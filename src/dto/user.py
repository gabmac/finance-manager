from datetime import UTC, datetime
from uuid import UUID, uuid7

from pydantic import BaseModel, Field



class User(BaseModel):
	id: UUID = Field(default_factory=uuid7)
	email: str = Field(description='User email')
	first_name: str = Field(description='User first name')
	last_name: str = Field(description='User last name')
	is_active: bool = Field(description='User is active')
	created_at: datetime = Field(
		default_factory=lambda: datetime.now(UTC),
		description='User created at',
	)


class UserWithJWT(User):
	jwt: str = Field(
		description='User JWT',
		pattern=r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$',
	)
