"""Run CueGen only on a copied database, never apply to the live library."""
import argparse,copy,json,shutil,subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
import sqlcipher3
from run_rekordbox_mcp import application_key,library_path
ROOT=Path(__file__).resolve().parent
def connect(path,readonly=True):
 db=sqlcipher3.connect(path.as_uri()+'?mode=ro',uri=True) if readonly else sqlcipher3.connect(str(path))
 db.execute("PRAGMA key = '"+application_key().replace("'","''")+"'");db.row_factory=sqlcipher3.Row
 assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 return db
def rows(db,t):return [dict(r) for r in db.execute('SELECT * FROM "'+t.replace('"','""')+'"')]
def main():
 p=argparse.ArgumentParser();p.add_argument('--track-id',required=True);a=p.parse_args()
 live=library_path().resolve();source=connect(live)
 track=dict(source.execute('SELECT * FROM djmdContent WHERE ID=?',(a.track_id,)).fetchone())
 assert track['AnalysisDataPath'],'Analyze this test track in Rekordbox first'
 audio=Path(track['FolderPath']);assert audio.exists()
 glob=audio.as_posix();assert not any(c in glob for c in '*?[]{}'),'Use a test track without glob metacharacters in its path'
 assert source.execute('SELECT count(*) FROM djmdContent WHERE FolderPath=?',(track['FolderPath'],)).fetchone()[0]==1
 run=ROOT/'cuegen/trials'/datetime.now().strftime('%Y%m%d-%H%M%S-%f');run.mkdir(parents=True)
 target=connect(run/'master.db',False);source.backup(target);target.close();source.close()
 shutil.copy2(run/'master.db',run/'before.db')
 relative=Path(track['AnalysisDataPath'].lstrip('/\\')).parent
 assert relative.parts and '..' not in relative.parts
 shutil.copytree(live.parent/'share'/relative,run/'share'/relative)
 exe=next((ROOT/'cuegen/bin').rglob('CueGen.Console.exe'))
 result=subprocess.run([str(exe),'--database='+str(run/'master.db'),'--phrase','--hotcues','--merge','--max=8','--distance=4','--glob='+glob,'--verbosity=info','--progress-'],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
 log=result.stdout+result.stderr;(run/'cuegen.log').write_text(log,encoding='utf-8')
 assert 'Finished cue points creation without errors' in log,'CueGen did not confirm success; see the trial log. Live library is unchanged.'
 before=connect(run/'before.db');after=connect(run/'master.db',False)
 old_cues=[dict(r) for r in before.execute('SELECT * FROM djmdCue WHERE ContentID=?',(a.track_id,))]
 cues=[dict(r) for r in after.execute('SELECT * FROM djmdCue WHERE ContentID=?',(a.track_id,))]
 cache=after.execute('SELECT Cues,rb_cue_count FROM contentCue WHERE ContentID=?',(a.track_id,)).fetchone()
 assert cache is not None,'No cue cache exists on the trial; analyze a native Rekordbox test track first'
 entries=json.loads(cache[0]);assert {e['ID'] for e in entries}=={c['ID'] for c in cues}
 # CueGen 1.0.37 leaves the cached count stale. Repair only the test copy.
 after.execute('UPDATE contentCue SET rb_cue_count=? WHERE ContentID=?',(len(entries),a.track_id));after.commit()
 canon=lambda rs:Counter(tuple(sorted(r.items())) for r in rs)
 changes={}
 for t, in before.execute("SELECT name FROM sqlite_master WHERE type='table'"):
  old,new=canon(rows(before,t)),canon(rows(after,t));removed,added=old-new,new-old
  if not removed and not added:continue
  assert t in ('djmdCue','contentCue'),'Unexpected trial change: '+t
  assert all(str(dict(r)['ContentID'])==a.track_id for r in list(removed)+list(added))
  if t=='djmdCue':assert not removed,'An existing cue changed; reject this trial'
  changes[t]={'removed':sum(removed.values()),'added':sum(added.values())}
 assert all(c in cues for c in old_cues),'Existing cues were changed'
 assert after.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 before.close();after.close()
 report={'status':'trial_verified','live_library_modified':False,'track_id':a.track_id,'trial_directory':str(run),'cuegen_exit_code':result.returncode,'old_cues':len(old_cues),'trial_cues':len(cues),'changes':changes,
 'note':'Version 1.0.37 can exit 1 on success. This tool checks its log and the actual complete database diff. No live-apply option exists.'}
 (run/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
