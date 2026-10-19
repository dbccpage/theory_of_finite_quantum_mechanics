import copy,hashlib,importlib.util,json,shutil,sys,tempfile
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');STAGING=Path(__file__).resolve().parent
BATCH=ROOT/'dag/results/batches/20261019T015232Z_next_ten';sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
REVIEW='20261019_next_ten_audit'
wrapper='''"""Reviewed successor of the retained original domain checker."""
import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0,str(ROOT/'dag/pfp'))
from review_exact_json import audit_bound
config=json.loads((HERE/'config.json').read_bytes())
spec=importlib.util.spec_from_file_location('original_'+config['task_id'].replace('-','_'),ROOT/config['run']/'check_candidate.py')
original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
def check(request,candidate):
    audit_bound(request,candidate,config['task_id'],HERE/'config.json')
    return original.check(request,candidate)
if __name__=='__main__':print(json.dumps(check(*sys.argv[1:]),indent=2))
'''
for node in json.loads((BATCH/'selection.json').read_bytes())['nodes']:
    task=node['node_id'];run=ROOT/node['run'];review=run.parent.parent/'reviews'/REVIEW
    profile_path=run/'p0/profile.json'
    if profile_path.is_file():profile=json.loads(profile_path.read_bytes());expected_names=list(dict.fromkeys(profile['production_sources']+profile['build_sources']))
    else:
        if task!='FQ-BELL-RATIONAL-VIOLATION-14-5':raise ValueError('Unknown missing profile')
        profile_path=run/'p0/reviewed_missions.json'
        expected_names=['code/python/src/qm/pfp_exact.py','code/python/src/qm/rational_bell.py','code/python/src/qm/bell_separator_extension.py','code/rust/src/finite_probability/pfp_exact.rs','code/rust/src/finite_probability/rational_bell.rs','code/rust/src/finite_probability/examples/rational_bell_replay.rs','code/python/tests/test_rational_bell.py','code/rust/src/finite_probability/lib.rs','code/rust/src/finite_probability/Cargo.toml','code/rust/Cargo.lock','lean4/PromptBellRational.lean','lean4/BellClassicalJointExtension.lean','lean4/DerivationDagQMClosure.lean','lean4/lakefile.lean','lean4/lean-toolchain','lean4/lake-manifest.json']
    attempts={}
    for path in sorted(run.glob('*/request.json')):
        req=json.loads(path.read_bytes())
        if req.get('stage_id') not in ('P1_DERIVE','P3_REPAIR') or not (path.parent/'candidate.json').is_file():continue
        candidate=json.loads((path.parent/'candidate.json').read_bytes());prefix=node['run']+'/'+req['attempt_id']+'/construction/'
        if {p['path'] for p in candidate['source_pins']}!={prefix+p for p in expected_names}:raise ValueError('Actual original construction coverage incomplete: '+task)
        attempts[req['attempt_id']]={'request_sha256':s.sha(path),'source_pins':{p['path']:p['sha256'] for p in candidate['source_pins']}}
    hosts=[]
    for path in run.glob('*/host_check.json'):
        h=json.loads(path.read_bytes())
        if h.get('stage_id')=='P2_VERIFY' and h.get('status')=='accepted_candidate_for_challenge':hosts.append((path.parent.name,h))
    if len(hosts)!=1:raise ValueError('Need one final accepted actual P2: '+task)
    host,h=hosts[0];request=json.loads((run/host/'request.json').read_bytes());accepted=Path(request['candidate']).parent.name
    config={'task_id':task,'run':node['run'],'profile_source':profile_path.relative_to(ROOT).as_posix(),'profile_sha256':s.sha(profile_path),'required_construction_sources':expected_names,'attempts':attempts,'accepted_attempt':accepted,'accepted_host':host,'boundary':'Sealed run successor predicates require the complete declared construction source set and original domain arithmetic. They are not a complete transitive dependency audit, new derivation or independent reviewer.'}
    review.mkdir(parents=True,exist_ok=True);s.save(review/'config.json',config)
    candidate=json.loads((run/accepted/'candidate.json').read_bytes());bad=copy.deepcopy(candidate);bad['source_pins']=bad['source_pins'][:1]
    s.save(review/'original_source_coverage_probe.json',bad)
    original=s.module('coverage_probe_'+task.replace('-','_'),run/'check_candidate.py')
    try:result=original.check(run/accepted/'request.json',review/'original_source_coverage_probe.json')
    except ValueError as error:result={'rejected':True,'reason':str(error)}
    else:result={'accepted_incomplete_source_set':True,'retained_source_count':1,'required_source_count':len(candidate['source_pins']),'domain_result':result}
    s.save(review/'original_probe_result.json',result)
    (review/'check_candidate.py').write_bytes(wrapper.encode())
    print(json.dumps({'task':task,'original_coverage_probe':result.get('accepted_incomplete_source_set',False),'accepted_attempt':accepted}),flush=True)
shutil.copyfile(STAGING/'review_exact_json.py',ROOT/'dag/pfp/review_exact_json.py')
