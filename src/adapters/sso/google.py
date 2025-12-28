from fastapi import Request
from fastapi_sso.sso.google import GoogleSSO

from src.entities.user import User
from src.ports.sso import SSOPort
from src.settings.config import GoogleConfig


class GoogleSSOAdapter(SSOPort):
	def __init__(self, config: GoogleConfig):
		self.config = config
		self.sso = GoogleSSO(
			client_id=config.client_id,
			client_secret=config.client_secret,
			redirect_uri=config.redirect_uri,
			allow_insecure_http=True,
		)

	async def login(self):
		async with self.sso:
			return await self.sso.get_login_redirect()

	async def callback(self, request: Request) -> User:
		async with self.sso:
			user = await self.sso.verify_and_process(request)
			user = User(
				email=user.email,
				first_name=user.first_name,
				last_name=user.last_name,
				is_active=True,
			)
		return user
