from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Request

from src.entities.user import User, UserWithJWT
from src.exceptions import NotFound
from src.ports.sso import SSOPort
from src.ports.user_reader import UserReaderPort
from src.ports.user_writer import UserWriterPort


class CallbackUseCase:
	def __init__(
		self,
		sso_adapter: SSOPort,
		user_reader: UserReaderPort,
		user_writer: UserWriterPort,
		secret_key: str,
		algorithm: str,
		expiration_hours: int,
	):
		self.sso_adapter = sso_adapter
		self.user_reader = user_reader
		self.user_writer = user_writer
		self.secret_key = secret_key
		self.algorithm = algorithm
		self.expiration_hours = expiration_hours

	async def execute(self, request: Request) -> UserWithJWT:
		sso_user = await self.sso_adapter.callback(request)

		try:
			user = await self.user_reader.find_by_email(sso_user.email)
		except NotFound:
			user = User(
				email=sso_user.email,
				first_name=sso_user.first_name,
				last_name=sso_user.last_name,
				is_active=sso_user.is_active,
				created_at=sso_user.created_at,
			)
			user = await self.user_writer.create_with_initial_balance(sso_user)

		payload = {
			'sub': str(user.id),
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'iat': datetime.now(UTC).timestamp(),
			'exp': (
				datetime.now(UTC) + timedelta(hours=self.expiration_hours)
			).timestamp(),
		}

		encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

		return UserWithJWT(
			id=user.id,
			email=user.email,
			first_name=user.first_name,
			last_name=user.last_name,
			is_active=user.is_active,
			created_at=user.created_at,
			jwt=encoded_jwt,
		)
