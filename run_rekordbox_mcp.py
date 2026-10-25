"""Portable launcher with an explicit library path and no transferred account files."""
import asyncio,json,logging,os,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'rekordbox-mcp'))

def library_path():
 settings=json.loads((ROOT/'dj-stack.json').read_text())
 value=os.environ.get('REKORDBOX_DATABASE') or settings.get('database')
 path=Path(value) if value else Path(os.environ.get('APPDATA',Path.home()/'AppData/Roaming'))/'Pioneer/rekordbox/master.db'
 return path/'master.db' if path.is_dir() else path

def application_key():
 source=ROOT/'cuegen/source/CueGen/Generator.cs'
 match=re.search(r'key: Config.UseSqlCipher \? "([^"]+)"',source.read_text(encoding='utf-8-sig'))
 if not match:raise RuntimeError('CueGen source key format changed; inspect the pinned source before proceeding')
 return match.group(1)

def configure():
 from pyrekordbox import config,Rekordbox6Database
 # Provide only the local library path and the generic application key already
 # published in CueGen. Avoid account-file copying or key extraction from a
 # running Rekordbox process. This adapter is pinned to pyrekordbox 0.4.3.
 config.__config__['rekordbox7'].update({'db_path':str(library_path()),'dp':application_key()})
 from rekordbox_mcp.database import RekordboxDatabase
 async def connect_explicit(self,database_path=None):
  def inner():
   path=Path(database_path) if database_path else library_path()
   if path.is_dir():path=path/'master.db'
   if not path.is_file():raise FileNotFoundError('Rekordbox library not found. Initialize Rekordbox locally or set REKORDBOX_DATABASE to its master.db.')
   self.database_path=path.parent
   self.db=Rekordbox6Database(path=path,db_dir=path.parent,key=application_key())
   self._connected=True;self._content_cache=None;self._content_cache_time=None
  await asyncio.to_thread(inner)
 RekordboxDatabase.connect=connect_explicit

def main():
 logging.getLogger('pyrekordbox').setLevel(logging.WARNING)
 configure()
 from rekordbox_mcp.server import main as server_main
 server_main()

if __name__=='__main__':main()
