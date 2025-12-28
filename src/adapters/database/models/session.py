from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from src.adapters.database.models.base_model import BaseModel


class DatabaseSettings:
	"""Database settings."""

	_instance = None
	host: str = ''
	password: str = ''
	port: int = 0
	user: str = ''
	database: str = ''

	engine: Engine | None = None

	def __new__(
		cls, host: str, password: str, port: int, user: str, database: str
	) -> 'DatabaseSettings':
		if cls._instance is None:
			cls.host = host
			cls.password = password
			cls.port = port
			cls.user = user
			cls.database = database
			cls._create_engine()
			cls._instance = cls
		return cls._instance

	@classmethod
	def get_db_url(cls) -> str:
		return f'postgresql+psycopg2://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.database}'

	@classmethod
	def _create_engine(cls) -> Engine:
		if cls.engine is None:
			cls.engine = create_engine(cls.get_db_url(), echo=False)
		return cls.engine

	@classmethod
	def init_db(cls) -> None:
		if cls.engine is None:
			msg = 'Engine is not initialized'
			raise ValueError(msg)

		BaseModel.metadata.create_all(cls.engine)

	@classmethod
	@contextmanager
	def get_session(cls) -> Generator[Session]:
		if cls.engine is None:
			msg = 'Engine is not initialized'
			raise ValueError(msg)
		with Session(cls.engine, autoflush=True) as session:
			try:
				yield session
				session.commit()
				session.flush()
			except Exception:
				session.rollback()
				raise
			finally:
				session.close()
