"""Initialize Uvicorn."""


import uvicorn

from src.settings.config import Environments, System


def api() -> None:
	config = System()
	"""Main funtion to initialize a fastapi application."""
	if config.environment == Environments.LOCAL:
		log_level = 'debug'
		reload = True
	else:
		log_level = 'info'
		reload = False

	uvicorn.run(
		'src.adapters.entrypoints.api.application:create_app',
		host=config.host,
		port=config.port,
		reload=reload,
		factory=True,
		log_level=log_level,
	)


if __name__ == '__main__':
	api()
