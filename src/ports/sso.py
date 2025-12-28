from abc import ABC, abstractmethod

from fastapi import Request

from src.entities.user import User


class SSOPort(ABC):
	@abstractmethod
	async def login(self) -> dict[str, str]:
		"""
		Login with SSO
		"""
		pass

	@abstractmethod
	async def callback(self, request: Request) -> User:
		"""
		Callback from SSO
		"""
		pass
