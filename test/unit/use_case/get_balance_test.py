from uuid import uuid7

from src.exceptions import NotFound
from src.use_case.get_balance import GetBalanceUseCase
from test.unit.use_case.conftest import BaseUseCaseConfTest


class GetBalanceTest(BaseUseCaseConfTest):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		cls.get_balance_use_case = GetBalanceUseCase(
			balance_reader=cls.balance_reader,
		)

	def setUp(self) -> None:
		super().setUp()
		self.balance = self.balance_generator.build()
		self.user_id = uuid7()

	def tearDown(self) -> None:
		super().tearDown()
		self.balance_reader.find_by_user_id.reset_mock()

	async def test_get_balance_success(self):
		self.balance_reader.find_by_user_id.return_value = self.balance

		result = await self.get_balance_use_case.execute(self.user_id)

		self.balance_reader.find_by_user_id.assert_called_once_with(self.user_id)
		self.assertEqual(result.id, self.balance.id)
		self.assertEqual(result.amount, self.balance.amount)
		self.assertEqual(result.created_at, self.balance.created_at)
		self.assertEqual(result.updated_at, self.balance.updated_at)

	async def test_get_balance_user_not_found(self):
		self.balance_reader.find_by_user_id.side_effect = NotFound(
			f'Balance for user {self.user_id} not found'
		)

		with self.assertRaises(NotFound) as context:
			await self.get_balance_use_case.execute(self.user_id)

		self.balance_reader.find_by_user_id.assert_called_once_with(self.user_id)
		self.assertIn(str(self.user_id), str(context.exception))

