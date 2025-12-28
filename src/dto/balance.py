from datetime import datetime

from pydantic import BaseModel, Field


class BalanceResponse(BaseModel):
	amount: float = Field(description='Balance amount')
	updated_at: datetime = Field(description='Balance updated at')

