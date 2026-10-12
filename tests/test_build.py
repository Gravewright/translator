import hashlib,json,re,tempfile,tomllib,unittest,zipfile
from pathlib import Path
from django.conf import settings
if not settings.configured:
    settings.configure(INSTALLED_APPS=['gravewright_translator'],SECRET_KEY='offline-build-test')
import django
django.setup()
from django.apps import apps
from django.core.management import call_command
from gravewright_translator import __version__

class BuildTests(unittest.TestCase):
    def test_real_django_app_builds_deterministic_portable_release(self):
        self.assertEqual(apps.get_app_config('gravewright_translator').verbose_name,'Translator')
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)
            call_command('build_translator',output=str(out))
            target=out/f'translator-{__version__}.zip'
            raw=target.read_bytes()
            call_command('build_translator',output=out)
            self.assertEqual(raw,target.read_bytes())
            self.assertTrue((out/'SHA256SUMS.txt').read_text().startswith(hashlib.sha256(raw).hexdigest()))
            with zipfile.ZipFile(target) as archive:
                self.assertFalse(any(n.endswith('.py') for n in archive.namelist()))
                manifest=json.loads(archive.read('manifest.json'))
                self.assertEqual(manifest['version'],__version__)
                project=tomllib.loads((Path(__file__).resolve().parents[1]/'pyproject.toml').read_text(encoding='utf-8'))
                self.assertEqual(project['project']['version'],__version__)
                names=set(archive.namelist())
                for name in ('README.md','API.md','DEVELOPMENT.md','CHANGELOG.md'):
                    self.assertIn(f'docs/{name}',names)
                self.assertIn('docs/examples/main.js',names)
                for name in sorted(names):
                    if not name.endswith('.md'):
                        continue
                    content=archive.read(name).decode('utf-8')
                    for link in re.findall(r'\]\(([^)]+)\)',content):
                        if '://' in link or link.startswith('#'):
                            continue
                        target=(Path(name).parent/link.split('#')[0]).as_posix()
                        self.assertIn(target,names,f'{name}: broken packaged documentation link {link}')
                example=json.loads(archive.read('docs/examples/messages.json'))
                self.assertEqual(set(example),{'en','pt-BR','es'})
                for locale,messages in example.items():
                    self.assertEqual(set(messages),set(example['en']))
                    for key,value in messages.items():
                        self.assertEqual(re.findall(r'\{[^}]+\}',value),re.findall(r'\{[^}]+\}',example['en'][key]))
                self.assertEqual(set(manifest['locales']),{'pt-BR','es'})
                pt=json.loads(archive.read('locales/pt-BR.json'))
                es=json.loads(archive.read('locales/es.json'))
                self.assertEqual(set(pt),set(es))
                self.assertEqual(pt['Settings'],'Configurações')
                self.assertEqual(es['Settings'],'Configuración')
                self.assertEqual(pt['Welcome, {name}'],'Boas-vindas, {name}')
                self.assertEqual(pt['Configure ownership'],'Configurar permissões')
                self.assertEqual(pt['Update'],'Atualizar')
                self.assertEqual(es['This module is used by these tables:'],'Este módulo se usa en estas mesas:')
