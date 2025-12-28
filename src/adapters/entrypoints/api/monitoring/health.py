from fastapi import status

from src.ports.base_router import BaseRouterViewNoUseCase


class HealthRouter(BaseRouterViewNoUseCase):
	def __init__(self, name: str) -> None:
		super().__init__(name)
		self._add_to_router()

	def _add_to_router(self) -> None:
		self.router.add_api_route(
			'/',
			self.health,
			methods=['GET'],
			status_code=status.HTTP_200_OK,
			description='Health check',
		)

	def health(self) -> dict[str, str]:
		return {'message': 'OK'}
