import hashlib,importlib.util,json,os,subprocess,sys,tempfile,tomllib,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import setup_windows as setup

class InstallerTests(unittest.TestCase):
 def test_bundled_payload_integrity(self):setup.verify_payloads(ROOT)

 def test_corrupt_payload_is_rejected(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);(root/'asset').write_bytes(b'changed')
   (root/'payload-sha256.json').write_text(json.dumps({'asset':hashlib.sha256(b'original').hexdigest()}))
   with self.assertRaises(ValueError):setup.verify_payloads(root)

 def test_archive_cannot_escape_installation(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);archive=root/'unsafe.zip'
   with zipfile.ZipFile(archive,'w') as z:z.writestr('../outside.txt','unexpected')
   with self.assertRaises(ValueError):setup.unpack(archive,root/'install')
   self.assertFalse((root/'outside.txt').exists())

 def test_registration_preserves_settings_and_refuses_duplicate(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);config=root/'config.toml'
   original='model = "example-model"\n[mcp_servers.other]\ncommand = "keep-me"\n'
   config.write_text(original)
   setup.register(root/'runtime',root)
   parsed=tomllib.loads(config.read_text())
   self.assertEqual(parsed['model'],'example-model')
   self.assertEqual(parsed['mcp_servers']['other'],{'command':'keep-me'})
   self.assertEqual(parsed['mcp_servers']['rekordbox']['enabled_tools'],setup.READ_TOOLS)
   backups=list(root.glob('config.toml.before-dj-*.bak'));self.assertEqual(len(backups),1)
   self.assertEqual(backups[0].read_text(),original)
   after=config.read_bytes()
   with self.assertRaises(RuntimeError):setup.register(root/'runtime',root)
   self.assertEqual(config.read_bytes(),after)

 @unittest.skipUnless(os.name=='nt','Windows installer')
 def test_prepare_only_installs_real_sources_without_database(self):
  with tempfile.TemporaryDirectory() as folder:
   target=Path(folder)/'new-stack'
   result=subprocess.run([sys.executable,str(ROOT/'setup_windows.py'),'--prepare-only','--target',str(target)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   self.assertTrue((target/'rekordbox-mcp/rekordbox_mcp/cue_tools.py').is_file())
   server=(target/'rekordbox-mcp/rekordbox_mcp/server.py').read_text(encoding='utf-8')
   self.assertIn('async def get_track_analysis',server)
   self.assertTrue((target/'cuegen/source/CueGen/Generator.cs').is_file())
   self.assertTrue(list((target/'cuegen/bin').rglob('CueGen.Console.exe')))
   self.assertFalse(list(target.rglob('master.db')))
   self.assertFalse((target/'rekordbox-mcp/.venv').exists())
   again=subprocess.run([sys.executable,str(ROOT/'setup_windows.py'),'--prepare-only','--target',str(target)],capture_output=True,text=True)
   self.assertNotEqual(again.returncode,0)

 def test_source_archives_do_not_ship_audio_or_databases(self):
  for archive in (ROOT/'sources').glob('*.zip'):
   with zipfile.ZipFile(archive) as z:
    self.assertIsNone(z.testzip())
    for name in z.namelist():self.assertNotIn(Path(name).suffix.lower(),{'.mp3','.flac','.wav','.db','.sqlite'})

 def test_release_contents_and_hashes(self):
  spec=importlib.util.spec_from_file_location('build_release',ROOT/'scripts/build_release.py')
  build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
  with tempfile.TemporaryDirectory() as folder:
   release=build.build(folder)
   with zipfile.ZipFile(release) as z:
    names=z.namelist();self.assertIn('dj-prep-toolkit/LICENSE',names)
    self.assertIn('dj-prep-toolkit/setup_windows.py',names)
    self.assertFalse(any('/.git/' in n or '__pycache__' in n for n in names))
    sums=json.loads(z.read('dj-prep-toolkit/SHA256SUMS.json'))
    for name,digest in sums.items():self.assertEqual(hashlib.sha256(z.read('dj-prep-toolkit/'+name)).hexdigest(),digest)

if __name__=='__main__':unittest.main()
