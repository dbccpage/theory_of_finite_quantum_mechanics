"""Scope and typed-substitution repair, preserving the complete staged runs."""
import copy,importlib.util,json,yaml
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
rows=json.loads((BATCH/'selection.json').read_bytes())['nodes']
for node in rows:
    task=node['node_id'];run=s.root_run(task);review=run.parent.parent/'reviews/20261019_scope_audit'
    candidate=json.loads((run/'p3b/candidate.json').read_bytes());host=json.loads((run/'p2_after_p3b/host_check.json').read_bytes())
    if host['status']!='accepted_candidate_for_challenge':raise ValueError('Missing accepted repair')
    s.save(review/'run_manifest.json',{'artifacts':[{'path':p.relative_to(run).as_posix(),'sha256':s.sha(p)} for p in sorted(run.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    path=s.ROOT/node['operad_collection'];s.yaml_new(review/'collection_before_review.yaml',yaml.safe_load(path.read_bytes()))
    collection=yaml.safe_load(path.read_bytes());delta=yaml.safe_load((run/'p5/operad_delta.yaml').read_bytes());kind=json.loads((run/'public_input.json').read_bytes())['kind'];gens={g['id']:g for g in delta['add_or_refine_generators']};findings=[]
    if kind=='u1':
        gens['cayley']['output']='PuncturedRationalCirclePoint';gens['inverse_cayley']['ordered_inputs']=['PuncturedRationalCirclePoint']
        keep={('inverse_cayley','cayley')}
        findings.append('Refine the Cayley image/inverse domain to the punctured circle. Powers have no supplied puncture-domain proof; reverse Cayley substitution is not promoted from sampled left-inverse checks.')
    elif kind in ('interference','zero'):
        name='admitted_mix' if kind=='interference' else 'apply_integer_matrix';old=gens[name]['ordered_inputs'][0]
        gens[name]['ordered_inputs']=[('RationalMatrix2' if kind=='interference' else 'IntegerMatrix2'),old];gens[name]['arity']=2
        pop='population' if kind=='interference' else 'exact_population'
        keep={(name,'sign_flip'),(pop,name),(pop,'sign_flip')}
        findings.append('Make the actual matrix an explicit operation argument; population retains exact zero and scale. Keep only evaluated sign/mix/population substitutions in checked compositions.')
    elif kind=='weights':
        gens['weighted_score']['output']='RationalScore';gens['total_mass']['output']='NonnegativeMassUnderDeclaredHypotheses';gens['scaled_bound']['ordered_inputs']=['NonnegativeMassUnderDeclaredHypotheses']
        keep={('scaled_bound','total_mass')}
        findings.append('Separate score from mass. A weighted score cannot be inserted as a normalization mass merely because both use rational scalars. Signed controls do not inhabit the nonnegative-weight refinement.')
        gens['total_mass']['hypotheses']=['p,q are nonnegative for this refined output colour. Signed total-mass arithmetic remains a negative control outside this carrier.']
    else:keep={(c['outer_operation'],c['inner_operation']) for c in delta['checked_compositions']}
    old_comps=delta['checked_compositions'];comps=[]
    for c in old_comps:
        key=(c['outer_operation'],c['inner_operation']);g,h=gens[key[0]],gens[key[1]]
        if key not in keep:
            delta['failed_compositions'].append({**c,'review_finding':'Not licensed as a checked composition on the final refined carriers; missing domain proof or unevaluated substitution.'});continue
        slots=[i for i,v in enumerate(g['ordered_inputs']) if v==h['output']]
        if not slots:raise ValueError('Reviewed graft still mismatched: '+str(key))
        c.update(input_slot=slots[0],colour_match=h['output']+' -> '+g['ordered_inputs'][slots[0]],evidence_status='Reviewed semantic substitution on the declared input hypotheses; native traces are finite, and named kernel statements keep their literal scopes. Full operad coherence remains open.')
        comps.append(c)
    delta['checked_compositions']=comps
    for g in gens.values():
        g['coefficient_ring']='Bytes and exact Nat counts' if kind in ('corpus','custody') else 'Z[i] for Gaussian operations; Z for integer probes; Q for explicitly rational operations'
        g['evidence_status']='Reviewed exact native evidence on retained inputs; consult the literal named Lean statement for any universal claim.'
    for r in delta['add_or_refine_relations']:
        r['historical_evidence_annotation']=r['evidence_status'];r['evidence_status']='Accepted repaired P2 gates and P4 coordinate challenges; universal scope is exactly the separately compiled Lean signatures, not every sentence of this relation.'
    delta['open_obligations']+=['Text literal counts are not semantic proof/axiom counts; sampled native values do not prove universal kernel statements.']
    s.yaml_new(review/'operad_delta.yaml',delta)
    profile=json.loads((run/'p0/profile.json').read_bytes())
    s.save(review/'scope_review.json',{'task_id':task,'findings_fixed':findings,'source_review':profile['source_scope_review'],'claim_boundary':profile['claim_boundary'],'accepted_attempt':'p3b','accepted_host':'p2_after_p3b','initial_failures_retained':['p2','p2_after_p3'],'checker_policy':'Complete construction-source set and exact request bytes enforced from P1; P3 contract evolution retained before/after without numeric oracle.','reviewer':'Same local Codex researcher. Separate native/checker predicates are not an independent author, model panel or human review.','authority_effect':'None'})
    p=collection['presentation'];p.update(status='scoped_stage_result_reviewed',generators=list(gens.values()),relations=delta['add_or_refine_relations'],compositions=comps,failed_compositions=delta['failed_compositions'],counterexamples=delta['counterexamples'],coherence_obligations=delta['open_obligations'])
    colours=sorted({g['output'] for g in gens.values()}|{c for g in gens.values() for c in g['ordered_inputs']})
    p['colours']=[{'id':c,'meaning':'Literal refined operation domain with all stated hypotheses; no automatic carrier identification.'} for c in colours]
    p['identities']=[{'colour':c,'proposed_operation':'id_'+c,'signature':c+' -> '+c,'status':'Semantic identity only; full refined-carrier operad proof remains open.'} for c in colours]
    collection['latest_run']['status']='scoped_result_or_obstruction_reviewed';collection['latest_review']={'path':review.relative_to(s.ROOT).as_posix(),'status':'scope_reviewed_pending_final_integration','operad_delta':(review/'operad_delta.yaml').relative_to(s.ROOT).as_posix()}
    collection['open_obligations']=delta['open_obligations'];slot=collection['operad_slots'][s.prepare.SLOTS[1]];slot['operations']=[{'catalog_id':g['id'],'inputs':g['ordered_inputs'],'output':g['output'],'semantic_predicate':g['semantic_predicate']} for g in gens.values()];slot['composition_plan']=comps
    collection['operad_slots_scope']['review_refinement']=(review/'scope_review.json').relative_to(s.ROOT).as_posix()
    path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode())
    (run.parent.parent/'.gitattributes').write_bytes(b'* -text whitespace=-trailing-space,-blank-at-eof\n')
    (review/'README.md').write_bytes(('# '+task+' review\n\n'+profile['claim_boundary']['supports']+'\n\nRemaining: '+profile['claim_boundary']['does_not_support']+'\n\n'+' '.join(findings)+'\n\nP1 and both rejected compiler attempts remain sealed. The repaired numerical data are unchanged. Full domain/kernel transport and formal operad coherence are not inferred from matching labels.\n').encode())
    index=s.ROOT/'dag/operads/index.json';ix=json.loads(index.read_bytes());row=next(n for n in ix['nodes'] if n['node_id']==task);row['status']='scoped_result_or_obstruction_reviewed';index.write_bytes((json.dumps(ix,indent=2,ensure_ascii=False)+'\n').encode())
    print(json.dumps({'task':task,'reviewed_generators':len(gens),'reviewed_compositions':len(comps),'fixed_findings':findings}),flush=True)
