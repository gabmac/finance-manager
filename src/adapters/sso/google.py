from typing import Any

from fastapi import Request
from fastapi_sso.sso.google import GoogleSSO

from src.config import GoogleConfig
from src.entities.user import User
from src.ports.sso import SSOPort


class GoogleSSOAdapter(SSOPort):
	def __init__(self, config: GoogleConfig):
		self.config = config
		self.sso = GoogleSSO(
			client_id=config.client_id,
			client_secret=config.client_secret,
			redirect_uri=config.redirect_uri,
			allow_insecure_http=True,
		)

	async def login(self) -> Any:
		async with self.sso:
			return await self.sso.get_login_redirect()

	async def callback(self, request: Request) -> User:
		async with self.sso:
			user = await self.sso.verify_and_process(request)
			if user is None:
				raise ValueError('Failed to verify and process user from SSO callback.')
			return User(
				email=user.email,
				first_name=user.first_name,
				last_name=user.last_name,
				is_active=True,
			)
