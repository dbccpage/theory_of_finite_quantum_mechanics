"""Read-only replay of received provider bytes, source pins and native receipts."""
import importlib.util,json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=next(p for p in R.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def custody():
 reg=load(R/'registration.json');need(reg['output_token_budget']==120000 and reg['call_limit']==4 and reg['effort']=='xhigh' and reg['model']=='claude-fable-5-1','registration drift')
 for pin in load(R/'source_manifest.json')['files']:
  need(sha(ROOT/pin['snapshot'])==pin['sha256'],'input snapshot mismatch')
  if pin.get('repository')!='the_symbol_game':need(sha(ROOT/pin['path'])==pin['sha256'],'live input source drift')
 adapter=module('custody_stream',R/'stream_call.py');outputs=0;inputs=0;cost=0;calls=[]
 for folder in sorted(R.iterdir()):
  if not folder.is_dir() or not (folder/'dispatch.json').exists():continue
  d=load(folder/'dispatch.json');need(d['status'] in ('completed','completed_truncated'),'unsettled dispatch')
  for pin in d['source_pins']:need(sha(pin['path'])==pin['sha256'],'dispatch source changed')
  need(sha(folder/'raw.sse')==d['raw_sha256'] and sha(folder/'response.json')==d['response_sha256'],'received bytes changed')
  items=list(adapter.events((folder/'raw.sse').read_bytes()))
  if d['status']=='completed':msg=adapter.reconstruct(items)
  else:
   need(folder.name=='p1_derive' and d.get('candidate_available') is False,'unapproved truncation reconciliation')
   starts=[e['message'] for kind,e in items if kind=='message_start'];ends=[e for kind,e in items if kind=='message_delta'];need(len(starts)==1 and ends and items[-1][0]=='message_stop','incomplete terminal accounting')
   need(ends[-1]['delta']['stop_reason']=='max_tokens','not a token-ceiling stop')
   msg=dict(starts[0]);blocks={}
   for kind,e in items:
    need(kind!='error','provider error')
    if kind=='content_block_start':blocks[e['index']]=dict(e['content_block'])
    elif kind=='content_block_delta':
     delta=e['delta'];field={'text_delta':'text','thinking_delta':'thinking','signature_delta':'signature'}.get(delta['type']);need(field is not None,'unexpected delta');blocks[e['index']][field]=blocks[e['index']].get(field,'')+delta[field]
    elif kind=='message_delta':msg.update(e['delta']);msg.setdefault('usage',{}).update(e.get('usage',{}))
   msg['content']=[blocks[i] for i in sorted(blocks)];need(not any(b['type']=='text' and b.get('text') for b in msg['content']),'expected no candidate text')
  need(msg==load(folder/'response.json'),'response not reconstructed from raw')
  received=[json.loads(s) for s in (folder/'received.jsonl').read_text(encoding='utf-8').splitlines()]
  rawlines=(folder/'raw.sse').read_bytes().splitlines();need([v['line'] for v in received]==[s.decode('utf-8') for s in rawlines],'received-line custody')
  need([v['received_utc'] for v in received]==sorted(v['received_utc'] for v in received),'receipt timestamps not ordered')
  text='\n'.join(b['text'] for b in msg['content'] if b['type']=='text');need(text.encode()==(folder/'response.txt').read_bytes(),'visible response changed')
  body=load(folder/'payload.json');need(body['model']==reg['model']==msg['model'] and body['output_config']=={'effort':'xhigh'} and body['stream'] is True,'provider setting mismatch')
  u=msg['usage'];need(u==d['usage'],'usage mismatch');need(type(u['input_tokens']) is int and type(u['output_tokens']) is int,'usage primitive type')
  need(u['output_tokens']<=body['max_tokens']==d['max_tokens']<=120000 and u['input_tokens']<=50000,'call token bound')
  inputs+=u['input_tokens'];outputs+=u['output_tokens'];cost+=u['input_tokens']*10+u['output_tokens']*50
  need(not u.get('cache_creation_input_tokens') and not u.get('cache_read_input_tokens'),'unexpected cache billing')
  calls.append(folder.name)
 need(0<len(calls)<=4 and outputs<=120000 and inputs<=200000 and cost<=8000000,'run budget')
 budget=load(R/'budget.json');need(not budget['unknown_outcome'] and budget['input_used']==inputs and budget['output_used']==outputs and budget['rated_microusd']==cost,'budget replay')
 native=0;failures=0
 for p in R.rglob('*_receipt.json'):
  d=load(p)
  if 'argv' not in d or 'sources' not in d:continue
  need(d['sources_unchanged'] is True,'native source drift')
  for pin in d['sources']:need(sha(R/pin['snapshot'])==pin['sha256'],'native input snapshot changed')
  native+=1;failures+=int(d['exit_code']!=0)
 return {'inference_calls':len(calls),'stages':calls,'input_tokens':inputs,'output_tokens':outputs,'rated_microusd':cost,'invoice_cost':'UNOBSERVED','native_receipts':native,'retained_failed_native_calls':failures,'truncated_no_candidate_calls':sum(1 for c in budget['calls'] if c['status']=='completed_truncated'),'scope':'Custody and actual receipt replay only. Mathematical acceptance comes from the separately bound host checks.'}
if __name__=='__main__':print(json.dumps(custody(),indent=2))
