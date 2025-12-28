from sqlmodel import select

from src.adapters.database.models.session import DatabaseSettings
from src.adapters.database.models.user import UserModel
from src.entities.user import User
from src.exceptions import NotFound
from src.ports.user_reader import UserReaderPort


class UserReaderRepository(UserReaderPort):
	"""Repository for reading user data from the database."""

	def __init__(self, database_settings: DatabaseSettings) -> None:
		self.database_settings = database_settings

	async def find_by_email(self, email: str) -> User:
		"""
		Find a user by email.

		Args:
		    email: The user's email address.

		Returns:
		    The user if found.

		Raises:
		    ValueError: If no user is found with the given email.
		"""
		with self.database_settings.get_session() as session:
			statement = select(UserModel).where(UserModel.email == email)
			user_model = session.exec(statement).first()

			if user_model is None:
				msg = f'User with email {email} not found'
				raise NotFound(msg)

			return User(
				id=user_model.id,
				email=user_model.email,
				first_name=user_model.first_name,
				last_name=user_model.last_name,
				is_active=user_model.is_active,
				created_at=user_model.created_at,
			)
