"""Apply reviewed UI terminology to generated catalog drafts (idempotent)."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
reviewed=json.loads((root/'scripts/reviewed.json').read_text())
source=json.loads((root/'source-inventory.json').read_text())
for key in reviewed:source.setdefault(key,['scripts/reviewed.json'])
(root/'source-inventory.json').write_text(json.dumps(source,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
for locale in ['en','pt-BR','es']:
 p=root/'gravewright_translator/catalogs'/f'{locale}.json'
 d=json.loads(p.read_text())
 for key,value in list(d.items()):
  if len(value)>1 and value.startswith('"') and value.endswith('"'):value=value[1:-1]
  if locale!='en':
   value=re.sub(r'\b(\w+)(?:\s+\1){1,}\b',r'\1',value,flags=re.I)
  d[key]=value
 for key,values in reviewed.items():d[key]=key if locale=='en' else values[0 if locale=='pt-BR' else 1]
 p.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
