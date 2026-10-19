"""Seal the actual stages and refine evidence status without target promotion."""
import importlib.util,json,sys,yaml
from fractions import Fraction as Q
from pathlib import Path
B=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
for row in json.loads((B/'selection.json').read_bytes())['nodes']:
    run=s.ROOT/row['run'];review=run.parent.parent/'reviews/20261019_resources_audit';profile=json.loads((run/'p0/profile.json').read_bytes());accepted=json.loads((run/'accepted.json').read_bytes())
    s.save(review/'run_manifest.json',{'artifacts':[{'path':p.relative_to(run).as_posix(),'sha256':s.sha(p)} for p in sorted(run.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    path=s.ROOT/row['operad_collection'];collection=yaml.safe_load(path.read_bytes());s.yaml_new(review/'collection_before_review.yaml',collection);delta=yaml.safe_load((run/'p5/operad_delta.yaml').read_bytes())
    kind=json.loads((run/'public_input.json').read_bytes())['kind']
    if kind=='witness':
        # The stage serializer declared Bell's reference F=1 as a literal.
        # Compute the actual rational density and trace pairing during review,
        # rather than describing that literal as an executed matrix product.
        v=[Q(1),Q(0),Q(0),Q(1)]
        rho=[[a*b/2 for b in v] for a in v]
        square=[[sum(rho[i][k]*rho[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        f=sum(square[i][i] for i in range(4));gap=Q(1,2)-f
        if sum(rho[i][i] for i in range(4))!=1 or square!=rho or f!=1 or gap>=0:raise ValueError('Bell reference calculation failed')
        candidate=json.loads((run/accepted['attempt']/'candidate.json').read_bytes())
        if any(Q(r['output'][24])!=f for r in candidate['data']['records']):raise ValueError('Stage Bell reference mismatch')
        control={'id':'review_recomputed_Bell_reference','rho':[[str(z) for z in r] for r in rho],'rho_squared':[[str(z) for z in r] for r in square],'trace_rho_squared':str(f),'witness_half_minus_fidelity':str(gap),'scope':'The earlier literal reference value is now checked by an actual 16-entry rational density product; this is review arithmetic, not an additional compiled matrix theorem.'}
        s.save(review/'bell_reference_control.json',control);delta['counterexamples'].append(control)
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
    path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode());(run.parent.parent/'.gitattributes').write_bytes(b'* -text whitespace=-trailing-space,-blank-at-eof\n')
    (review/'README.md').write_bytes(('# '+row['node_id']+' review\n\n'+profile['source_scope_review']+'\n\nSupported: '+profile['claim_boundary']['supports']+'\n\nRemaining: '+profile['claim_boundary']['does_not_support']+'\n\nHistorical source annotations and all stage bytes are preserved. No external provider dispatched. AuthorityEffect: None.\n').encode())
    ix=s.ROOT/'dag/operads/index.json';index=json.loads(ix.read_bytes());node=next(n for n in index['nodes'] if n['node_id']==row['node_id']);node.update(status='scoped_result_or_obstruction_reviewed',latest_review=review.relative_to(s.ROOT).as_posix());ix.write_bytes((json.dumps(index,indent=2,ensure_ascii=False)+'\n').encode())
    print(json.dumps({'task':row['node_id'],'review':'scoped_result_or_obstruction_reviewed'}),flush=True)
