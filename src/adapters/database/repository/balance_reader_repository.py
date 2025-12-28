from uuid import UUID

from sqlmodel import select

from src.adapters.database.models.balance import BalanceModel
from src.adapters.database.models.session import DatabaseSettings
from src.entities.balance import Balance
from src.exceptions import NotFound
from src.ports.balance_reader import BalanceReaderPort


class BalanceReaderRepository(BalanceReaderPort):
	def __init__(self, database_settings: DatabaseSettings) -> None:
		self.database_settings = database_settings

	async def find_by_user_id(self, user_id: UUID) -> Balance:
		with self.database_settings.get_session() as session:
			statement = select(BalanceModel).where(BalanceModel.user_id == user_id)
			balance_model = session.exec(statement).first()

			if balance_model is None:
				msg = f'Balance for user {user_id} not found'
				raise NotFound(msg)

			return Balance(
				id=balance_model.id,
				amount=balance_model.amount,
				created_at=balance_model.created_at,
				updated_at=balance_model.updated_at,
			)

