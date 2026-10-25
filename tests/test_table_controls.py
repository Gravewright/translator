"""Catalog coverage for the table controls and authored-value-safe host hooks."""
from collections import Counter
import json
from pathlib import Path
import re
import unittest


class TableControlCatalogTests(unittest.TestCase):
    def test_table_control_keys_exist_with_matching_parameters(self):
        root = Path(__file__).resolve().parents[1] / 'gravewright_translator/catalogs'
        source = json.loads((root / 'en.json').read_text(encoding='utf-8'))
        keys = (
            'Empty map', 'Activate after creation', 'Activate for selected players',
            'Measurement title', 'Move {0}', 'Circular activation area',
            'Activation radius (cells)', 'Mouse pointers', "Show participants' pointers",
            'Share my pointer', 'Shortcuts', 'Keyboard shortcuts', 'Restore defaults',
            'Unassign shortcut for {action}', 'This shortcut is already assigned to {action}.',
        )
        parameters = re.compile(r'\{(?:[A-Za-z_][A-Za-z0-9_.]*|\d+)\}')
        for locale in ('pt-BR', 'es'):
            messages = json.loads((root / (locale + '.json')).read_text(encoding='utf-8'))
            for key in keys:
                with self.subTest(locale=locale, key=key):
                    self.assertEqual(source[key], key)
                    self.assertTrue(messages[key].strip())
                    self.assertNotEqual(messages[key], key)
                    self.assertEqual(Counter(parameters.findall(key)), Counter(parameters.findall(messages[key])))
            for key in (' / cell', 'Invalid imported map surface.', 'Only interactive images can have a blueprint.'):
                self.assertNotRegex(messages[key], r'\w\?\w')
