from unittest.mock import Mock

from fastapi import Request

from src.exceptions import NotFound
from src.use_case.callback import CallbackUseCase
from test.unit.use_case.conftest import BaseUseCaseConfTest


class CallbackTest(BaseUseCaseConfTest):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		cls.secret_key = 'test_secret_key'
		cls.algorithm = 'HS256'
		cls.expiration_hours = 24

		cls.callback_use_case = CallbackUseCase(
			sso_adapter=cls.google_sso_adapter,
			user_reader=cls.user_reader,
			user_writer=cls.user_writer,
			secret_key=cls.secret_key,
			algorithm=cls.algorithm,
			expiration_hours=cls.expiration_hours,
		)
		cls.mock_request = Mock(spec=Request)

	def setUp(self) -> None:
		super().setUp()
		self.user = self.user_generator.build()
		self.google_sso_adapter.callback.return_value = self.user

	def tearDown(self) -> None:
		super().tearDown()
		self.google_sso_adapter.callback.reset_mock()
		self.user_reader.find_by_email.reset_mock()
		self.user_writer.create_with_initial_balance.reset_mock()

	async def test_callback_existing_user(self):
		self.user_reader.find_by_email.return_value = self.user

		result = await self.callback_use_case.execute(self.mock_request)

		self.google_sso_adapter.callback.assert_called_once_with(self.mock_request)
		self.user_reader.find_by_email.assert_called_once_with(self.user.email)
		self.user_writer.create_with_initial_balance.assert_not_called()
		self.assertEqual(
			result.model_dump_json(exclude={'jwt'}), self.user.model_dump_json()
		)

	async def test_callback_new_user(self):
		self.user_reader.find_by_email.side_effect = NotFound('User not found')
		self.user_reader.find_by_email.return_value = None

		self.user_writer.create_with_initial_balance.return_value = self.user

		result = await self.callback_use_case.execute(self.mock_request)

		self.google_sso_adapter.callback.assert_called_once_with(self.mock_request)
		self.user_reader.find_by_email.assert_called_once_with(self.user.email)
		self.user_writer.create_with_initial_balance.assert_called_once_with(self.user)
		self.assertEqual(
			result.model_dump_json(exclude={'jwt'}), self.user.model_dump_json()
		)
