"""Reconcile authoritative terminal usage from a truncated response; never accept a candidate."""
from pathlib import Path
import json,hashlib,importlib.util,copy
R=Path(__file__).resolve().parent
f=R/'p1_derive';a=R/'accounting_reconciliation';a.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_bytes((json.dumps(v,indent=2)+'\n').encode())
s=importlib.util.spec_from_file_location('adapter',R/'stream_call.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
budget=m.load(R/'budget.json');dispatch=m.load(f/'dispatch.json')
for name,p in [('original_budget.json',R/'budget.json'),('original_dispatch.json',f/'dispatch.json'),('failure.json',f/'failure.json')]: (a/name).write_bytes(p.read_bytes())
items=list(m.events((f/'raw.sse').read_bytes()));message=None;blocks={};stopped=False
for kind,e in items:
 if stopped:raise ValueError('event after terminal')
 if kind=='error':raise ValueError('provider error is not known usage')
 if kind=='message_start':
  if message is not None:raise ValueError('duplicate start')
  message=copy.deepcopy(e['message'])
 elif kind=='content_block_start':blocks[e['index']]=copy.deepcopy(e['content_block'])
 elif kind=='content_block_delta':
  d=e['delta'];field={'text_delta':'text','thinking_delta':'thinking','signature_delta':'signature'}.get(d['type'])
  if not field:raise ValueError('unsupported block delta')
  blocks[e['index']][field]=blocks[e['index']].get(field,'')+d[field]
 elif kind=='message_delta':message.update(e['delta']);message.setdefault('usage',{}).update(e.get('usage',{}))
 elif kind=='message_stop':stopped=True
assert stopped and message['stop_reason']=='max_tokens' and message['model']=='claude-fable-5-1'
message['content']=[blocks[k] for k in sorted(blocks)];usage=message['usage'];assert usage['output_tokens']==dispatch['max_tokens']==41942
text='\n'.join(b['text'] for b in message['content'] if b['type']=='text');assert text==''
save(f/'response.json',message);(f/'response.txt').write_bytes(text.encode())
assert budget['unknown_outcome'] and budget['output_used']==78058
budget['output_used']+=usage['output_tokens'];budget['input_used']+=usage['input_tokens'];cost=usage['input_tokens']*10+usage['output_tokens']*50;budget['rated_microusd']+=cost;budget['unknown_outcome']=False
assert budget['output_used']==120000 and budget['rated_microusd']<=8000000
entry=next(e for e in budget['calls'] if e['stage']=='p1_derive');entry.update(status='completed_truncated',usage=usage,raw_sha256=sha(f/'raw.sse'),response_sha256=sha(f/'response.json'),rated_microusd=cost,invoice_cost='UNOBSERVED',candidate_available=False)
save(f/'dispatch.json',entry);save(R/'budget.json',budget)
save(a/'receipt.json',{'reason':'The adapter rejected max_tokens as a candidate, correctly. Final provider message_delta/message_stop nevertheless establish usage. Reconcile accounting only; no retry or acceptance.','original_budget_sha256':sha(a/'original_budget.json'),'original_dispatch_sha256':sha(a/'original_dispatch.json'),'raw_sha256':sha(f/'raw.sse'),'payload_sha256':sha(f/'payload.json'),'usage':usage,'total_output_tokens':budget['output_used'],'total_input_tokens':budget['input_used'],'total_rated_microusd':budget['rated_microusd'],'candidate_available':False,'automatic_retry':False,'invoice_cost':'UNOBSERVED'})
print(json.dumps({'accounting':'reconciled_from_terminal_provider_usage','output_tokens':budget['output_used'],'rated_usd':budget['rated_microusd']/1000000,'P1_candidate_available':False}))