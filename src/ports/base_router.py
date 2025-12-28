from abc import ABC, abstractmethod
from typing import Any

from fastapi import APIRouter


class BaseRouterViewNoUseCase(ABC):
	router: APIRouter

	def __init__(self, name: str) -> None:
		self.name = name
		self.router = APIRouter(
			prefix=f'/{name}',
			tags=[name],
		)

	@abstractmethod
	def _add_to_router(self) -> None:
		"""
		Add to view to router
		"""


class BaseRouterView(BaseRouterViewNoUseCase):
	def __init__(self, name: str, use_case: Any) -> None:
		self.use_case = use_case
		super().__init__(name)
		self._add_to_router()
