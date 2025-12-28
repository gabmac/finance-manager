from fastapi import status

from src.adapters.database.models.balance import BalanceModel
from src.adapters.database.models.user import UserModel
from test.integration.balance.conftest import BalanceConfTest


class BalanceTest(BalanceConfTest):
	def test_get_balance(self):
		# Scenario: User with balance in the database

		# Given a user with balance in the database
		with self.db.get_session() as session:
			user_data = self.user_with_balance.model_dump(exclude={'balance'})
			user = UserModel.model_validate(user_data)
			session.add(user)
			session.flush()

			balance_data = self.user_with_balance.balance.model_dump()
			balance_data['user_id'] = user.id
			balance = BalanceModel.model_validate(balance_data)
			session.add(balance)
			session.commit()

			user_id = str(user.id)

		# When I call the get balance endpoint with a valid token
		token = self.create_jwt_token(user_id)
		self.test_client.headers.update({'Authorization': f'Bearer {token}'})

		response = self.test_client.get(f'/api/user/{user_id}/balance')

		# Then I should receive the balance
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response_data = response.json()
		self.assertEqual(response_data['amount'], self.user_with_balance.balance.amount)

	def test_get_balance_user_not_found(self):
		# Scenario: User not in the database

		# Given a non-existent user id
		non_existent_user_id = '01936b8a-1234-7def-8000-000000000000'

		# When I call the get balance endpoint
		token = self.create_jwt_token(non_existent_user_id)
		self.test_client.headers.update({'Authorization': f'Bearer {token}'})

		response = self.test_client.get(f'/api/user/{non_existent_user_id}/balance')

		# Then I should receive a 404 error
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		response_data = response.json()
		self.assertIn('detail', response_data)

	def test_get_balance_unauthorized_no_token(self):
		# Scenario: No authentication token provided

		# Given a user with balance in the database
		with self.db.get_session() as session:
			user_data = self.user_with_balance.model_dump(exclude={'balance'})
			user = UserModel.model_validate(user_data)
			session.add(user)
			session.flush()

			balance_data = self.user_with_balance.balance.model_dump()
			balance_data['user_id'] = user.id
			balance = BalanceModel.model_validate(balance_data)
			session.add(balance)
			session.commit()

			user_id = str(user.id)

		# When I call the get balance endpoint without a token
		self.test_client.headers.pop('Authorization', None)

		response = self.test_client.get(f'/api/user/{user_id}/balance')

		# Then I should receive a 401 error
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		response_data = response.json()
		self.assertIn('detail', response_data)

	def test_get_balance_unauthorized_expired_token(self):
		# Scenario: Expired authentication token

		# Given a user with balance in the database
		with self.db.get_session() as session:
			user_data = self.user_with_balance.model_dump(exclude={'balance'})
			user = UserModel.model_validate(user_data)
			session.add(user)
			session.flush()

			balance_data = self.user_with_balance.balance.model_dump()
			balance_data['user_id'] = user.id
			balance = BalanceModel.model_validate(balance_data)
			session.add(balance)
			session.commit()

			user_id = str(user.id)

		# When I call the get balance endpoint with an expired token
		token = self.create_expired_jwt_token(user_id)
		self.test_client.headers.update({'Authorization': f'Bearer {token}'})

		response = self.test_client.get(f'/api/user/{user_id}/balance')

		# Then I should receive a 401 error
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		response_data = response.json()
		self.assertIn('detail', response_data)

