from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environments(Enum):
	LOCAL = 'local'
	DEVELOPMENT = 'development'
	PRODUCTION = 'production'


class System(BaseSettings):
	model_config = SettingsConfigDict(env_prefix='SYSTEM_')

	environment: Environments = Field(
		description='Environment of the system',
	)

	application_name: str = Field(
		description='Application name',
		default='finance-manager',
	)

	host: str = Field(
		description='Host to bind the server',
		default='0.0.0.0',
	)
	port: int = Field(
		description='Port to bind the server',
		default=8000,
	)


class PostgresConfig(BaseSettings):
	model_config = SettingsConfigDict(env_prefix='POSTGRES_', case_sensitive=False)

	host: str = Field(
		description='Host of the system',
	)
	port: int = Field(
		description='Port of the system',
	)
	user: str = Field(
		description='User of the system',
	)
	password: str = Field(
		description='Password of the system',
	)
	database: str = Field(
		description='Database of the system',
	)


class GoogleConfig(BaseSettings):
	model_config = SettingsConfigDict(env_prefix='GOOGLE_', case_sensitive=False)

	client_id: str = Field(
		description='Client ID of the system',
	)
	client_secret: str = Field(
		description='Client secret of the system',
	)
	redirect_uri: str = Field(description='Redirect Uri')


class JWTConfig(BaseSettings):
	model_config = SettingsConfigDict(env_prefix='JWT_', case_sensitive=False)

	secret_key: str = Field(
		description='Secret key of the system',
	)
	algorithm: str = Field(
		description='Algorithm of the system',
	)
	expiration_hours: int = Field(
		description='Expiration time of the system',
		default=12,
	)
