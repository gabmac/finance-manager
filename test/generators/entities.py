from polyfactory.factories.pydantic_factory import ModelFactory

from src.entities.balance import Balance
from src.entities.user import User, UserWithBalance


class UserGenerator(ModelFactory):
	__model__ = User


class UserWithBalanceGenerator(ModelFactory):
	__model__ = UserWithBalance


class BalanceGenerator(ModelFactory):
	__model__ = Balance
