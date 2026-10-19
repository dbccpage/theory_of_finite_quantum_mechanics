import copy,json,shutil,yaml
from pathlib import Path
from domain_submission import ROOT,s
BATCH=ROOT/'dag/results/batches/20261019T015232Z_next_ten';REVIEW='20261019_next_ten_audit'
if not (BATCH/'review/initial_structure/structure_receipt.json').exists():s.native.record(BATCH/'review/initial_structure','structure',[__import__('sys').executable,'-X','utf8','dag/pfp/validate_prompts.py'])
original_save,original_yaml=s.save,s.yaml_new
def identical_save(path,data):
    if path.exists():
        if json.loads(path.read_bytes())!=data:raise ValueError('Resume would change retained JSON: '+str(path))
    else:original_save(path,data)
def identical_yaml(path,data):
    if path.exists():
        if yaml.safe_load(path.read_bytes())!=data:raise ValueError('Resume would change retained YAML: '+str(path))
    else:original_yaml(path,data)
s.save,s.yaml_new=identical_save,identical_yaml
for node in json.loads((BATCH/'selection.json').read_bytes())['nodes']:
    task=node['node_id'];run=ROOT/node['run'];review=run.parent.parent/'reviews'/REVIEW
    s.save(review/'run_manifest.json',{'scope':'Original stage artifacts sealed before review refinements. No stage output overwritten.','artifacts':[{'path':p.relative_to(run).as_posix(),'sha256':s.sha(p)} for p in sorted(run.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    path=ROOT/node['operad_collection'];before=review/'collection_before_review.yaml'
    if before.exists():
        if before.read_bytes()!=path.read_bytes():raise ValueError('Resume requires explicit custody of already refined canonical collection')
    else:shutil.copyfile(path,before)
    collection=yaml.safe_load(path.read_bytes());delta=yaml.safe_load((run/'p5/operad_delta.yaml').read_bytes())
    if task=='FQ-ENTROPY-DICHOTOMY-BAKER':
        bad=delta['checked_compositions'].pop(1);bad['evidence_status']='Review rejected this direct insertion: a single bound is not the required bound family. Original P0/P5 records remain sealed.';delta['failed_compositions'].append(bad)
        template=copy.deepcopy(next(g for g in delta['add_or_refine_generators'] if g['id']=='log_series'))
        template.update({'id':'spectrum_log_bounds','ordered_inputs':['NormalizedRationalSpectrum','PositiveTermBudget'],'output':'RationalLogSeriesBounds','arity':2,'hypotheses':['Same complete normalized nonnegative rational spectrum and positive finite budget; zero weights contribute zero without evaluating log0.'],'semantic_predicate':'Apply the actual native per-coordinate loop and retain one bound per coordinate in the same spectrum order.','implementation_note':'This is the existing explicit loop in entropy_exact.certify, with a correctly typed indexed-family result; it is not a newly proved operad instance.'})
        delta['add_or_refine_generators'].append(template)
        delta['checked_compositions'].append({'outer_operation':'entropy_sum','input_slot':1,'inner_operation':'spectrum_log_bounds','colour_match':'RationalLogSeriesBounds -> RationalLogSeriesBounds','hypothesis_match':'Same complete spectrum order and retained term budget; zero entries handled explicitly.','licensing_relations':['series_identity','rational_tail'],'evidence_status':'Actual native per-coordinate bound family and weighted interval sums checked; finite-tail formal transport remains open.'})
    for g in delta['add_or_refine_generators']:
        g['evidence_status']='Reviewed finite native predicates on the retained exact inputs. Literal kernel statements and remaining formal transports have separate scope; no complete refined-carrier operad is claimed.'
    for r in delta['add_or_refine_relations']:
        old=r.get('evidence_status','')
        r['historical_evidence_annotation']=old
        if 'pending' in old.lower() or 'await' in old.lower() or 'P3 proof candidate' in old:
            r['evidence_status']='The retained accepted P2 host gates passed for the final candidate; consult the compiled literal anchor signatures and this relation scope. Earlier pending annotation is preserved separately.'
        r['audit_scope_rule']='Compiled module anchors are references to literal statements, not a blanket proof of every generator or relation. Refined-carrier and rational/real transport obligations remain explicit.'
    config=json.loads((review/'config.json').read_bytes());binding={'task_id':task,'review_id':REVIEW,'accepted_candidate':node['run']+'/'+config['accepted_attempt']+'/candidate.json','accepted_host':node['run']+'/'+config['accepted_host']+'/host_check.json','reviewer':'Same local Codex researcher; native domain checkers are independent code predicates, not an independent author.'}
    s.yaml_new(review/'operad_delta.yaml',delta);s.save(review/'scope_review.json',{**binding,'claim_boundary':json.loads((run/'p5/candidate.json').read_bytes())['claim_boundary'],'finding':'The shared helper accepted incomplete declared construction-source coverage. A successor now requires complete expected pin identity and the exact sealed request. The original numerical certificates were not changed.','operad_finding':'Entropy single-bound-to-family insertion was mistyped and is replaced by the existing native spectrum-loop operation with an explicit family output.' if task=='FQ-ENTROPY-DICHOTOMY-BAKER' else 'Retained operation colours, arities, conditional hypotheses, failed compositions, semantic identities and open formal coherence remain scoped.'})
    pres=collection['presentation'];pres.update({'status':'scoped_result_audited_pending_final_integration','generators':delta['add_or_refine_generators'],'relations':delta['add_or_refine_relations'],'compositions':delta['checked_compositions'],'failed_compositions':delta['failed_compositions'],'counterexamples':delta['counterexamples'],'coherence_obligations':delta['open_obligations']})
    colours=sorted({g['output'] for g in pres['generators']}|{c for g in pres['generators'] for c in g['ordered_inputs']});prior={c['id']:c['meaning'] for c in pres['colours']};pres['colours']=[{'id':c,'meaning':prior.get(c,'Scoped semantic coordinate family with explicit source and ordering hypotheses.')} for c in colours]
    pres['identities']=[{'colour':c,'proposed_operation':'id_'+c,'signature':c+' -> '+c,'status':'Semantic identity on the stated carrier; a full refined-carrier operad in Lean remains open.'} for c in colours]
    slots=collection['operad_slots'];m2=slots[s.prepare.SLOTS[1]];m2['operations']=[{'catalog_id':g['id'],'inputs':g['ordered_inputs'],'output':g['output'],'semantic_predicate':g['semantic_predicate']} for g in pres['generators']];m2['composition_plan']=pres['compositions']
    collection['latest_review']={'path':review.relative_to(ROOT).as_posix(),'status':'scope_reviewed_pending_final_integration','sealed_run_manifest':(review/'run_manifest.json').relative_to(ROOT).as_posix(),'operad_delta':(review/'operad_delta.yaml').relative_to(ROOT).as_posix(),'successor_checker':(review/'check_candidate.py').relative_to(ROOT).as_posix(),'source_status_rule':'Historical source labels and bottleneck prose are retained annotations; the explicit run/review scope governs reuse.'}
    path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode())
    print(json.dumps({'task':task,'review_generators':len(pres['generators']),'scope_review':'pending final gates'}),flush=True)
