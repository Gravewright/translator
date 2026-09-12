"""Build a deterministic, offline marketplace ZIP from the Django app catalogs."""
import hashlib
import json
from pathlib import Path
import re
import zipfile

from django.core.management.base import BaseCommand, CommandError
from gravewright_translator import __version__

ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDER = re.compile(r'\{[A-Za-z_][A-Za-z0-9_.]*\}')


class Command(BaseCommand):
    help = 'Build Translator language data for installation through Gravewright Marketplace.'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=Path, default=Path('dist'))

    def handle(self, *args, **options):
        source = json.loads((ROOT / 'catalogs/en.json').read_text())
        files = {name: (ROOT / 'package' / name).read_bytes() for name in ('manifest.json', 'main.js')}
        report = {}
        for locale in ('pt-BR', 'es'):
            path = ROOT / 'catalogs' / f'{locale}.json'
            catalog = json.loads(path.read_text())
            if set(catalog) != set(source):
                raise CommandError(f'{locale}: missing/extra sources: {set(source) ^ set(catalog)}')
            for text, translated in catalog.items():
                if (not isinstance(translated, str) or not translated.strip()
                        or sorted(PLACEHOLDER.findall(text)) != sorted(PLACEHOLDER.findall(translated))):
                    raise CommandError(f'{locale}: invalid translation/placeholders: {text}')
            files[f'locales/{locale}.json'] = path.read_bytes()
            report[locale] = {'entries': len(catalog), 'missing': 0,
                              'unchanged': sum(key == value for key, value in catalog.items())}
        files['LICENSE.txt'] = (ROOT / 'LICENSE.txt').read_bytes()
        output = options['output']
        output.mkdir(parents=True, exist_ok=True)
        target = output / f'translator-{__version__}.zip'
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, raw in sorted(files.items()):
                info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, raw)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        (output / 'coverage.json').write_text(json.dumps(report, indent=2) + '\n')
        (output / 'SHA256SUMS.txt').write_text(f'{digest}  {target.name}\n')
        self.stdout.write(f'{target}: {len(source)} entries/language; SHA-256 {digest}')
