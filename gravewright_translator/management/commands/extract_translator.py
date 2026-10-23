"""Inventory core dictionaries, literal templates and browser interface strings."""
import ast
import json
from pathlib import Path
import re

from django.core.management.base import BaseCommand
from gravewright.web.localization import StaticText


def inventory(source):
    strings = {}
    def add(text, origin):
        if isinstance(text, str) and text.strip() and re.search('[A-Za-zÀ-ÿ]', text):
            strings.setdefault(text.strip(), set()).add(origin)
    def walk(value, origin):
        if isinstance(value, str):add(value, origin)
        elif isinstance(value, dict):
            for item in value.values():walk(item, origin)
        elif isinstance(value, list):
            for item in value:walk(item, origin)
    for path in (source / 'gravewright').rglob('*messages*.json'):
        walk(json.loads(path.read_text(encoding='utf-8')), path.relative_to(source).as_posix())
    for path in (source / 'gravewright').rglob('*.html'):
        if 'node_modules' in path.parts or 'vendor' in path.parts or not path.is_file():continue
        parser = StaticText(); parser.feed(path.read_text(encoding='utf-8')); parser.close()
        for text in parser.strings:add(text, path.relative_to(source).as_posix())
    quoted = re.compile(r'"((?:\\.|[^"\\])*)"|\x27((?:\\.|[^\x27\\])*)\x27')
    calls = re.compile(r'''\b(?:gwText|modalText|text|label|t)\s*\(\s*((?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'))''')
    for path in (source / 'gravewright').rglob('*.js'):
        if ('vendor' in path.parts or 'node_modules' in path.parts or not path.is_file()
                or path.stat().st_size > 600000 or path.name.startswith('generated') or path.name.endswith('.test.js')):continue
        content = path.read_text(encoding='utf-8')
        for match in calls.finditer(content):
            try:
                value = ast.literal_eval(match[1])
                value = re.sub(r'\\(?:x([0-9A-Fa-f]{2})|u([0-9A-Fa-f]{4}))', lambda m: chr(int(m[1] or m[2], 16)), value)
            except (ValueError, SyntaxError):
                continue
            add(value, path.relative_to(source).as_posix())
        for match in quoted.finditer(content):
            raw = next(part for part in match.groups() if part is not None)
            if '\\' in raw or len(raw) > 800:continue
            if (re.fullmatch(r'[A-Za-z][A-Za-z0-9\s.,!?():%/→–—…+·\-]*', raw)
                    and (raw[:1].isupper() or ' ' in raw) and len(raw.strip()) > 1):
                add(raw, path.relative_to(source).as_posix())
    return {key: sorted(value) for key, value in sorted(strings.items())}


class Command(BaseCommand):
    help = 'Extract a reviewable inventory; does not translate campaign or player data.'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=Path, required=True)
        parser.add_argument('--output', type=Path, required=True)

    def handle(self, *args, **options):
        sources = inventory(options['source'])
        options['output'].parent.mkdir(parents=True, exist_ok=True)
        options['output'].write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        self.stdout.write(f'{len(sources)} unique source strings')
