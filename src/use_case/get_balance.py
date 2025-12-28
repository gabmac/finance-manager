from uuid import UUID

from src.entities.balance import Balance
from src.ports.balance_reader import BalanceReaderPort


class GetBalanceUseCase:
	def __init__(self, balance_reader: BalanceReaderPort):
		self.balance_reader = balance_reader

	async def execute(self, user_id: UUID) -> Balance:
		return await self.balance_reader.find_by_user_id(user_id)

