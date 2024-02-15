from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group


class UserModelTest(TestCase):
    """класс для тестов юзера"""

    fixtures = ["fixtures/02-users.json", "fixtures/01-groups.json"]

    def test_loaded_user_and_groups(self):
        self.assertEqual(get_user_model().objects.count(), 11)
        self.assertEqual(Group.objects.count(), 2)
