from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BalanceResponse(BaseModel):
	amount: Decimal = Field(description='Balance amount')
	updated_at: datetime = Field(description='Balance updated at')
