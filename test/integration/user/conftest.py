from unittest.mock import AsyncMock

from src.adapters.sso.google import GoogleSSOAdapter
from test.integration.conftest import BaseViewConfTest


class UserConfTest(BaseViewConfTest):
	def setUp(self) -> None:
		super().setUp()
		self.user = self.user_generator.build()
		self.user_with_balance = self.user_with_balance_generator.build().model_copy(
			update=self.user.model_dump()
		)
		GoogleSSOAdapter.callback = AsyncMock(return_value=self.user)
