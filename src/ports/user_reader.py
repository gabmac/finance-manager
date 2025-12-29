from abc import ABC, abstractmethod

from src.entities.user import User


class UserReaderPort(ABC):
	@abstractmethod
	async def find_by_email(self, email: str) -> User:
		pass
