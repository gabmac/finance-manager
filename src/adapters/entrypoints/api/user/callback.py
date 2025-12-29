from typing import Callable

from fastapi import HTTPException, Request, status

from src.dto.output.user import UserWithJWT
from src.ports.base_router import BaseRouterView
from src.ports.sso import SSOPort
from src.use_case.callback import CallbackUseCase


class CallbackRouter(BaseRouterView):
	def __init__(
		self,
		name: str,
		use_case_factory: Callable[[SSOPort, str, str, int], CallbackUseCase],
		google_sso_adapter: SSOPort,
	):
		super().__init__(name, use_case_factory)
		self.use_case = use_case_factory
		self.google_sso_adapter = google_sso_adapter

	def _add_to_router(self) -> None:
		self.router.add_api_route(
			'/callback',
			self.callback,
			methods=['GET'],
			response_model=UserWithJWT,
			status_code=status.HTTP_200_OK,
			description='Callback from SSO',
			tags=['sso', 'callback'],
		)

	async def callback(self, provider: str, request: Request) -> UserWithJWT:
		match provider:
			case 'google':
				adapter = self.google_sso_adapter
			case _:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail='Invalid provider',
				)

		use_case = self.use_case(
			adapter,
		)
		return await use_case.execute(request)
