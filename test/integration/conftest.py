from datetime import UTC, datetime, timedelta

import jwt
import testing.postgresql
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from src.adapters.database.models.base_model import BaseModel
from src.adapters.database.models.session import DatabaseSettings
from src.adapters.entrypoints.api.application import create_app
from src.config import JWTConfig
from test.conftest import BaseConfTest

# Tell testing.postgresql where to find PostgreSQL binaries (Homebrew path)
Postgresql = testing.postgresql.PostgresqlFactory(
	cache_initialized_db=True,
	postgres_args='-h 127.0.0.1',
)


class BaseViewConfTest(BaseConfTest):
	fastapi_app = None
	test_client: TestClient | None = None
	postgresql = None
	jwt_config = None

	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()

		cls.jwt_config = JWTConfig()

		# Start PostgreSQL test instance
		cls.postgresql = Postgresql()
		cls.app = create_app()

		# Override DatabaseSettings engine with test database
		engine = create_engine(cls.postgresql.url())
		DatabaseSettings._instance = None
		DatabaseSettings.engine = engine
		cls.db = DatabaseSettings

		# Create all tables in the test database
		BaseModel.metadata.create_all(engine)

		cls.fastapi_app = create_app()

		cls.test_client = TestClient(
			app=cls.fastapi_app,
			base_url='http://localhost:9857',
		)
		cls.test_client.headers.update(
			{
				'Content-Type': 'application/json',
			},
		)

	def create_jwt_token(self, user_id: str) -> str:
		payload = {
			'sub': user_id,
			'exp': datetime.now(UTC)
			+ timedelta(hours=self.jwt_config.expiration_hours),
		}
		return jwt.encode(
			payload,
			self.jwt_config.secret_key,
			algorithm=self.jwt_config.algorithm,
		)

	def create_expired_jwt_token(self, user_id: str) -> str:
		payload = {
			'sub': user_id,
			'exp': datetime.now(UTC) - timedelta(hours=1),
		}
		return jwt.encode(
			payload,
			self.jwt_config.secret_key,
			algorithm=self.jwt_config.algorithm,
		)

	@classmethod
	def tearDownClass(cls) -> None:
		super().tearDownClass()
		if cls.test_client is not None:
			cls.test_client.close()
			cls.test_client = None

		if cls.postgresql is not None:
			cls.postgresql.stop()
			cls.postgresql = None

		# Reset DatabaseSettings
		DatabaseSettings._instance = None
		DatabaseSettings.engine = None

		# Reset app state
		cls.fastapi_app = None
