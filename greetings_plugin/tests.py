from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.

class GreetingTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(username="Test", email="test@email.com")
        self.user.set_password('password')
        self.user.is_active = True
        self.user.save()

    def test_create_greetings_with_authenticated_user_passes(self):
        self.client.force_login(user=self.user)

        response = self.client.post(path="/api/greetings/v1/greet/", json={"text": "hello"})
        self.assertEqual(response.status_code, 201)
        