from polyfactory.factories.pydantic_factory import ModelFactory

from src.entities.balance import Balance
from src.entities.user import User, UserWithBalance


class UserGenerator(ModelFactory[User]):
	__model__ = User


class UserWithBalanceGenerator(ModelFactory[UserWithBalance]):
	__model__ = UserWithBalance


class BalanceGenerator(ModelFactory[Balance]):
	__model__ = Balance
