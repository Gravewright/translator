"""Sign an existing deterministic ZIP; private keys always remain outside the repo."""
import argparse,base64,hashlib,json
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key

parser=argparse.ArgumentParser()
parser.add_argument('--key',type=Path,required=True)
parser.add_argument('--key-id',default='gravewright-2026')
parser.add_argument('--archive',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--tag',action='append',help='Creator-defined category; repeat for multiple tags.')
args=parser.parse_args()
key=load_pem_private_key(args.key.read_bytes(),password=None)
record={'id':'gravewright.translator','name':'Translator','version':'0.1.0',
        'description':'Installation-wide English, Brazilian Portuguese and Spanish language options.',
        'sdk':'>=1.0.0 <2.0.0', 'type':'module',
        'tags':args.tag or ['Tradução', 'Idiomas', 'Interface'],
        'download':'https://github.com/Gravewright/translator/releases/download/v0.1.0/translator-0.1.0.zip',
        'sha256':hashlib.sha256(args.archive.read_bytes()).hexdigest(),'keyId':args.key_id}
canonical=json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
record['signature']=base64.b64encode(key.sign(canonical)).decode()
args.output.write_text(json.dumps([record],indent=2)+'\n')
print('Signed',record['id'],record['version'],record['sha256'])
