from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.


class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
