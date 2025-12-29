from decimal import Decimal

from pydantic import BaseModel, Field

from src.enums.transaction import TransactionType


class CreateTransaction(BaseModel):
	amount: Decimal = Field(gt=0, description='Transaction amount')
	description: str | None = Field(default=None, description='Transaction description')
	type: TransactionType = Field(description='Transaction type')
