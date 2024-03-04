from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import Group


class UserModelTest(TestCase):
    """класс для тестов  юзера"""

    fixtures = ["fixtures/01-groups.json", "fixtures/02-users.json"]

    def test_loaded_user_and_groups(self):
        self.assertEqual(get_user_model().objects.count(), 12)
        self.assertEqual(Group.objects.count(), 2)
