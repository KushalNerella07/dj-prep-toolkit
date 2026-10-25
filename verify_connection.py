"""Real stdio JSON-RPC MCP handshake and optional read-only library test."""
import argparse,json,os,queue,subprocess,sys,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def verify(library):
 process=subprocess.Popen([sys.executable,'-u',str(ROOT/'run_rekordbox_mcp.py')],cwd=ROOT,
  stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',
  env={**os.environ,'PYTHONIOENCODING':'utf-8'},creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
 messages=queue.Queue();errors=[]
 def read_output():
  for line in process.stdout:messages.put(line)
  messages.put(None)
 def read_errors():
  for line in process.stderr:errors.append(line)
 threading.Thread(target=read_output,daemon=True).start();threading.Thread(target=read_errors,daemon=True).start()
 number=0
 def send(method,params,notification=False):
  nonlocal number
  message={'jsonrpc':'2.0','method':method,'params':params}
  if not notification:number+=1;message['id']=number
  process.stdin.write(json.dumps(message)+'\n');process.stdin.flush()
  if notification:return
  deadline=time.monotonic()+30
  while time.monotonic()<deadline:
   try:line=messages.get(timeout=max(.01,deadline-time.monotonic()))
   except queue.Empty:break
   if line is None:raise RuntimeError('MCP server exited: '+''.join(errors)[-1500:])
   result=json.loads(line)
   if result.get('id')==number:
    if 'error' in result:raise RuntimeError(str(result['error']))
    return result['result']
  raise TimeoutError('MCP request timed out: '+method+'; '+''.join(errors)[-1500:])
 def call(name,args):
  result=send('tools/call',{'name':name,'arguments':args})
  if result.get('isError'):raise RuntimeError(str(result.get('content')))
  return json.loads(next(c['text'] for c in result['content'] if c['type']=='text'))
 try:
  send('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'dj-stack-verifier','version':'1.0'}})
  send('notifications/initialized',{},True)
  names=[t['name'] for t in send('tools/list',{})['tools']]
  assert all(n in names for n in ['get_playlists','search_tracks','get_track_analysis'])
  report={'status':'mcp_connected','tool_count':len(names),'tool_names':names,'library_modified':False}
  if library:
   playlists=call('get_playlists',{});tracks=call('search_tracks',{'limit':10})
   if isinstance(playlists,dict):playlists=playlists.get('result',playlists)
   if isinstance(tracks,dict):tracks=tracks.get('result',tracks)
   report['playlist_count']=len(playlists)
   if tracks:
    for track in tracks:
     data=call('get_track_analysis',{'track_id':str(track.get('id',track.get('ID')))})
     if data['beats']:break
    report['sample']={'title':data['title'],'cue_count':len(data['cues']),'beat_count':len(data['beats'])}
    report['beat_grid_verified']=bool(data['beats'])
   else:report['sample']='Empty library: import and analyze a test track in Rekordbox first.'
  print(json.dumps(report,indent=2),flush=True)
 finally:
  process.stdin.close()
  try:process.wait(timeout=5)
  except subprocess.TimeoutExpired:
   process.terminate();process.wait(timeout=5)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--library',action='store_true');a=p.parse_args();verify(a.library)
