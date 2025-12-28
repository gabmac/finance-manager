from src.adapters.database.models.balance import BalanceModel
from src.adapters.database.models.session import DatabaseSettings
from src.adapters.database.models.user import UserModel
from src.entities.user import User
from src.ports.user_writer import UserWriterPort


class UserWriterRepository(UserWriterPort):
	"""Repository for writing user data to the database."""

	def __init__(self, database_settings: DatabaseSettings) -> None:
		self.database_settings = database_settings

	async def create_with_initial_balance(self, user: User) -> User:
		with self.database_settings.get_session() as session:
			user_model = UserModel(
				id=user.id,
				email=user.email,
				first_name=user.first_name,
				last_name=user.last_name,
				is_active=user.is_active,
			)
			session.add(user_model)
			session.flush()

			balance_model = BalanceModel(
				amount=0.0,
				user_id=user_model.id,
			)
			session.add(balance_model)
			session.commit()

			return User(
				id=user_model.id,
				email=user_model.email,
				first_name=user_model.first_name,
				last_name=user_model.last_name,
				is_active=user_model.is_active,
				created_at=user_model.created_at,
			)
