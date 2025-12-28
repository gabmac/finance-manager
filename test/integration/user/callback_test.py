from sqlmodel import select

from src.adapters.database.models.balance import BalanceModel
from src.adapters.database.models.user import UserModel
from src.entities.user import UserWithBalance, UserWithJWT
from test.integration.user.conftest import UserConfTest


class CallbackTest(UserConfTest):
	def test_callback(self):
		# Scenario: No User in the database

		# When I call the callback endpoint
		response = self.test_client.get('/auth/google/callback')
		self.assertEqual(response.status_code, 200)

		# Then I should receive a JWT with the user information
		response_data = response.json()
		self.assertIn('jwt', response_data)
		self.assertIn('id', response_data)
		self.assertEqual(response_data['email'], self.user.email)
		self.assertEqual(response_data['first_name'], self.user.first_name)
		self.assertEqual(response_data['last_name'], self.user.last_name)
		self.assertEqual(response_data['is_active'], self.user.is_active)

		with self.db.get_session() as session:
			# And the user should be created in the database
			user = session.exec(select(UserModel)).all()
			self.assertEqual(len(user), 1)
			user = user[0]
			self.assertIsNotNone(user)
			self.assertEqual(user.email, self.user.email)
			self.assertEqual(user.first_name, self.user.first_name)
			self.assertEqual(user.last_name, self.user.last_name)
			self.assertEqual(user.is_active, self.user.is_active)

			# And the balance should be created in the database
			self.assertEqual(user.balance.amount, 0.0)

	def test_callback_existing_user(self):
		# Scenario: User already in the database

		# Given a user in the database
		with self.db.get_session() as session:
			# Insert user from generator
			user_data = self.user_with_balance.model_dump(exclude={'balance'})
			user = UserModel.model_validate(user_data)
			session.add(user)
			session.flush()

			# Insert balance with user_id
			balance_data = self.user_with_balance.balance.model_dump()
			balance_data['user_id'] = user.id
			balance = BalanceModel.model_validate(balance_data)
			session.add(balance)
			session.commit()

		# When I call the callback endpoint
		response = self.test_client.get('/auth/google/callback')
		self.assertEqual(response.status_code, 200)

		# Then I should receive a JWT with the user information
		response_data = response.json()
		response_user = UserWithJWT.model_validate(response_data)
		self.assertEqual(response_user.email, self.user.email)

		with self.db.get_session() as session:
			# And the user should be updated in the database
			user = session.exec(
				select(UserModel).where(UserModel.id == self.user.id)
			).first()
			user = UserWithBalance.model_validate(user)
			self.assertEqual(user, self.user_with_balance)
