from uuid import UUID

from fastapi import HTTPException, status

from src.dto.balance import BalanceResponse
from src.exceptions import NotFound
from src.ports.base_router import BaseRouterView
from src.use_case.get_balance import GetBalanceUseCase


class BalanceRouter(BaseRouterView):
	def __init__(
		self,
		name: str,
		use_case: GetBalanceUseCase,
	) -> None:
		super().__init__(name, use_case)

	def _add_to_router(self) -> None:
		self.router.add_api_route(
			'/{user_id}/balance',
			self.get_balance,
			methods=['GET'],
			response_model=BalanceResponse,
			status_code=status.HTTP_200_OK,
			description='Get user balance',
			tags=['user', 'balance'],
		)

	async def get_balance(self, user_id: UUID) -> BalanceResponse:
		try:
			balance = await self.use_case.execute(user_id)
		except NotFound as e:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=str(e),
			)

		return BalanceResponse(
			amount=balance.amount,
			updated_at=balance.updated_at,
		)

