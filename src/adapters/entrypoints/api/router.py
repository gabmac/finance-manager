from fastapi import APIRouter

from src.ports.base_router import BaseRouterView, BaseRouterViewNoUseCase


class API:
	def __init__(
		self,
		health_router: BaseRouterViewNoUseCase,
		balance_router: BaseRouterView,
	):
		self.router = APIRouter(prefix='/api')
		self.router.include_router(health_router.router)
		self.router.include_router(balance_router.router)


class AuthAPI:
	def __init__(
		self,
		login_router: BaseRouterView,
		callback_router: BaseRouterViewNoUseCase,
	):
		self.router = APIRouter(prefix='/auth')
		self.router.include_router(login_router.router)
		self.router.include_router(callback_router.router)
