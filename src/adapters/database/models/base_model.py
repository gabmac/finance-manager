from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid6 import uuid7


class BaseModel(SQLModel):
	"""Base class for all database models."""

	id: UUID = Field(default_factory=uuid7, primary_key=True)
