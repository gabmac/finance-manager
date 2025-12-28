from src.ports.sso import SSOPort


class LoginUseCase:
	def __init__(self, sso_adapter: SSOPort):
		self.sso_adapter = sso_adapter

	async def execute(self):
		return await self.sso_adapter.login()
