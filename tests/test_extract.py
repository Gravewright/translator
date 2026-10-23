"""The inventory includes parameterized native Translator calls."""
from pathlib import Path
import tempfile
import unittest

from django.conf import settings

if not settings.configured:
    settings.configure(INSTALLED_APPS=['gravewright_translator'], SECRET_KEY='offline-extraction-test')
import django
django.setup()

from gravewright_translator.management.commands.extract_translator import inventory


class ExtractionTests(unittest.TestCase):
    def test_native_alias_and_adapter_calls_keep_parameterized_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'gravewright/maps/strings.js'
            path.parent.mkdir(parents=True)
            path.write_text(r'''
                t('Prepared {count} steps');
                translator.t ('Page {0} of {1}');
                text('Preparing PDF page {0} of {1}\u2026');
            ''', encoding='utf-8')
            result = inventory(root)
            for key in ('Prepared {count} steps', 'Page {0} of {1}', 'Preparing PDF page {0} of {1}…'):
                self.assertEqual(result[key], ['gravewright/maps/strings.js'])

    def test_dependency_and_test_text_are_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ('vendor/library.js', 'node_modules/library/index.js', 'panel.test.js'):
                path = root / 'gravewright/maps' / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("t('Never inventory this {0}');", encoding='utf-8')
            self.assertEqual(inventory(root), {})
