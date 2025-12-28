from abc import ABC, abstractmethod
from uuid import UUID

from src.entities.balance import Balance


class BalanceReaderPort(ABC):
	@abstractmethod
	async def find_by_user_id(self, user_id: UUID) -> Balance:
		pass

