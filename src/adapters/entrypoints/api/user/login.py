from typing import Type

from fastapi import HTTPException, status

from src.ports.base_router import BaseRouterView
from src.ports.sso import SSOPort
from src.use_case.login import LoginUseCase


class LoginRouter(BaseRouterView):
	def __init__(
		self,
		name: str,
		use_case: Type[LoginUseCase],
		google_sso_adapter: SSOPort,
	):
		super().__init__(name, use_case)
		self.google_sso_adapter = google_sso_adapter

	def _add_to_router(self) -> None:
		self.router.add_api_route(
			'/login',
			self.login,
			methods=['GET'],
			status_code=status.HTTP_200_OK,
			description='Login with SSO',
			tags=['sso', 'login'],
		)

	async def login(self, provider: str) -> dict[str, str]:
		match provider:
			case 'google':
				adapter = self.google_sso_adapter
			case _:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail='Invalid provider',
				)
		return await self.use_case(adapter).execute()
