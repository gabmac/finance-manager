from typing import Awaitable, Callable

import jwt
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.settings.config import JWTConfig


class JWTValidationMiddleware(BaseHTTPMiddleware):
	"""Middleware for validating JWT tokens on protected routes."""

	# Routes that don't require authentication
	EXCLUDED_PATHS: set[str] = {
		'/docs',
		'/redoc',
		'/openapi.json',
		'/api/health',
        '/docs/',
		'/redoc/',
		'/openapi.json/',
		'/api/health/',
	}

	# Path prefixes that don't require authentication
	EXCLUDED_PREFIXES: tuple[str, ...] = (
		'/auth/',
	)

	def __init__(
		self,
		app: ASGIApp,
		jwt_config: JWTConfig,
	) -> None:
		super().__init__(app)
		self.secret_key = jwt_config.secret_key
		self.algorithm = jwt_config.algorithm

	def _is_excluded_path(self, path: str) -> bool:
		"""Check if the path should skip JWT validation."""
		if path in self.EXCLUDED_PATHS:
			return True
		return path.startswith(self.EXCLUDED_PREFIXES)

	def _extract_token(self, request: Request) -> str | None:
		"""Extract JWT token from Authorization header."""
		auth_header = request.headers.get('Authorization')
		if not auth_header:
			return None

		parts = auth_header.split()
		if len(parts) != 2 or parts[0].lower() != 'bearer':
			return None

		return parts[1]

	def _unauthorized_response(self, detail: str) -> JSONResponse:
		"""Create a 401 Unauthorized response."""
		return JSONResponse(
			status_code=status.HTTP_401_UNAUTHORIZED,
			content={'detail': detail},
			headers={'WWW-Authenticate': 'Bearer'},
		)

	async def dispatch(
		self,
		request: Request,
		call_next: Callable[[Request], Awaitable[Response]],
	) -> Response:
		# Skip validation for excluded paths
		if self._is_excluded_path(request.url.path):
			return await call_next(request)

		# Extract token
		token = self._extract_token(request)
		if not token:
			return self._unauthorized_response('Missing authentication token')

		# Validate token
		try:
			payload = jwt.decode(
				token,
				self.secret_key,
				algorithms=[self.algorithm],
			)
			# Store user info in request state for downstream access
			request.state.user_id = payload.get('sub')
			request.state.user_email = payload.get('email')
			request.state.jwt_payload = payload

		except jwt.ExpiredSignatureError:
			return self._unauthorized_response('Token has expired')
		except jwt.InvalidTokenError as e:
			return self._unauthorized_response(f'Invalid token: {e!s}')

		return await call_next(request)
