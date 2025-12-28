from abc import ABC, abstractmethod

from src.entities.user import User


class UserWriterPort(ABC):
	"""Port for writing user data."""

	@abstractmethod
	async def create_with_initial_balance(self, user: User) -> User:
		"""
		Create a new user with an initial balance of 0.

		Args:
		    user: The user entity to create.

		Returns:
		    The created user.
		"""
		pass
