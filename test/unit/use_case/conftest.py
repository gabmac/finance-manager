from unittest.mock import Mock

from src.ports.balance_reader import BalanceReaderPort
from src.ports.sso import SSOPort
from src.ports.user_reader import UserReaderPort
from src.ports.user_writer import UserWriterPort
from test.conftest import BaseConfTest


class BaseUseCaseConfTest(BaseConfTest):
	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		cls.google_sso_adapter = Mock(spec=SSOPort)
		cls.user_reader = Mock(spec=UserReaderPort)
		cls.user_writer = Mock(spec=UserWriterPort)
		cls.balance_reader = Mock(spec=BalanceReaderPort)
