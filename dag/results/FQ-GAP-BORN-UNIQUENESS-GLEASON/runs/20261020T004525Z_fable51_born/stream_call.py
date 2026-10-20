"""Bounded run-local Messages streaming adapter; append raw bytes before interpretation."""
import hashlib,json,re,sys,time,os,urllib.request,urllib.error
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
ROOT=next(p for p in R.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.pending')
 tmp.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode());os.replace(tmp,p)
def load(p):return json.loads(Path(p).read_bytes())
def require(v,m):
 if not v:raise ValueError(m)
def events(raw):
 fields={};data=[]
 for line in raw.splitlines():
  if not line:
   if data:yield fields.get('event','message'),json.loads(b'\n'.join(data))
   fields={};data=[]
  elif line.startswith(b'data:'):data.append(line[5:].lstrip(b' '))
  elif line.startswith(b'event:'):fields['event']=line[6:].strip().decode()
 if data:yield fields.get('event','message'),json.loads(b'\n'.join(data))
def reconstruct(items):
 message=None;blocks={};stopped=False
 for kind,e in items:
  require(not stopped,'event after stop')
  if kind=='error':raise ValueError('provider stream error')
  if kind=='message_start':
   require(message is None,'duplicate start');message=e['message']
  elif kind=='content_block_start':
   require(message is not None and e['index'] not in blocks,'invalid block start');blocks[e['index']]=dict(e['content_block'])
  elif kind=='content_block_delta':
   d=e['delta'];block=blocks[e['index']];field={'text_delta':'text','thinking_delta':'thinking','signature_delta':'signature','input_json_delta':'partial_json'}.get(d['type'])
   require(field is not None,'unsupported delta');block[field]=block.get(field,'')+d[field]
  elif kind=='message_delta':
   require(message is not None,'delta before start');message.update(e.get('delta',{}));message.setdefault('usage',{}).update(e.get('usage',{}))
  elif kind=='message_stop':stopped=True
 require(stopped and message is not None,'incomplete stream')
 require(message.get('stop_reason')=='end_turn','nonterminal/truncated output')
 message['content']=[blocks[i] for i in sorted(blocks)];return message

