"""Build a distributable source kit without account files or generated libraries."""
import hashlib,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from setup_windows import verify_payloads

ROOT_FILES=['README.md','LICENSE','CONTRIBUTING.md','SECURITY.md','VERSION','START-HERE.txt','AGENTS.md',
 'setup_windows.py','run_rekordbox_mcp.py','verify_connection.py','stage_cuegen.py','requirements-windows.txt',
 'manifest.json','payload-sha256.json','.gitignore','.gitattributes']
FOLDERS=['sources','overlay','skills','licenses','docs','scripts','tests','.github']
def build(output_dir=None):
 verify_payloads(ROOT)
 files=[ROOT/name for name in ROOT_FILES]
 for directory in FOLDERS:
  files.extend(p for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
 files=sorted(set(files))
 forbidden={'.db','.sqlite','.sqlite3','.mp3','.flac','.wav','.aiff','.m4a','.pyc'}
 for file in files:
  if file.suffix.lower() in forbidden or file.name in ('auth.json','config.toml','.env'):
   raise ValueError('Private or generated file cannot be packaged: '+str(file))
  if not file.is_file():raise FileNotFoundError(file)
 version=(ROOT/'VERSION').read_text().strip()
 dest=Path(output_dir) if output_dir else ROOT/'dist';dest.mkdir(parents=True,exist_ok=True)
 target=dest/f'dj-prep-toolkit-{version}-windows.zip'
 hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
  for file in files:z.write(file,'dj-prep-toolkit/'+file.relative_to(ROOT).as_posix())
  z.writestr('dj-prep-toolkit/SHA256SUMS.json',json.dumps(hashes,indent=2)+'\n')
 with zipfile.ZipFile(target) as z:
  if z.testzip() is not None:raise ValueError('ZIP integrity check failed')
  for name,digest in hashes.items():
   if hashlib.sha256(z.read('dj-prep-toolkit/'+name)).hexdigest()!=digest:raise ValueError('ZIP content mismatch: '+name)
 (target.with_suffix('.zip.sha256')).write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n')
 return target
if __name__=='__main__':print(build())
