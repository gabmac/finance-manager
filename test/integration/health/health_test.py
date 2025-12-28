from test.integration.health.conftest import HealthConfTest


class HealthTest(HealthConfTest):
	def test_health(self) -> None:
		response = self.test_client.get('/api/health')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'message': 'OK'})
