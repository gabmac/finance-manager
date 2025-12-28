from test.integration.conftest import BaseViewConfTest


class BalanceConfTest(BaseViewConfTest):
	def setUp(self) -> None:
		super().setUp()
		self.user_with_balance = self.user_with_balance_generator.build()

