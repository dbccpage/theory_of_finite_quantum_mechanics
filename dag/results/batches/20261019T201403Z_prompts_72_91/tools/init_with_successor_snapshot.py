"""Start twenty ordered prompt runs; no provider dispatch or theorem acceptance."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import yaml

sys.dont_write_bytecode = True
ROOT = Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
EXTERNAL = Path(r'C:\Users\a343o\source\repos\the_symbol_game')
BATCH_ID = '20261019T201403Z_prompts_72_91'
RUN_ID = '20261019T201403Z_staged'
BATCH = ROOT/'dag/results/batches'/BATCH_ID
spec = importlib.util.spec_from_file_location('stage_preparation', ROOT/'dag/pfp/prepare_stage.py')
prepare = importlib.util.module_from_spec(spec); spec.loader.exec_module(prepare)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, value):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        if p.name=='request.json':return
        if json.loads(p.read_bytes())!=value:raise ValueError('Existing preparation artifact differs '+str(p))
        return
    p.write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())


sys.path.insert(0,str(ROOT/'dag/pfp'))
from custody import Custody
custody=Custody(ROOT)
index = ROOT/'dag/operads/index.json'
nodes = json.loads(index.read_bytes())['nodes']
if nodes[0]['node_id'] != 'FQ-BELL-CLASSICAL-JOINT-EXTENSION':
    raise ValueError('Prompt order changed')
selected = nodes[71:91]
selection = {'schema_id':'finite-qm.ordered-batch.v1','batch_id':BATCH_ID,'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'index_sha256':sha(index),'selection_rule':'Ordered index positions 72 through 91 after the seventy-one completed nodes; no cherry picking.','created_utc':datetime.now(timezone.utc).isoformat(),'execution_mode':'Local Codex researcher and native exact/checker processes using file-based PFP stages. No external provider calls authorized or scheduled; active chat cost unmeasured.','end_state':'Run all twenty, review and repair their evidence/claims, commit, push and open a PR. Merge explicitly requested.','nodes':[]}
for position, node in enumerate(selected, start=1):
    name = node['node_id']
    if any((ROOT/'dag/results'/name/'runs').glob('*/p5/candidate.json')):raise ValueError('Selected prompt already run: '+name)
    run = ROOT/'dag/results'/name/'runs'/RUN_ID
    collection = ROOT/node['operad_collection']; data = yaml.safe_load(collection.read_bytes())
    packet = prepare.build_packet(ROOT/node['prompt'],attempt_id='p0')
    save(run/'p0/request.json',packet)
    records = []
    sources = [('this_repository',node['prompt'],None),('this_repository',node['operad_collection'],None)]
    sources += [(s.get('repository','this_repository'),s['path'],s.get('sha256')) for s in data['source_bindings'] if s.get('path')]
    sources += [('this_repository',p['path'],p['sha256']) for p in data['target'].get('paper_source_pins',[])]
    seen = set()
    for repository, relative, expected in sources:
        key = (repository,relative)
        if key in seen: continue
        seen.add(key)
        actual = (ROOT if repository == 'this_repository' else EXTERNAL)/relative
        record = {'repository':repository,'source_path':relative,'recorded_sha256':expected,'available':actual.is_file()}
        if actual.is_file():
            record['actual_sha256']=sha(actual);record['matches_recorded_pin']=expected is None or expected==record['actual_sha256']
            if expected and not record['matches_recorded_pin']:
                if not custody.matches('paper',relative,expected,name):raise ValueError('Unresolved source pin '+relative)
                record['pin_resolution']='Explicit filename-custody migration; original expected digest retained'
                record['custody_ledger_sha256']=sha(ROOT/'dag/pfp/filename_custody.json')
            snapshot = run/'inputs'/repository/relative;snapshot.parent.mkdir(parents=True,exist_ok=True)
            if snapshot.exists():
                if snapshot.read_bytes()!=actual.read_bytes():
                    if name!='DS-QM212-MAJORANA-PROBLEM' or relative!='dag/operads/ds_qm212_majorana_problem.yaml' or snapshot.read_bytes()!=(BATCH/'custody/majorana_collection_before.yaml').read_bytes():raise ValueError('Unreviewed snapshot drift '+relative)
                    record['historical_collection_snapshot']=snapshot.relative_to(ROOT).as_posix()
                    snapshot=run/'inputs_after_source_review'/repository/relative
                    snapshot.parent.mkdir(parents=True,exist_ok=True)
                    if snapshot.exists():raise ValueError('Successor snapshot exists')
                    shutil.copyfile(actual,snapshot)
            else:shutil.copyfile(actual,snapshot)
            record['snapshot']=snapshot.relative_to(ROOT).as_posix()
        records.append(record)
    save(run/'p0/source_inventory.json',{'task_id':name,'source_records':records,'boundary':'Availability and byte custody only; declaration and mathematical scope still require substantive mining.'})
    row = dict(node,position=position,run=run.relative_to(ROOT).as_posix(),original_target=data['target']['source_statement'],status='P0_request_prepared_sources_retained')
    selection['nodes'].append(row)
    print(json.dumps({'position':position,'node':name,'sources':len(records),'missing':sum(not r['available'] for r in records),'changed_pins':sum(r.get('available') and not r.get('matches_recorded_pin') for r in records)}),flush=True)
save(BATCH/'selection.json',selection)
save(BATCH/'execution_policy.json',{'authority_effect':'None','researcher':'one local Codex agent','external_provider_calls':0,'paid_dispatch_budget':'none reserved; no paid dispatch','candidate_attempt_limit':'No success quota. Retain actual derivation/repair attempts; unresolved target clauses must remain open.','stage_cost':'active chat cost unmeasured; native wall time recorded from executions','stage_policy':'P0 semantic mining and reviewed missions precede P1; P2 native predicates; P3 only actual repair; P4 actual challenges; P5 result or exact obstruction.','batch_stop':'After twenty prompt executions and substantive review, commit/push/open PR and merge after verified checks.'})
