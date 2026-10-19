"""Seal the actual stages and refine evidence status without target promotion."""
import importlib.util,json,sys,yaml
from fractions import Fraction as Q
from pathlib import Path
B=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
original_save=s.save
original_yaml=s.yaml_new
def checked_existing(path,data,kind):
    if path.exists():
        actual=(json.loads if kind=='json' else yaml.safe_load)(path.read_bytes())
        if actual!=data:raise ValueError('Nonidentical retained review '+str(path))
    else:(original_save if kind=='json' else original_yaml)(path,data)
s.save=lambda path,data:checked_existing(path,data,'json')
s.yaml_new=lambda path,data:checked_existing(path,data,'yaml')
for row in json.loads((B/'selection.json').read_bytes())['nodes'][10:]:
    run=s.ROOT/row['run'];review=run.parent.parent/'reviews/20261019_boundaries_audit';profile=json.loads((run/'p0/profile.json').read_bytes());accepted=json.loads((run/'accepted.json').read_bytes())
    s.save(review/'run_manifest.json',{'artifacts':[{'path':p.relative_to(run).as_posix(),'sha256':s.sha(p)} for p in sorted(run.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    path=s.ROOT/row['operad_collection'];collection=yaml.safe_load(path.read_bytes());s.yaml_new(review/'collection_before_review.yaml',collection);delta=yaml.safe_load((run/'p5/operad_delta.yaml').read_bytes())
    kind=json.loads((run/'public_input.json').read_bytes())['kind']
    if kind=='majorana':
        for failed in delta['failed_compositions']:
            if 'Actual Majorana P2' in failed.get('reason',''):
                failed['historical_proposal_annotation']=failed['proposal']
                failed['proposal']='Accept AB-BA in an AB+BA anticommutator slot'
                failed['failure_predicate']='G3_WITNESS'
        delta['review_metadata_corrections']={'generic_P3_wrapper_annotation':'The historical wrapper called the submission uncompiled and used a G5_SCOPE repair tag. Actual P2 Lean compilation passed; the failing predicate was G3_WITNESS from the Rust sign/output mismatch. Raw P3 bytes are retained, and this review overlay states the corrected classification.'}
    work_hypotheses=list(dict.fromkeys(h for g in delta['add_or_refine_generators'] for h in g['hypotheses']))
    delta['scope_refinements']={'historical_source_assumptions_are_not_the_full_work_unit_contract':True,'work_unit_admitted_hypotheses':work_hypotheses,'boundary':'Finite carriers, declared operations/readouts and actual native bounds are supplied assumptions, even when the historical source assumption list is empty.'}
    for g in delta['add_or_refine_generators']:g['evidence_status']='Reviewed exact finite native controls. Kernel signatures are separately scoped. Full refined-carrier operad instantiation remains open.'
    for relation in delta['add_or_refine_relations']:
        relation['historical_evidence_annotation']=relation['evidence_status']
        relation['evidence_status']='Accepted actual P2 and P4 controls; only the literal named Lean signatures are kernel theorems. Native array-to-signature and physical transports remain as stated.'
        relation['named_Lean_scope']=profile['lean_anchors']
    # A graft carries its fixed context, not merely a colour name.
    for c in delta['checked_compositions']:c['hypothesis_match']+=' Fixed matrices, signs, gauge unit, original comparison table, row order, sector and pairing (where relevant) must agree across both operations. Formal universal refined-carrier closure is unpaid.'
    delta['open_obligations'].append('A source provider PASS/hash, route index, census label or Boolean flag is not mathematical evidence for the original target. No historical provider receipt is newly authenticated.')
    s.yaml_new(review/'operad_delta.yaml',delta)
    s.save(review/'scope_review.json',{'task_id':row['node_id'],'reviewed_finding':profile['source_scope_review'],'claim_boundary':profile['claim_boundary'],'accepted':accepted,'reviewer':'Same local Codex researcher. Separate checker code and native kernels do not constitute an independent author/model panel.','authority_effect':'None'})
    collection['presentation'].update(status='scoped_stage_result_reviewed',generators=delta['add_or_refine_generators'],relations=delta['add_or_refine_relations'],compositions=delta['checked_compositions'],failed_compositions=delta['failed_compositions'],counterexamples=delta['counterexamples'],coherence_obligations=delta['open_obligations'])
    collection['latest_run']['status']='scoped_result_or_obstruction_reviewed';collection['latest_review']={'path':review.relative_to(s.ROOT).as_posix(),'status':'scope_reviewed_pending_final_integration','operad_delta':(review/'operad_delta.yaml').relative_to(s.ROOT).as_posix()};collection['open_obligations']=delta['open_obligations'];collection['operad_slots'][s.prepare.SLOTS[1]]['composition_plan']=delta['checked_compositions'];collection['operad_slots_scope']['review_refinement']=(review/'scope_review.json').relative_to(s.ROOT).as_posix()
    ambient=collection['operad_slots'][s.prepare.SLOTS[0]]
    ambient['historical_source_assumptions']=list(ambient.get('admitted_assumptions',[]))
    ambient['work_unit_admitted_hypotheses']=work_hypotheses
    ambient['admitted_assumptions']=list(dict.fromkeys(ambient['historical_source_assumptions']+work_hypotheses))
    path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode());(run.parent.parent/'.gitattributes').write_bytes(b'* -text whitespace=-trailing-space,-blank-at-eof\n')
    (review/'README.md').write_bytes(('# '+row['node_id']+' review\n\n'+profile['source_scope_review']+'\n\nSupported: '+profile['claim_boundary']['supports']+'\n\nRemaining: '+profile['claim_boundary']['does_not_support']+'\n\nHistorical source annotations and all stage bytes are preserved. No external provider dispatched. AuthorityEffect: None.\n').encode())
    ix=s.ROOT/'dag/operads/index.json';index=json.loads(ix.read_bytes());node=next(n for n in index['nodes'] if n['node_id']==row['node_id']);node.update(status='scoped_result_or_obstruction_reviewed',latest_review=review.relative_to(s.ROOT).as_posix());ix.write_bytes((json.dumps(index,indent=2,ensure_ascii=False)+'\n').encode())
    print(json.dumps({'task':row['node_id'],'review':'scoped_result_or_obstruction_reviewed'}),flush=True)
