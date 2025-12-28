"""Application Settings"""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import (
	APIRouter,
	FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.database.models.session import DatabaseSettings
from src.adapters.database.repository.balance_reader_repository import (
	BalanceReaderRepository,
)
from src.adapters.database.repository.user_reader_repository import UserReaderRepository
from src.adapters.database.repository.user_writer_repository import UserWriterRepository
from src.adapters.entrypoints.api.balance.users_balance import BalanceRouter
from src.adapters.entrypoints.api.cross_cutting.middleware_context import (
	RequestContextsMiddleware,
)
from src.adapters.entrypoints.api.cross_cutting.middleware_jwt import (
	JWTValidationMiddleware,
)
from src.adapters.entrypoints.api.cross_cutting.middleware_logging import (
	RequestContextLogMiddleware,
)
from src.adapters.entrypoints.api.monitoring.health import HealthRouter
from src.adapters.entrypoints.api.router import API, AuthAPI
from src.adapters.entrypoints.api.user.callback import CallbackRouter
from src.adapters.entrypoints.api.user.login import LoginRouter
from src.adapters.sso.google import GoogleSSOAdapter
from src.config import GoogleConfig, JWTConfig, PostgresConfig, System
from src.use_case.callback import CallbackUseCase
from src.use_case.get_balance import GetBalanceUseCase
from src.use_case.login import LoginUseCase


class AppConfig:
	"""Application Configurations"""

	def __init__(
		self,
		router: APIRouter,
		auth_router: AuthAPI,
		config: System,
		db_config: PostgresConfig,
		jwt_config: JWTConfig,
	):
		self.router = router
		self.auth_router = auth_router
		self.config = config
		self.jwt_config = jwt_config

		@asynccontextmanager
		async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
			yield

		self.app = FastAPI(
			title='Finance Manager',
			description='Finance Manager',
			openapi_url='/openapi.json',
			docs_url='/docs',
			redoc_url='/redoc',
			lifespan=lifespan,
		)

	def init_cors(self) -> None:
		"""Initialize CORS"""
		self.app.add_middleware(
			CORSMiddleware,
			allow_origins=['*'],
			allow_credentials=True,
			allow_methods=['*'],
			allow_headers=['*'],
		)

	def init_security_schemes(self) -> None:
		"""Configure OpenAPI security schemes for swagger UI."""

		# Store reference to original openapi method
		original_openapi = self.app.openapi

		def custom_openapi() -> Any:
			if self.app.openapi_schema:
				return self.app.openapi_schema
			openapi_schema = original_openapi()
			openapi_schema['components']['securitySchemes'] = {
				'BearerAuth': {
					'type': 'http',
					'scheme': 'bearer',
					'bearerFormat': 'JWT',
				},
			}
			openapi_schema['security'] = [
				{'BearerAuth': []},
			]
			self.app.openapi_schema = openapi_schema
			return self.app.openapi_schema

		self.app.openapi = custom_openapi  # type: ignore

	def init_context(self) -> None:
		self.app.add_middleware(
			RequestContextsMiddleware,  # pyright: ignore[reportUndefinedVariable]
		)
		self.app.add_middleware(
			JWTValidationMiddleware,  # pyright: ignore[reportUndefinedVariable]
			jwt_config=self.jwt_config,
		)
		self.app.add_middleware(
			RequestContextLogMiddleware,  # pyright: ignore[reportUndefinedVariable]
			application_name=self.config.application_name,
		)

	def init_routes(self) -> None:
		"""Intialize Routes"""
		self.app.include_router(self.router)  # type: ignore
		self.app.include_router(self.auth_router)  # type: ignore

	def start_application(self) -> FastAPI:
		"""Start Application with Environment"""
		self.init_context()
		self.init_cors()
		self.init_security_schemes()
		self.init_routes()
		return self.app


def init_api() -> FastAPI:
	db_config = PostgresConfig()
	db = DatabaseSettings(
		host=db_config.host,
		password=db_config.password,
		port=db_config.port,
		user=db_config.user,
		database=db_config.database,
	)

	jwt_config = JWTConfig()
	user_reader = UserReaderRepository(database_settings=db)
	user_writer = UserWriterRepository(database_settings=db)
	balance_reader = BalanceReaderRepository(database_settings=db)

	get_balance_use_case = GetBalanceUseCase(balance_reader=balance_reader)

	callback_use_case_factory = lambda sso_adapter: CallbackUseCase(  # noqa: E731
		sso_adapter=sso_adapter,
		user_reader=user_reader,
		user_writer=user_writer,
		secret_key=jwt_config.secret_key,
		algorithm=jwt_config.algorithm,
		expiration_hours=jwt_config.expiration_hours,
	)

	initializer = API(
		health_router=HealthRouter(name='health'),
		balance_router=BalanceRouter(name='user', use_case=get_balance_use_case),
	)

	auth_api = AuthAPI(
		login_router=LoginRouter(
			name='{provider}',
			use_case=LoginUseCase,
			google_sso_adapter=GoogleSSOAdapter(config=GoogleConfig()),
		),
		callback_router=CallbackRouter(
			name='{provider}',
			use_case_factory=callback_use_case_factory,  # type: ignore
			google_sso_adapter=GoogleSSOAdapter(config=GoogleConfig()),
		),
	)

	return AppConfig(
		router=initializer.router,
		auth_router=auth_api.router,  # type: ignore
		db_config=db_config,
		jwt_config=jwt_config,
		config=System(),
	).start_application()


def get_app() -> FastAPI:
	"""Get or create the FastAPI application."""
	return init_api()


# Lazy app initialization - only called when accessed
app: FastAPI | None = None


def create_app() -> FastAPI:
	"""Create the app instance (used by tests and production)."""
	global app
	if app is None:
		app = init_api()
	return app
