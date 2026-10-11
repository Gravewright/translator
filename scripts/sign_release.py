"""Sign an existing deterministic ZIP; private keys always remain outside the repo."""
import argparse,base64,hashlib,json,zipfile
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key

parser=argparse.ArgumentParser()
parser.add_argument('--key',type=Path,required=True)
parser.add_argument('--key-id',required=True)
parser.add_argument('--archive',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--tag',action='append',help='Creator-defined category; repeat for multiple tags.')
parser.add_argument('--download',help='HTTPS archive URL; defaults to the central Marketplace release.')
args=parser.parse_args()
key=load_pem_private_key(args.key.read_bytes(),password=None)
with zipfile.ZipFile(args.archive) as archive:
    manifest=json.loads(archive.read('manifest.json'))
if manifest['id'] != 'gravewright.translator':
    parser.error('Expected a Translator package.')
record={'id':manifest['id'],'name':manifest['name'],'version':manifest['version'],
        'description':manifest['description'],
        'sdk':manifest['sdk']['requires'], 'type':'module',
        'tags':args.tag or ['Tradução', 'Idiomas', 'Interface'],
        'download':args.download or f"https://github.com/Gravewright/marketplace/releases/download/gravewright.translator-v{manifest['version']}/{args.archive.name}",
        'sha256':hashlib.sha256(args.archive.read_bytes()).hexdigest(),'keyId':args.key_id}
canonical=json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
record['signature']=base64.b64encode(key.sign(canonical)).decode()
args.output.write_text(json.dumps([record],indent=2)+'\n')
print('Signed',record['id'],record['version'],record['sha256'])
