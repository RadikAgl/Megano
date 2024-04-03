import json
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from settings_app.models import SiteSettings


class UserModelTest(TestCase):
    """Класс для тестирования модели пользователя"""

    fixtures = ["01-groups.json", "02-users.json"]

    # TODO - стоит ли кастомизировать загрузку фикстур

    # @classmethod
    # def setUpTestData(cls) -> None:
    #     super().setUpTestData()
    #     cls.load_fixtures()
    #
    # @classmethod
    # def load_fixtures(cls) -> None:
    #     # Загрузка данных непосредственно из файла в базу данных
    #     fixture_dir: str = SiteSettings.load().fixture_dir
    #
    #     # Загрузка фикстуры групп
    #     groups_fixture_path: str = os.path.join(fixture_dir, "01-groups.json")
    #     with open(groups_fixture_path, "r") as groups_fixture_file:
    #         groups_data: dict = json.load(groups_fixture_file)
    #         for group_data in groups_data:
    #             Group.objects.create(name=group_data["fields"]["name"])
    #
    #     # Загрузка фикстуры пользователей
    #     users_fixture_path: str = os.path.join(fixture_dir, "02-users.json")
    #     with open(users_fixture_path, "r") as users_fixture_file:
    #         users_data: dict = json.load(users_fixture_file)
    #         for user_data in users_data:
    #             user_model = get_user_model()
    #             user_model.objects.create(
    #                 email=user_data["fields"]["email"],
    #                 password=user_data["fields"]["password"],
    #                 is_superuser=user_data["fields"]["is_superuser"],
    #                 is_staff=user_data["fields"]["is_staff"],
    #                 is_active=user_data["fields"]["is_active"],
    #                 date_joined=user_data["fields"]["date_joined"],
    #             )

    def test_loaded_user_and_groups(self) -> None:
        self.assertEqual(get_user_model().objects.count(), 11)
        self.assertEqual(Group.objects.count(), 2)
