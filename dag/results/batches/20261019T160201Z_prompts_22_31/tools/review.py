"""Review mathematical claims and parameter-sensitive operad substitutions."""
import importlib.util,json,sys,yaml,copy
from fractions import Fraction as Q
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
sys.path.insert(0,str(s.ROOT/'dag/pfp'));from structure_checker import matmul
findings={
'power':['Unrestricted p=1 absolute-value I3 vanishing is false: the mixed-sign triple gives2. The aligned triple still gives0. A new admitted-Real.rpow proof supplies the actual power-equation uniqueness, rather than reusing an unrelated even-exponent lemma.'],
'selection':['A same-carrier pair of normalized readouts refutes selection by that bare interface only; it is not a universal impossibility theorem about all primitive-difference extensions.'],
'quotient':['Fresh compilation exposed absent E003/E005 imports. New minimal implementations preserve input pairs in the difference codomain and place report equality in Zero, matching H000 parityPD. Rejected elaboration/codomain attempts remain retained; no historical source recovery is claimed. Quotient existence does not automatically make delta descend without congruence.'],
'sorkin':['The universal quantifier over triples matters: a particular zero I3 can coexist with nonzero quartic coefficient. Equal embedding weights are not A=B in the source (N0,N1) coordinates; Galois equality is B=0. No full positivity-cone classification follows from two basis probes.'],
'pinching':['The 2x2 pinching inequality and positive rescalings do not prove norm uniqueness over every dimension and every CPTP map. Squared norms are retained exactly; no approximate spectral values occur.'],
'k23':['The scalar K23 objectives4/12 are not substituted for the matrix problem. Actual diagonal arrays give6 and9/2 with different polar constraints. The identity vertex potential is inadmissible for trace-zero repairs. No publication erratum or general Lean LP-duality theorem is claimed.'],
'tsirelson':['Native two-sided matrix SOS identities and the fixed rational quadratic-form bounds have separate formal transports. They do not prove a bound for arbitrary observables or reconstruct tensor/Born structure.'],
'census':['Source-declared lost/open labels are public input data, not computed mathematical necessity verdicts. Fresh kernel list counts and nodup concern the declared census only.'],
'matrix':['The universal source recovery/adjoint proofs use Z[i], finite enumeration, linearity and an admitted pairing. They do not turn Gaussian integers into C or supply a spectral theorem.'],
'time':['The Boolean half-step obstruction does not exclude amplitude roots. Both ±M/2 are unitary roots of swap. Integer tags2k+1 are not analytic logarithms; a repeated-root equation requires the same sign at both insertions.']}
for node in json.loads((BATCH/'selection.json').read_bytes())['nodes']:
    task=node['node_id'];run=s.root_run(task);review=run.parent.parent/'reviews/20261019_structure_audit';accepted=json.loads((run/'accepted.json').read_bytes());profile=json.loads((run/'p0/profile.json').read_bytes());kind=json.loads((run/'public_input.json').read_bytes())['kind']
    s.save(review/'run_manifest.json',{'artifacts':[{'path':p.relative_to(run).as_posix(),'sha256':s.sha(p)} for p in sorted(run.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]})
    path=s.ROOT/node['operad_collection'];s.yaml_new(review/'collection_before_review.yaml',yaml.safe_load(path.read_bytes()));collection=yaml.safe_load(path.read_bytes());delta=yaml.safe_load((run/'p5/operad_delta.yaml').read_bytes())
    if kind=='time':
        for c in delta['checked_compositions']:c['hypothesis_match']+=' The same declared root sign is used at both occurrences when licensing the square-equals-swap relation. Mixed signs give negative swap instead.'
        M=[[(Q(1),Q(1)),(Q(1),Q(-1))],[(Q(1),Q(-1)),(Q(1),Q(1))]];minus=[ [(-a,-b) for a,b in r] for r in M ];cross=matmul(M,minus)
        if cross!=[[(Q(0),Q(0)),(Q(-4),Q(0))],[(Q(-4),Q(0)),(Q(0),Q(0))]]:raise ValueError('Mixed-root control failed')
        counter={'id':'mixed_root_signs','actual_scaled_product':[[[str(a),str(b)] for a,b in r] for r in cross],'normalization':'Divide each root by2; mixed product is -swap, whereas repeated same-sign root gives swap.','scope':'Exact review checker arithmetic on this matrix; no continuous group is constructed.'}
        delta['counterexamples'].append(counter);delta['failed_compositions'].append({'proposal':'License a square-equals-swap equation with arbitrary independent root signs','reason':'Actual mixed signs yield -swap, so the root-choice hypothesis must match.'});s.save(review/'mixed_root_control.json',counter)
    for g in delta['add_or_refine_generators']:g['evidence_status']='Reviewed exact finite native records; literal named kernel statements supply only their own universal scopes. Full refined-carrier operad/coherence remains open.'
    for r in delta['add_or_refine_relations']:
        r['historical_evidence_annotation']=r['evidence_status'];r['evidence_status']='Accepted P2 plus executed P4; consult literal named Lean signatures and retained matrix/coordinate transport obligations rather than treating the whole relation prose as a theorem.'
    delta['open_obligations']+=['No inference from a source flag, declared census label, finite sample, quotient carrier or coordinate name to a stronger mathematical/physical authority claim.']
    s.yaml_new(review/'operad_delta.yaml',delta);s.save(review/'scope_review.json',{'task_id':task,'findings_fixed_or_fenced':findings[kind],'claim_boundary':profile['claim_boundary'],**accepted,'reviewer':'Same local Codex researcher. Independent exact code predicates are not an independent author, panel or human review.','authority_effect':'None'})
    p=collection['presentation'];p.update(status='scoped_stage_result_reviewed',generators=delta['add_or_refine_generators'],relations=delta['add_or_refine_relations'],compositions=delta['checked_compositions'],failed_compositions=delta['failed_compositions'],counterexamples=delta['counterexamples'],coherence_obligations=delta['open_obligations'])
    collection['latest_run']['status']='scoped_result_or_obstruction_reviewed';collection['latest_review']={'path':review.relative_to(s.ROOT).as_posix(),'status':'scope_reviewed_pending_final_integration','operad_delta':(review/'operad_delta.yaml').relative_to(s.ROOT).as_posix()};collection['open_obligations']=delta['open_obligations'];collection['operad_slots'][s.prepare.SLOTS[1]]['composition_plan']=delta['checked_compositions'];collection['operad_slots_scope']['review_refinement']=(review/'scope_review.json').relative_to(s.ROOT).as_posix()
    path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode());(run.parent.parent/'.gitattributes').write_bytes(b'* -text whitespace=-trailing-space,-blank-at-eof\n')
    (review/'README.md').write_bytes(('# '+task+' review\n\n'+'\n\n'.join(findings[kind])+'\n\nSupported: '+profile['claim_boundary']['supports']+'\n\nRemaining: '+profile['claim_boundary']['does_not_support']+'\n\nAll original stage artifacts are sealed; the original prompt and historical source labels remain annotations. AuthorityEffect: None.\n').encode())
    ix=s.ROOT/'dag/operads/index.json';index=json.loads(ix.read_bytes());row=next(n for n in index['nodes'] if n['node_id']==task);row['status']='scoped_result_or_obstruction_reviewed';ix.write_bytes((json.dumps(index,indent=2,ensure_ascii=False)+'\n').encode())
    print(json.dumps({'task':task,'review_findings':findings[kind]}),flush=True)
