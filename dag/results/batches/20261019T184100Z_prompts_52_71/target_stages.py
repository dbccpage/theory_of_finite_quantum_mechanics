"""Local artifact/receipt bookkeeping for this twenty-prompt batch.

Substantive per-target profiles and independent domain checkers are required.
This is not a provider runner, theorem oracle, or general auto-solve framework.
"""
import copy,hashlib,importlib.util,json,re,shutil,sys
from pathlib import Path
import yaml

sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
BATCH=ROOT/'dag/results/batches/20261019T184100Z_prompts_52_71'


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m


prepare=module('batch_prepare',ROOT/'dag/pfp/prepare_stage.py')
native=module('batch_native',BATCH/'native.py')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise ValueError('Refusing overwrite: '+str(path))
    path.write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())


def yaml_new(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():raise ValueError('Refusing overwrite: '+str(path))
    path.write_bytes(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=100).encode())


def row(task):
    return next(n for n in json.loads((BATCH/'selection.json').read_bytes())['nodes'] if n['node_id']==task)


def root_run(task):return ROOT/row(task)['run']
def pin(path):return {'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path)}


def snapshots(names,folder):
    result=[]
    for name in names:
        target=folder/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target);result.append(pin(target))
    return result


def p0(task,profile,public,delta):
    run=root_run(task);source=yaml.safe_load((ROOT/row(task)['operad_collection']).read_bytes());original=source['target']['source_statement']
    if profile['source_review_status']!='semantics_reviewed_for_selected_step':raise ValueError('Semantic review required')
    if not profile['source_scope_review'] or not profile['independent_predicates'] or not delta['add_or_refine_generators'] or not delta['add_or_refine_relations']:raise ValueError('Incomplete four missions')
    checker=run/'check_candidate.py';format_file=run/'format_certificate.py'
    if not checker.is_file() or not format_file.is_file():raise ValueError('Checker/complete wire format unavailable')
    inventory=json.loads((run/'p0/source_inventory.json').read_bytes())
    if (run/'p0/additional_source_inventory.json').exists():
        inventory['source_records']+=json.loads((run/'p0/additional_source_inventory.json').read_bytes())['source_records']
    sources=[{'path':r['snapshot'],'sha256':r['actual_sha256']} for r in inventory['source_records'] if r['available']]
    sources+=snapshots([p for p in profile['production_sources'] if not p.endswith('.lean')],run/'p0/operation_sources')
    sources += [pin(checker),pin(ROOT/'dag/pfp/exact_json.py'),pin(format_file)]
    for generator in delta['add_or_refine_generators']:
        generator.setdefault('source_pins',copy.deepcopy(sources));generator.setdefault('evidence_status','Source semantics reviewed; actual native and candidate kernel acceptance remain P2 gates.')
    for relation in delta['add_or_refine_relations']:
        relation.setdefault('source_pins',copy.deepcopy(sources))
    slots={
      prepare.SLOTS[0]:{'mining_status':'FILLED','carrier':profile['carrier'],'coefficient_ring':profile['coefficient_ring'],'source_pins':sources,'public_input':public,'original_target':original,'source_scope_review':profile['source_scope_review'],'admitted_assumptions':source['target']['declared_assumptions']},
      prepare.SLOTS[1]:{'mining_status':'FILLED','operations':[{'catalog_id':g['id'],'inputs':g['ordered_inputs'],'output':g['output'],'semantic_predicate':g['semantic_predicate']} for g in delta['add_or_refine_generators']],'composition_plan':delta['checked_compositions'],'tree':profile['composition_tree']},
      prepare.SLOTS[2]:{'mining_status':'FILLED','algebraic_relations':delta['add_or_refine_relations'],'rejection_predicates':profile['independent_predicates'],'negative_control_plan':profile['challenge_plan']},
      prepare.SLOTS[3]:{'mining_status':'FILLED','certificate_predicates':profile['independent_predicates'],'anchors':profile['anchors'],'unpaid_imports':delta['open_obligations'],'anchor_status':'New Lean anchors are candidate declarations until the retained P2 compiler runs; compiled source leads retain their literal scope.'}}
    catalog={'entries':[{'id':g['id'],'inputs':g['ordered_inputs'],'output':g['output'],'semantic_predicate':g['semantic_predicate']} for g in delta['add_or_refine_generators']]}
    schema={'type':'object','required':['schema_id','task_id','stage_id','attempt_id','input_sha256','source_pins','data'],'properties':{k:{'type':'string'} for k in ('schema_id','task_id','stage_id','attempt_id','input_sha256')}}
    schema['properties'].update({'source_pins':{'type':'array','items':{'type':'object'}},'data':{'type':'object'}})
    reviewed={'original_target':original,'work_unit':{'schema_id':'omega.pfp.finite-qm-work-unit.v1','task_id':task,'objective':original,'selected_catalog_ids':[g['id'] for g in delta['add_or_refine_generators']],'operad_slots':slots,'answer_schema':schema,'checker_id':profile['checker_id']},'catalog':catalog}
    save(run/'p0/profile.json',profile);save(run/'public_input.json',public);save(run/'p0/reviewed_missions.json',reviewed)
    save(run/'p0/host_review.json',{'task_id':task,'review_status':'accepted_for_next_step','reviewed_sha256':sha(run/'p0/reviewed_missions.json'),'checker_pins':[pin(checker),pin(ROOT/'dag/pfp/exact_json.py')],'reviewer':'One local Codex researcher, source and typed-contract review. No independent human/model reviewer.','boundary':'Prerequisites reviewed; no theorem acceptance from FILLED or source status labels.'})
    request=json.loads((run/'p0/request.json').read_bytes());binding={k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')}
    response={**binding,'status':'ready_for_host_review','mission_patch':slots,'source_checks':inventory['source_records'],'next_missing_dependency':'Actual candidate construction and independent/native/kernel P2 execution','operad_delta':delta,'claim_boundary':profile['claim_boundary'],'execution':'Serialized local researcher artifact, not a provider transcript.'}
    save(run/'p0/candidate.json',response);save(run/'p0/raw_response.json',response);yaml_new(run/'p0/operad_delta.yaml',delta)
    save(run/'p0/host_check.json',{**binding,'candidate_sha256':sha(run/'p0/candidate.json'),'status':'reviewed_for_next_step','predicate_results':{'source_scope_review':profile['source_scope_review'],'reviewed_sha256':sha(run/'p0/reviewed_missions.json')},'bounded_failure_codes':[],'operad_delta':delta,'claim_boundary':profile['claim_boundary']})
    return run


def begin_p1(task):
    run=root_run(task)
    request=prepare.build_packet(ROOT/row(task)['prompt'],'P1_DERIVE',attempt_id='p1',reviewed_path=run/'p0/reviewed_missions.json',review_path=run/'p0/host_review.json')
    save(run/'p1/request.json',request)
    return request


def p1(task,data,public_tsv):
    run=root_run(task);profile=json.loads((run/'p0/profile.json').read_bytes())
    request=prepare.build_packet(ROOT/row(task)['prompt'],'P1_DERIVE',attempt_id='p1',reviewed_path=run/'p0/reviewed_missions.json',review_path=run/'p0/host_review.json')
    if (run/'p1/request.json').exists():
        if json.loads((run/'p1/request.json').read_bytes())!=request:raise ValueError('P1 request changed')
    else:save(run/'p1/request.json',request)
    names=list(dict.fromkeys(profile['production_sources']+profile['build_sources']))
    candidate={'schema_id':'finite-qm.domain-certificate.v1',**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'source_pins':snapshots(names,run/'p1/construction'),'data':data}
    save(run/'p1/candidate.json',candidate);delta=yaml.safe_load((run/'p0/operad_delta.yaml').read_bytes())
    response={**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'candidate_certificate':candidate,'construction':profile['construction'],'remaining_obligations':delta['open_obligations'],'operad_delta':delta,'claim_boundary':profile['claim_boundary'],'execution':'Actual local exact producer output; no external provider dispatched.'}
    save(run/'p1/response.json',response);save(run/'p1/raw_response.json',response);yaml_new(run/'p1/operad_delta.yaml',delta)
    (run/'public_input.tsv').write_bytes(public_tsv.encode())
    return candidate


def p2(task,attempt='p1',checkpoint=None,lean_dependencies=()):
    run=root_run(task);profile=json.loads((run/'p0/profile.json').read_bytes());checkpoint=checkpoint or ('p2' if attempt=='p1' else 'p2_after_'+attempt)
    candidate=json.loads((run/attempt/'candidate.json').read_bytes());working=[]
    for p in candidate['source_pins']:
        source=ROOT/p['path'].split('/'+attempt+'/construction/',1)[1]
        if sha(source)!=p['sha256']:raise ValueError('Working source differs from submitted bytes')
        working.append(source)
    digest=sha(run/attempt/'candidate.json');binding={'task_id':task,'stage_id':'P2_VERIFY','attempt_id':checkpoint,'input_sha256':digest};folder=run/checkpoint
    save(folder/'request.json',{**binding,'candidate':'../'+attempt+'/candidate.json','host_action':'Actual independent predicates and native compilation, no acceptance by label.','lean_dependencies':list(lean_dependencies)});save(folder/'candidate.json',{'candidate_sha256':digest})
    py=sys.executable;cargo=str(Path.home()/'.cargo/bin/cargo.exe');lean=str(Path.home()/'.elan/bin/lean.exe')
    commands=[('certificate',[py,'-X','utf8',str(run/'check_candidate.py'),str(run/attempt/'request.json'),str(run/attempt/'candidate.json')],ROOT,None),('python',[py,'-X','utf8',profile['python_test'],'-v'],ROOT,None),('rust',[cargo,'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib',profile['rust_filter'],'--offline','--locked'],ROOT,None),('lean',[lean,'-j','1','-o',str(native.LIB/(Path(profile['lean_source']).stem+'.olean')),Path(profile['lean_source']).name],ROOT/'lean4',None),('rust_replay',[cargo,'run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example',profile['rust_example'],'--offline','--locked'],ROOT,(run/'public_input.tsv').read_bytes())]
    commands[3:3]=[('lean_dependency_'+name,[lean,'-j','1','-o',str(native.LIB/(name+'.olean')),name+'.lean'],ROOT/'lean4',None) for name in lean_dependencies]
    receipts={}
    for kind,command,cwd,stdin in commands:
        receipts[kind]=native.record(folder/'native',kind,command,cwd=cwd,sources=working+([run/'check_candidate.py',ROOT/'dag/pfp/exact_json.py'] if kind=='certificate' else []),stdin=stdin)
        print(json.dumps({'node':task,'gate':kind,'exit_code':receipts[kind]['exit_code'],'seconds':receipts[kind]['seconds']}),flush=True)
    output=(folder/'native/lean.stdout.log').read_text();expected=set(profile['lean_anchors'])
    reports=re.findall(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",output)
    relevant=[(n,a) for n,a in reports if n in expected]
    anchors=len(relevant)==len(expected) and {n for n,_ in relevant}==expected and all({x.strip() for x in a.split(',') if x.strip()}<={'propext','Classical.choice','Quot.sound'} for _,a in relevant) and 'sorryAx' not in output
    wire=module(task.replace('-','_')+'_wire',run/'format_certificate.py');lines=(folder/'native/rust_replay.stdout.log').read_text().splitlines();cross=lines==wire.lines(candidate['data'])
    pylog=(folder/'native/python.stderr.log').read_text();rustlog=(folder/'native/rust.stdout.log').read_text()
    ptest=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',pylog);rtest=re.search(r'test result: ok\. (\d+) passed; 0 failed',rustlog)
    tests=bool(ptest and rtest and int(ptest.group(1))>0 and int(rtest.group(1))>0)
    ok=all(r['exit_code']==0 for r in receipts.values()) and anchors and cross and tests
    delta=yaml.safe_load((run/attempt/'operad_delta.yaml').read_bytes())
    status='accepted_candidate_for_challenge' if ok else 'repairable_candidate_defect'
    result={**binding,'candidate_sha256':digest,'status':status,'checker_pins':[pin(run/'check_candidate.py'),pin(ROOT/'dag/pfp/exact_json.py')],'predicate_results':{'native_exit_codes':{k:v['exit_code'] for k,v in receipts.items()},'required_named_Lean_reports':anchors,'exact_cross_language_full_output':cross,'nonempty_test_coverage':tests,'Python_tests':int(ptest.group(1)) if ptest else None,'Rust_tests':int(rtest.group(1)) if rtest else None,'scope':profile['claim_boundary']},'bounded_failure_codes':[] if ok else ['G5_SCOPE'] if receipts['lean']['exit_code'] or not anchors else ['G3_WITNESS'],'operad_delta':delta}
    save(folder/'host_check.json',result);save(folder/'raw_response.json',result);yaml_new(folder/'operad_delta.yaml',delta)
    save(run/attempt/'host_check.json',{**{k:candidate[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'candidate_sha256':digest,'status':'see_host_checkpoint','host_check':'../'+checkpoint+'/host_check.json'})
    return result


def p4(task,mutators,*,attempt='p1',host_checkpoint='p2',controls):
    run=root_run(task);candidate=json.loads((run/attempt/'candidate.json').read_bytes());checker=module(task.replace('-','_')+'_checker',run/'check_candidate.py')
    request=prepare.build_packet(ROOT/row(task)['prompt'],'P4_CHALLENGE',attempt_id='p4',reviewed_path=run/'p0/reviewed_missions.json',review_path=run/'p0/host_review.json',candidate_path=run/attempt/'candidate.json',host_check_path=run/host_checkpoint/'host_check.json');save(run/'p4/request.json',request)
    accepted=checker.check(run/attempt/'request.json',run/attempt/'candidate.json');results=[]
    for name,mutate in mutators:
        bad=copy.deepcopy(candidate);mutate(bad['data']);path=run/'p4/mutants'/(name+'.json');save(path,bad)
        try:checker.check(run/attempt/'request.json',path)
        except ValueError as error:reason=str(error)
        else:raise ValueError('Counterfeit accepted: '+name)
        results.append({'id':name,'path':path.relative_to(run).as_posix(),'rejected':True,'reason':reason})
    delta=yaml.safe_load((run/attempt/'operad_delta.yaml').read_bytes());delta['counterexamples']+=controls
    response={**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'near_miss':results,'challenged_predicate':json.loads((run/'p0/profile.json').read_bytes())['independent_predicates'],'valid_control':accepted,'challenge_result':'The same independent checker evaluated all saved mutations and the original valid candidate.','operad_delta':delta}
    save(run/'p4/candidate.json',response);save(run/'p4/raw_response.json',response);yaml_new(run/'p4/operad_delta.yaml',delta)
    save(run/'p4/host_check.json',{**{k:request[k] for k in ('task_id','stage_id','attempt_id','input_sha256')},'candidate_sha256':sha(run/'p4/candidate.json'),'status':'survives_executed_challenges','predicate_results':{'mutants':results,'valid_control':accepted,'counterexamples':controls},'bounded_failure_codes':[],'operad_delta':delta})
    return results


def p5(task,*,attempt='p1',host_checkpoint='p2',attempts=None):
    run=root_run(task);profile=json.loads((run/'p0/profile.json').read_bytes());delta=yaml.safe_load((run/'p4/operad_delta.yaml').read_bytes());candidate=json.loads((run/attempt/'candidate.json').read_bytes());host=json.loads((run/host_checkpoint/'host_check.json').read_bytes())
    if host['status']!='accepted_candidate_for_challenge':raise ValueError('Missing accepted host result')
    host_ref=(run/host_checkpoint/'host_check.json').relative_to(ROOT).as_posix()
    for generator in delta['add_or_refine_generators']:
        generator['evidence_status']='Target-specific native predicates checked on retained inputs; relation-specific kernel scope is separate. General refined-carrier operad instantiation remains open.'
        generator['latest_host_check']=host_ref
    for relation in delta['add_or_refine_relations']:
        relation['latest_host_check']=host_ref
        if relation['id'] in profile.get('relation_evidence',{}):relation['evidence_status']=profile['relation_evidence'][relation['id']]
    attempts=attempts or ['p0','p1','p2','p4'];binding={'task_id':task,'stage_id':'P5_RECORD','attempt_id':'p5','input_sha256':sha(run/'p4/host_check.json')}
    save(run/'p5/request.json',{**binding,'host_result':'../'+host_checkpoint+'/host_check.json','challenge':'../p4/host_check.json'})
    result={**binding,'result_or_obstruction':profile['result_or_obstruction'],'attempt_refs':attempts,'source_bindings':candidate['source_pins'],'remaining_obligations':delta['open_obligations'],'operad_delta':delta,'next_mathematical_step':profile['next_mathematical_step'],'claim_boundary':profile['claim_boundary'],'status':'recorded_pending_batch_review','execution_accounting':{'external_provider_calls':0,'chat_cost':'unmeasured','researcher':'one local Codex researcher, independent native predicates, no independent human/model reviewer'}}
    save(run/'p5/candidate.json',result);save(run/'p5/raw_response.json',result);yaml_new(run/'p5/operad_delta.yaml',delta)
    save(run/'p5/host_check.json',{**binding,'candidate_sha256':sha(run/'p5/candidate.json'),'status':'scoped_result_or_obstruction_recorded_pending_batch_review','predicate_results':host['predicate_results'],'bounded_failure_codes':[],'claim_boundary':profile['claim_boundary']})
    path=ROOT/row(task)['operad_collection'];collection=yaml.safe_load(path.read_bytes());colours=sorted({g['output'] for g in delta['add_or_refine_generators']}|{c for g in delta['add_or_refine_generators'] for c in g['ordered_inputs']})
    collection['presentation']={'status':'scoped_stage_result_pending_batch_review','scope':profile['claim_boundary']['narrowest_claim'],'colours':[{'id':c,'meaning':profile['colour_meanings'].get(c,'Scoped semantic carrier with the declared hypotheses.')} for c in colours],'generators':delta['add_or_refine_generators'],'relations':delta['add_or_refine_relations'],'compositions':delta['checked_compositions'],'identities':[{'colour':c,'proposed_operation':'id_'+c,'signature':c+' -> '+c,'status':'Semantic identity; generic function-substitution laws do not instantiate these refined carriers in Lean.'} for c in colours],'symmetric_actions':[],'coherence_obligations':delta['open_obligations'],'failed_compositions':delta['failed_compositions'],'counterexamples':delta['counterexamples']}
    collection['operad_slots']=json.loads((run/'p0/reviewed_missions.json').read_bytes())['work_unit']['operad_slots'];collection['operad_slots_scope']={'work_unit':(run/'p0/reviewed_missions.json').relative_to(ROOT).as_posix(),'scope':'FILLED means reviewed prerequisites for this selected step; original target and unpaid imports retained.'};collection['open_obligations']=delta['open_obligations'];collection['latest_run']={'path':run.relative_to(ROOT).as_posix(),'stage':'P5_RECORD','status':'scoped_result_or_obstruction_pending_batch_review'}
    collection['stage_history']=[{'stage':json.loads((run/a/'request.json').read_bytes())['stage_id'],'attempt':a,'run':run.relative_to(ROOT).as_posix(),'operad_delta':(run/a/'operad_delta.yaml').relative_to(ROOT).as_posix(),'host_check':(run/a/'host_check.json').relative_to(ROOT).as_posix()} for a in attempts+['p5']]
    collection.setdefault('scope_notes',[]).append(profile['source_scope_review']);path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode())
    index=ROOT/'dag/operads/index.json';data=json.loads(index.read_bytes());node=next(n for n in data['nodes'] if n['node_id']==task);node.update({'current_stage':'P5_RECORD','ready_for_derivation':False,'latest_run':run.relative_to(ROOT).as_posix(),'status':'scoped_result_or_obstruction_pending_batch_review'});index.write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
    (run/'README.md').write_bytes((profile['report']+'\n\nEvery executed checkpoint retains an operad delta, source/candidate bindings and actual host results. This is local file-based PFP execution, not an external-provider transcript. No whole-repository or hosted-CI success is claimed. Awaiting the requested batch review. AuthorityEffect: None.\n').encode())
    print(json.dumps({'node':task,'stage':'P5_RECORD','generators':len(delta['add_or_refine_generators']),'relations':len(delta['add_or_refine_relations']),'batch_review':'pending'}),flush=True)
