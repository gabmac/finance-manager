from abc import ABC, abstractmethod

from src.entities.user import User


class UserReaderPort(ABC):
	"""Port for reading user data."""

	@abstractmethod
	async def find_by_email(self, email: str) -> User:
		"""
		Find a user by email.

		Args:
		    email: The user's email address.

		Returns:
		    The user if found.
		"""
		pass
