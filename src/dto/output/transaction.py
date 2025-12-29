from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.enums.transaction import TransactionType


class TransactionResponse(BaseModel):
	id: UUID = Field(description='Transaction ID')
	amount: Decimal = Field(description='Transaction amount', gt=0)
	description: str | None = Field(description='Transaction description')
	type: TransactionType = Field(description='Transaction type')
	created_at: datetime = Field(description='Transaction created at')
