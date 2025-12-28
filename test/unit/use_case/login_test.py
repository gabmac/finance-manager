from src.use_case.login import LoginUseCase
from test.unit.use_case.conftest import BaseUseCaseConfTest


class LoginTest(BaseUseCaseConfTest):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		cls.login_use_case = LoginUseCase(cls.google_sso_adapter)

	async def test_login(self):
		await self.login_use_case.execute()
		self.google_sso_adapter.login.assert_called_once()