def main(stage):
 reg=load(R/'registration.json');folder=R/stage
 require(folder.is_dir() and not (folder/'dispatch.json').exists(),'immutable dispatch required')
 packet=load(folder/'request.json');payload=load(folder/'payload.json')
 require(packet['task_id']==reg['task_id'] and payload['model']==reg['model'],'target/model mismatch')
 require(payload['stream'] is True and payload['output_config']=={'effort':reg['effort']},'effort/stream mismatch')
 state=load(R/'budget.json') if (R/'budget.json').exists() else {'calls':[],'input_used':0,'output_used':0,'rated_microusd':0,'unknown_outcome':False}
 require(not state['unknown_outcome'] and len(state['calls'])<reg['call_limit'],'budget/ambiguous outcome')
 remaining=reg['output_token_budget']-state['output_used'];require(remaining>0,'output budget')
 env={}
 for line in Path(r'C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/.env').read_text(encoding='utf-8-sig').splitlines():
  m=re.match(r'\s*(?:export\s+)?([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(.*)',line)
  if m:env[m[1]]=m[2].strip().strip('"\'')
 key=env.get('ANTHROPIC_API_KEY','');require(bool(key),'missing credential')
 headers={'x-api-key':key,'anthropic-version':'2023-06-01','content-type':'application/json'}
 def api(path,body=None):
  data=None if body is None else json.dumps(body,ensure_ascii=False,separators=(',',':')).encode()
  return urllib.request.urlopen(urllib.request.Request('https://api.anthropic.com/v1/'+path,data=data,headers=headers),timeout=300)
 if not (R/'model_access.json').exists():
  with api('models/'+reg['model']) as response:raw=response.read()
  (R/'model_access.json').write_bytes(raw)
 model=load(R/'model_access.json');require(model['id']==reg['model'] and type(model['max_tokens']) is int,'model max unavailable')
 payload['max_tokens']=min(remaining,model['max_tokens'])
 with api('messages/count_tokens',{k:payload[k] for k in ('model','system','messages')}) as response:count=json.load(response)
 save(folder/'token_count.json',count);n=count['input_tokens']
 require(type(n) is int and 0<n<=reg['input_tokens_per_call_limit'] and state['input_used']+n<=reg['input_token_budget'],'input ceiling')
 quote=n*10+payload['max_tokens']*50;require(state['rated_microusd']+quote<=8000000,'rated cost ceiling')
 save(folder/'payload.json',payload)
 pins=[{'path':str(p),'sha256':sha(p)} for p in (folder/'request.json',folder/'payload.json',R/'registration.json',R/'stream_call.py')]
 reservation={'stage':stage,'model':reg['model'],'effort':reg['effort'],'max_tokens':payload['max_tokens'],'input_count':n,'quote_microusd':quote,'status':'reserved','source_pins':pins,'started_utc':datetime.now(timezone.utc).isoformat(),'no_automatic_retry':True}
 save(folder/'dispatch.json',reservation);state['calls'].append(reservation);state['unknown_outcome']=True;save(R/'budget.json',state)
 start=time.monotonic();last=start;event_count=0
 try:
  with api('messages',payload) as response:
   save(folder/'http.json',{'status':response.status,'request_id':response.headers.get('request-id'),'content_type':response.headers.get('content-type')})
   with (folder/'raw.sse').open('xb',buffering=0) as rawfile,(folder/'received.jsonl').open('x',encoding='utf-8') as log:
    for line in response:
     rawfile.write(line);log.write(json.dumps({'received_utc':datetime.now(timezone.utc).isoformat(),'line':line.decode('utf-8').rstrip('\r\n')},ensure_ascii=False)+'\n');log.flush();event_count+=1
     if time.monotonic()-last>=25:
      save(folder/'progress.json',{'received_lines':event_count,'raw_bytes':rawfile.tell(),'elapsed_seconds':round(time.monotonic()-start,1),'state':'streaming'});print(json.dumps({'stage':stage,'state':'streaming','lines':event_count,'seconds':round(time.monotonic()-start)}),flush=True);last=time.monotonic()
  message=reconstruct(events((folder/'raw.sse').read_bytes()));save(folder/'response.json',message)
  require(message.get('model')==reg['model'],'model substitution')
  usage=message['usage'];actualin=usage['input_tokens'];actualout=usage['output_tokens']
  require(type(actualin) is int and type(actualout) is int and 0<=actualout<=payload['max_tokens'],'usage unavailable/excess')
  require(actualin<=reg['input_tokens_per_call_limit'] and not usage.get('cache_creation_input_tokens') and not usage.get('cache_read_input_tokens'),'unexpected billing')
  (folder/'response.txt').write_bytes('\n'.join(b['text'] for b in message['content'] if b['type']=='text').encode())
  require(all(sha(p['path'])==p['sha256'] for p in pins),'source drift during call')
  state['input_used']+=actualin;state['output_used']+=actualout;state['rated_microusd']+=actualin*10+actualout*50;state['unknown_outcome']=False
  reservation.update(status='completed',usage=usage,response_sha256=sha(folder/'response.json'),raw_sha256=sha(folder/'raw.sse'),seconds=round(time.monotonic()-start,3),rated_microusd=actualin*10+actualout*50,invoice_cost='UNOBSERVED')
  save(folder/'dispatch.json',reservation);save(R/'budget.json',state)
  print(json.dumps({'stage':stage,'status':'completed','usage':usage,'run_output_used':state['output_used'],'rated_usd':state['rated_microusd']/1000000}),flush=True)
 except Exception as e:
  failure={'status':'outcome_unknown','error_type':type(e).__name__,'http_status':getattr(e,'code',None),'automatic_retry':False}
  if isinstance(e,urllib.error.HTTPError):(folder/'http_error.bin').write_bytes(e.read())
  save(folder/'failure.json',failure);print(json.dumps(failure),flush=True);raise SystemExit(1)
if __name__=='__main__':main(sys.argv[1])
