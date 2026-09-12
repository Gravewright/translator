"""Build/test the Django app against a Gravewright checkout on PYTHONPATH."""
from config.settings import *  # noqa: F403

INSTALLED_APPS = [*INSTALLED_APPS, 'gravewright_translator']  # noqa: F405
