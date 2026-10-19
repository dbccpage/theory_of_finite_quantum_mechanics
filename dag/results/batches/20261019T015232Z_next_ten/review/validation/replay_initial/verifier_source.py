"""Read-only replay of exact staged evidence, custody and literal claim ceilings.

This recomputes independent domain predicates; it checks saved native receipts
and logs but does not rerun compilers. Receipt authorship is not authenticated.
"""
import argparse,hashlib,importlib.util,json,re,sys
from decimal import Decimal
from fractions import Fraction as Q
from pathlib import Path
import yaml
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0,str(ROOT/'dag/pfp'))
from exact_json import require,load
REVIEW='20261019_next_ten_audit'
NAMES=[('rational_bell','PromptBellRational',6),('born_ray','PromptBornRay',5),('cabello_frame','PromptCabelloCensus',4),('cabello_obstruction','PromptCabelloParity',3),('carrier_contract','PromptCarrierContract',5),('cech_f2','PromptCechF2',5),('declared_interface','PromptDeclaredInterface',4),('entropy_exact','PromptEntropyExact',5),('born_gap','PromptBornGap',5),('c500_ledger','PromptC500Ledger',4)]
BELL_ANCHORS=['QuantumMechanics.PromptBellRational.'+n for n in ['density_positive','rational_density_and_involutions','exact_born_correlations','all_born_cells_strictly_positive','no_scaled_joint_law']]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def module(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def safe(root,name):
    p=(root/name).resolve();require(p.is_relative_to(root.resolve()) and p!=root.resolve(),'custody:path_escape');return p
def inventory(root,rows):
    require(type(rows) is list and rows,'custody:empty_inventory');names=[r['path'] for r in rows];require(len(names)==len(set(names)),'custody:duplicate_inventory')
    for r in rows:require(sha(safe(root,r['path']))==r['sha256'],'custody:changed_artifact:'+r['path'])
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    require(actual==set(names),'custody:run_inventory_changed');return len(names)
def axiom_reports(text,expected):
    require('sorryAx' not in text and 'error:' not in text,'kernel:unproved_output')
    rows=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",text)
    selected=[(n,a) for n,a in rows if n in expected]
    require(len(selected)==len(expected) and {n for n,_ in selected}==set(expected),'kernel:required_anchor_coverage')
    for _,a in selected:require({x.strip() for x in a.split(',') if x.strip()}<={'propext','Classical.choice','Quot.sound'},'kernel:unapproved_axiom')
def expected_wire(task,run,data):
    if task=='FQ-BELL-RATIONAL-VIOLATION-14-5':
        return ['\t'.join([a['id']]+[q for row in a['pairs'] for q in row]+a['correlations']+[a['chsh'],a['minimum_probability'],str(a['support_assignments']),a['separator_lower'],a['separator_upper'],str(a['violating_mask']) if a['violating_mask'] is not None else 'none']) for a in data['cases']]
    return module('wire_'+task.replace('-','_'),run/'format_certificate.py').lines(data)
def native_receipts(task,run,config,ordinal):
    name,lean_name,python_tests=NAMES[ordinal];attempt=config['accepted_attempt'];host=config['accepted_host'];candidate=load(run/attempt/'candidate.json');request=load(run/host/'request.json');folder=run/host/'native'
    anchors=BELL_ANCHORS if ordinal==0 else load(run/'p0/profile.json')['lean_anchors']
    rust_filter='cabello_certificates' if ordinal==2 else name
    example='cabello_replay' if ordinal==2 else name+'_replay'
    test='test_rational_bell.py' if ordinal==0 else 'test_cabello_frame.py' if ordinal==2 else 'test_'+name+'.py'
    dependencies=request.get('lean_dependencies',[]);expected={'certificate','python','rust','lean','rust_replay'}|{'lean_dependency_'+n for n in dependencies}
    records={p.name.removesuffix('_receipt.json'):json.loads(p.read_bytes(),parse_float=Decimal) for p in folder.glob('*_receipt.json')}
    require(set(records)==expected,'native:command_coverage')
    working={str((ROOT/p['path'].split('/'+attempt+'/construction/',1)[1]).resolve()):p['sha256'] for p in candidate['source_pins']}
    for kind,r in records.items():
        require(type(r.get('exit_code')) is int and r['exit_code']==0 and r.get('sources_unchanged') is True,'native:failed_or_changed')
        argv=r['argv'];py=argv[0] if kind in ('certificate','python') else None
        if kind=='certificate':want=[py,'-X','utf8',str(run/'check_candidate.py'),str(run/attempt/'request.json'),str(run/attempt/'candidate.json')]
        elif kind=='python':want=[py,'-X','utf8','code/python/tests/'+test,'-v']
        elif kind=='rust':want=[argv[0],'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib',rust_filter,'--offline','--locked']
        elif kind=='rust_replay':want=[argv[0],'run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example',example,'--offline','--locked']
        else:
            lean=lean_name if kind=='lean' else kind.removeprefix('lean_dependency_');want=[argv[0],'-j','1','-o',str(ROOT/'lean4/.lake/build/lib/lean'/(lean+'.olean')),lean+'.lean']
        require(argv==want,'native:wrong_command:'+kind);cwd=ROOT/'lean4' if kind.startswith('lean') else ROOT
        require(Path(r['cwd']).resolve()==cwd.resolve(),'native:wrong_cwd');pins={str(Path(p['path']).resolve()):p['sha256'] for p in r['source_pins']}
        expected_pins=dict(working)
        if kind=='certificate':expected_pins.update({str((run/'check_candidate.py').resolve()):sha(run/'check_candidate.py'),str((ROOT/'dag/pfp/exact_json.py').resolve()):sha(ROOT/'dag/pfp/exact_json.py')})
        require(pins==expected_pins and len(pins)==len(r['source_pins']),'native:source_binding')
        for k in ('stdout','stderr'):require(safe(folder,r[k]).is_file(),'native:missing_output')
        expected_stdin=sha(run/('public_cases.tsv' if ordinal==0 else 'public_input.tsv')) if kind=='rust_replay' else None
        require(r['stdin_sha256']==expected_stdin,'native:stdin_binding')
    text=(folder/'lean.stdout.log').read_text();axiom_reports(text,anchors)
    ptest=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',(folder/'python.stderr.log').read_text());rtest=re.search(r'test result: ok\. (\d+) passed; 0 failed',(folder/'rust.stdout.log').read_text())
    require(ptest and int(ptest.group(1))==python_tests,'native:python_test_coverage');require(rtest and int(rtest.group(1))==3,'native:rust_test_coverage')
    lines=(folder/'rust_replay.stdout.log').read_text().splitlines();require(lines==expected_wire(task,run,candidate['data']),'native:full_output_difference')
    return {'Python_tests':python_tests,'Rust_tests':3,'kernel_anchors':len(anchors),'replay_lines':len(lines)}
def verify_node(node,ordinal,execute_mutants=True):
    task=node['node_id'];run=ROOT/node['run'];review=run.parent.parent/'reviews'/REVIEW;config=load(review/'config.json');profile=safe(ROOT,config['profile_source']);require(sha(profile)==config['profile_sha256'],'custody:profile')
    artifacts=inventory(run,load(review/'run_manifest.json')['artifacts']);accepted=config['accepted_attempt'];host=config['accepted_host'];candidate=load(run/accepted/'candidate.json');first=load(run/'p1/candidate.json');h=load(run/host/'host_check.json')
    require(h['status']=='accepted_candidate_for_challenge' and h['candidate_sha256']==sha(run/accepted/'candidate.json'),'stage:accepted_candidate_binding')
    missions=load(run/'p0/reviewed_missions.json');require(load(run/'p0/host_review.json')['reviewed_sha256']==sha(run/'p0/reviewed_missions.json'),'stage:mission_review')
    for attempt,info in config['attempts'].items():
        packet=load(run/attempt/'request.json');c=load(run/attempt/'candidate.json');require(sha(run/attempt/'request.json')==info['request_sha256'],'custody:request_changed')
        require(packet['public_context']['reviewed_work']==missions,'stage:reviewed_problem_changed')
        require(packet['public_context']['original_target']['source_statement']==node['original_target'],'stage:original_target_changed')
        require(c['data']==first['data'],'stage:source_repair_changed_numbers')
        for pin in c['source_pins']:require(sha(safe(ROOT,pin['path']))==pin['sha256'],'custody:construction')
        sources=packet['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['source_pins']
        for pin in sources:require(sha(safe(ROOT,pin['path']))==pin['sha256'],'custody:mission_source')
    for folder in sorted(p for p in run.iterdir() if p.is_dir() and (p/'request.json').is_file()):
        req,sub,check=[load(folder/n) for n in ('request.json','candidate.json','host_check.json')]
        for k in ('task_id','stage_id','attempt_id','input_sha256'):
            require(req[k]==check[k],'stage:checkpoint_host_binding')
            if k in sub:require(req[k]==sub[k],'stage:checkpoint_submission_binding')
        require(req['task_id']==task and (folder/'operad_delta.yaml').is_file() and (folder/'raw_response.json').is_file(),'stage:missing_operad_or_raw')
        delta=yaml.safe_load((folder/'operad_delta.yaml').read_bytes());require(set(delta)=={'add_or_refine_generators','add_or_refine_relations','checked_compositions','failed_compositions','counterexamples','open_obligations'},'operad:delta_fields')
        if req['stage_id']=='P2_VERIFY':
            prior=(folder/req['candidate']).resolve();require(prior.is_relative_to(run),'stage:candidate_escape');require(req['input_sha256']==sub['candidate_sha256']==check['candidate_sha256']==sha(prior),'stage:P2_binding')
        elif 'candidate_sha256' in check:require(check['candidate_sha256']==sha(folder/'candidate.json'),'stage:host_candidate_digest')
        if 'public_context' in req:require(req['input_sha256']==hashlib.sha256(json.dumps(req['public_context'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'stage:context_digest')
    p4=load(run/'p4/request.json');require(p4['public_context']['accepted_candidate']==candidate,'stage:challenge_candidate_changed')
    p5=load(run/'p5/candidate.json');require(p5['source_bindings']==candidate['source_pins'] and p5['input_sha256']==sha(run/'p4/host_check.json'),'stage:P5_binding')
    checker=module('audit_'+task.replace('-','_'),review/'check_candidate.py');result=checker.check(run/accepted/'request.json',run/accepted/'candidate.json');mutants=[]
    if execute_mutants:
        for row in load(run/'p4/host_check.json')['predicate_results']['mutants']:
            try:checker.check(run/accepted/'request.json',safe(run,row['path']))
            except ValueError as error:mutants.append({'id':row['id'],'reason':str(error)})
            else:raise ValueError('challenge:mutant_accepted:'+row['id'])
        probes=[review/'original_source_coverage_probe.json']+[p for p in [review/'partial_kernel_pin_only_probe.json'] if p.exists()]
        for probe in probes:
            try:checker.check(run/accepted/'request.json',probe)
            except ValueError as error:require('construction_source' in str(error) or 'kernel_data_source' in str(error),'review:wrong_coverage_refusal')
            else:raise ValueError('review:incomplete_pins_accepted')
    source_summary=native_receipts(task,run,config,ordinal)
    validator=module('structural_audit',ROOT/'dag/pfp/validate_prompts.py');collection=yaml.safe_load((ROOT/node['operad_collection']).read_bytes())
    require(collection['collection_status']=='source_candidates_collected_semantic_mining_open' and collection['target']['statement_status']=='source_claim_to_scope_check_not_accepted_result','scope:historical_label_promoted')
    require(validator.check_presentation(collection['presentation'])==[],'operad:typing_error')
    reviewed=yaml.safe_load((review/'operad_delta.yaml').read_bytes());require(collection['presentation']['generators']==reviewed['add_or_refine_generators'] and collection['presentation']['relations']==reviewed['add_or_refine_relations'] and collection['presentation']['compositions']==reviewed['checked_compositions'],'operad:canonical_review_binding')
    if ordinal==0:
        uniform=next(a for a in candidate['data']['cases'] if a['id']=='uniform_same_observables')
        for x in range(2):
            for y in range(2):
                table=[sum(Q(1,16) for m in range(16) if ((m>>x)&1)==a and ((m>>(2+y))&1)==b) for a in range(2) for b in range(2)]
                require(table==list(map(Q,uniform['pairs'][2*x+y])),'control:uniform_joint_projection')
    return {'task_id':task,'original_run_artifacts':artifacts,'accepted_attempt':accepted,'independent_domain_result':result,'native_evidence':source_summary,'rejected_P4_mutants':len(mutants),'remaining_obligations':p5['remaining_obligations'],'claim_boundary':p5['claim_boundary']}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--node');parser.add_argument('--skip-mutants',action='store_true');args=parser.parse_args();rows=load(HERE/'selection.json')['nodes'];out=[]
    for i,node in enumerate(rows):
        if args.node and node['node_id']!=args.node:continue
        result=verify_node(node,i,not args.skip_mutants);out.append(result);print(json.dumps(result),flush=True)
    require(bool(out),'audit:empty_selection')
if __name__=='__main__':main()
