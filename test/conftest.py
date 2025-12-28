from unittest import IsolatedAsyncioTestCase

from test.generators.entities import BalanceGenerator, UserGenerator, UserWithBalanceGenerator


class BaseConfTest(IsolatedAsyncioTestCase):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		cls.user_generator = UserGenerator()
		cls.user_with_balance_generator = UserWithBalanceGenerator()
		cls.balance_generator = BalanceGenerator()
