import os
from django.core.management import call_command
from django import setup


def load_all_fixtures():
    """
    Загружает все фикстуры из каталога './fixtures'.

    Каждый файл с расширением '.json' в указанном каталоге обрабатывается
    командой 'python load_fixtures.py', которая загружает данные из файла в базу данных Django.
    """

    fixture_dir = "./fixtures"

    for file_name in os.listdir(fixture_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(fixture_dir, file_name)
            call_command("loaddata", file_path)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    setup()

    load_all_fixtures()
