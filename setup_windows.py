"""Install the pinned DJ tools. Never opens or modifies a Rekordbox library."""
import argparse,hashlib,json,os,shutil,struct,subprocess,sys,tomllib,zipfile
from pathlib import Path
from datetime import datetime
KIT=Path(__file__).resolve().parent
READ_TOOLS=['connect_database','get_library_stats','get_playlists','get_playlist_tracks','search_tracks','get_track_details','get_track_analysis','get_track_file_path']

def verify_payloads(base=KIT):
 expected=json.loads((base/'payload-sha256.json').read_text(encoding='utf-8'))
 for name,digest in expected.items():
  file=(base/name).resolve()
  if not file.is_relative_to(base.resolve()):raise ValueError('Payload path escapes the source kit')
  if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=digest:
   raise ValueError('Payload integrity check failed: '+name)

def unpack(archive,dest):
 with zipfile.ZipFile(archive) as z:
  for member in z.infolist():
   target=(dest/member.filename).resolve()
   if not target.is_relative_to(dest.resolve()):raise ValueError('Archive path escapes installation')
  z.extractall(dest)

def register(root,config_dir=None):
 config_dir=Path(config_dir) if config_dir else Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))
 config_dir.mkdir(parents=True,exist_ok=True);path=config_dir/'config.toml'
 original=path.read_text(encoding='utf-8-sig') if path.exists() else ''
 parsed=tomllib.loads(original)
 if 'rekordbox' in parsed.get('mcp_servers',{}):raise RuntimeError('rekordbox MCP entry already exists; no configuration was changed. Review it before replacing.')
 exe=(root/'rekordbox-mcp/.venv/Scripts/python.exe').resolve()
 launcher=(root/'run_rekordbox_mcp.py').resolve()
 quote=json.dumps
 entry='\n\n[mcp_servers.rekordbox]\n'+f'command = {quote(str(exe))}\nargs = [{quote(str(launcher))}]\ncwd = {quote(str(root))}\nstartup_timeout_sec = 90\ntool_timeout_sec = 90\nenabled_tools = {json.dumps(READ_TOOLS)}\n'
 entry+='\n[mcp_servers.rekordbox.env]\nPYTHONIOENCODING = "utf-8"\n'
 updated=original.rstrip()+entry;validated=tomllib.loads(updated)
 assert {k:v for k,v in validated.items() if k!='mcp_servers'}=={k:v for k,v in parsed.items() if k!='mcp_servers'}
 assert {k:v for k,v in validated['mcp_servers'].items() if k!='rekordbox'}==parsed.get('mcp_servers',{})
 if path.exists():shutil.copy2(path,path.with_name('config.toml.before-dj-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.bak'))
 path.write_text(updated,encoding='utf-8');print('Registered read-only rekordbox MCP entry:',path)

def main():
 p=argparse.ArgumentParser();p.add_argument('--target',type=Path,default=Path.home()/'Documents/Codex/DJStack');p.add_argument('--prepare-only',action='store_true');p.add_argument('--register-mcp',action='store_true');p.add_argument('--install-skill',action='store_true');p.add_argument('--database',type=Path)
 a=p.parse_args();root=a.target.expanduser().resolve()
 if os.name!='nt':raise SystemExit('This release supports Windows only. macOS and Linux are not supported.')
 if sys.version_info[:2]!=(3,12) or struct.calcsize('P')!=8:raise SystemExit('Run with 64-bit Python 3.12: py -3.12 setup_windows.py ...')
 if root.exists():raise SystemExit('Target exists. Choose a new --target; nothing has been overwritten.')
 if (a.register_mcp or a.install_skill) and a.prepare_only:raise SystemExit('--prepare-only cannot install configuration or skills')
 if a.register_mcp:
  config=Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'config.toml'
  if config.exists() and 'rekordbox' in tomllib.loads(config.read_text(encoding='utf-8-sig')).get('mcp_servers',{}):
   raise SystemExit('rekordbox MCP is already registered; no files were changed. Review the existing entry first.')
 if a.install_skill and (Path.home()/'.agents/skills/rekordbox-short-blends').exists():
  raise SystemExit('The skill already exists; no files were changed. Review it before replacing.')
 verify_payloads()
 root.mkdir(parents=True)
 unpack(KIT/'sources/rekordbox-mcp-base.zip',root/'rekordbox-mcp')
 unpack(KIT/'sources/CueGen-source.zip',root/'cuegen/source')
 unpack(KIT/'sources/CueGen.1.0.37.win-x64.exe.zip',root/'cuegen/bin')
 shutil.copytree(KIT/'overlay/rekordbox_mcp',root/'rekordbox-mcp/rekordbox_mcp',dirs_exist_ok=True)
 shutil.copy2(KIT/'requirements-windows.txt',root/'rekordbox-mcp/requirements-windows.txt')
 for name in ['run_rekordbox_mcp.py','verify_connection.py','stage_cuegen.py']:
  shutil.copy2(KIT/name,root/name)
 settings={'database':str(a.database.resolve()) if a.database else None}
 (root/'dj-stack.json').write_text(json.dumps(settings,indent=2),encoding='utf-8')
 shutil.copy2(KIT/'manifest.json',root/'source-manifest.json')
 if not a.prepare_only:
  subprocess.run([sys.executable,'-m','venv',str(root/'rekordbox-mcp/.venv')],check=True)
  python=root/'rekordbox-mcp/.venv/Scripts/python.exe'
  subprocess.run([str(python),'-m','pip','install','-r','requirements-windows.txt'],cwd=root/'rekordbox-mcp',check=True)
  subprocess.run([str(python),'-m','pip','check'],check=True)
  if a.register_mcp:register(root)
  if a.install_skill:
   dest=Path.home()/'.agents/skills/rekordbox-short-blends'
   if dest.exists():raise RuntimeError('Skill already exists; existing skill was not overwritten')
   shutil.copytree(KIT/'skills/rekordbox-short-blends',dest)
   (dest/'references/installation.json').write_text(json.dumps({'install_root':str(root)},indent=2),encoding='utf-8')
   print('Installed portable skill:',dest)
 print('Installed files at:',root)
 print('No Rekordbox database was opened. Next: run verify_connection.py with the new venv Python.')

if __name__=='__main__':main()
