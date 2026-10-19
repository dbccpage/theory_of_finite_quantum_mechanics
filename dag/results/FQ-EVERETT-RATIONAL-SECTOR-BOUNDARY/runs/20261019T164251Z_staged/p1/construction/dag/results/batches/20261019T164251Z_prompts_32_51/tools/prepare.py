"""Manual per-target semantic profiles, then actual exact P1 construction."""
import importlib.util,json,re,sys
from pathlib import Path
BATCH=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('s',BATCH/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
import importlib,types
pkg=types.ModuleType('batch_dynamics');pkg.__path__=[str(s.ROOT/'code/python/src/qm')];sys.modules['batch_dynamics']=pkg
m=importlib.import_module('batch_dynamics.dynamics_exact')
from specs import S

nodes=json.loads((BATCH/'selection.json').read_bytes())['nodes'];deps=json.loads((BATCH/'lean_order.json').read_bytes())
production=['code/python/src/qm/dynamics_exact.py','code/python/tests/test_dynamics_exact.py','code/rust/src/finite_probability/dynamics_exact.rs','code/rust/src/finite_probability/examples/dynamics_exact_replay.rs','dag/pfp/dynamics_checker.py','dag/pfp/exact_json.py','dag/pfp/review_exact_json.py']+['lean4/'+p+'.lean' for p in deps]+[(BATCH/'tools/prepare.py').relative_to(s.ROOT).as_posix()]
production+=['code/python/src/qm/structure_exact.py','code/rust/src/finite_probability/structure_exact.rs','dag/pfp/structure_checker.py',(BATCH/'tools/specs.py').relative_to(s.ROOT).as_posix()]
build=['code/rust/src/finite_probability/lib.rs','code/rust/src/finite_probability/Cargo.toml','code/rust/Cargo.lock','lean4/lakefile.lean','lean4/lean-toolchain','lean4/lake-manifest.json']
selected=range(int(sys.argv[1]),int(sys.argv[1])+1) if len(sys.argv)>1 else range(20)
for i in selected:
    node,spec=nodes[i],S[i];task=node['node_id'];run=s.root_run(task);kind=spec['kind']
    if kind=='census':
        text=(s.ROOT/'lean4/H017ExtrasDropone.lean').read_text();part=text.split('def allExtras')[1].split('def lostExtras')[0];names=re.findall(r'FrozenExtra\.(\w+)',part)
        labels=dict(re.findall(r'\| FrozenExtra\.(\w+) => DropVerdict\.(\w+)',text));spec['cases']=[['1' if labels[n]=='lost' else '0' for n in names]]
        s.save(run/'p0/census_declared_inputs.json',{'ordered_identifiers':names,'source_labels':[labels[n] for n in names],'scope':'Literal captured source declarations, not a mathematical necessity oracle.'})
    public={'kind':kind,'cases':spec['cases'],'scope':spec['support'],'unpaid_target':spec['unpaid']}
    (run/'check_candidate.py').write_bytes(("import sys\nfrom pathlib import Path\nROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())\nsys.path.insert(0,str(ROOT/'dag/pfp'))\nfrom dynamics_checker import check as predicate\ndef check(request,candidate):return predicate(request,candidate,"+repr(task)+",Path(__file__).parent/'p1/review_contract.json',ROOT)\nif __name__=='__main__':\n import json\n print(json.dumps(check(sys.argv[1],sys.argv[2])))\n").encode())
    (run/'format_certificate.py').write_bytes(("def lines(data):return ["+repr(kind)+"+'\\t'+'\\t'.join(r['output']) for r in data['records']]\n").encode())
    relations=[{'id':kind+'_relation_'+str(j),'equation_or_predicate':eq,'typing_conditions':'Literal declared operation domains; '+spec['unpaid'],'evidence_status':'P1 candidate; independent native and named kernel gates remain required.','scope':spec['support']} for j,eq in enumerate(spec['equations'])]
    gens={g['id']:g for g in spec['gens']}
    for c in spec['comps']:
        a,b=gens[c['outer_operation']],gens[c['inner_operation']];slot=c['input_slot']
        if a['ordered_inputs'][slot]!=b['output']:raise ValueError('Mistyped operation graft')
        c.update(colour_match=b['output']+' -> '+a['ordered_inputs'][slot],hypothesis_match='Same declared coordinates, coefficients and context; all operation hypotheses must be carried into the graft.',licensing_relations=[r['id'] for r in relations],evidence_status='Semantic substitution supported by the retained finite operation traces and separately scoped named kernel statements. A complete refined-carrier operad is not asserted.')
    delta={'add_or_refine_generators':spec['gens'],'add_or_refine_relations':relations,'checked_compositions':spec['comps'],'failed_compositions':[{'proposal':'Promote the selected step to the unrestricted original target','reason':spec['unpaid']}],'counterexamples':[],'open_obligations':[spec['unpaid'],'Prove the full refined-carrier operad identity, substitution, symmetry and coherence laws; mere colour matches do not instantiate that formal structure.']}
    anchors=['QuantumMechanics.PromptDynamics.'+n for n in spec['anchors']]
    boundary={'supports':spec['support'],'does_not_support':spec['unpaid'],'narrowest_claim':spec['support'],'next_test':'Challenge every output coordinate and strict custody/type boundary, then address the explicit unpaid mathematical bridge.'}
    profile={'source_review_status':'semantics_reviewed_for_selected_step','source_scope_review':spec['review'],'carrier':'Literal per-operation finite or admitted scalar carriers','coefficient_ring':'Exact Z, Q, Q(i), Q(sqrt5); admitted a real root only under the stated Lean hypotheses','production_sources':production,'build_sources':build,'independent_predicates':['Independent domain equations and actual matrix/graph/quotient arrays recompute every output.','Exact public input, canonical rational primitive types, complete source pins and exact sealed request bytes.','Full native cross-language output equality and actual named Lean axiom reports; no label-based target promotion.'],'challenge_plan':'Alter every output coordinate, input identity, primitive types, source set and sealed request.','composition_tree':spec['equations'],'anchors':production+anchors,'checker_id':'independent-dynamics-'+kind+'-v1','python_test':'code/python/tests/test_dynamics_exact.py','rust_filter':'dynamics_'+kind,'lean_source':'lean4/PromptDynamics.lean','lean_anchors':anchors,'rust_example':'dynamics_exact_replay','construction':spec['review'],'claim_boundary':boundary,'result_or_obstruction':spec['support'],'next_mathematical_step':spec['unpaid'],'colour_meanings':{},'report':'# '+task+'\n\n'+spec['review']+'\n\nSupported: '+spec['support']+'\n\nRemaining: '+spec['unpaid']}
    s.p0(task,profile,public,delta);s.begin_p1(task);data=m.certify(kind,spec['cases']);candidate=s.p1(task,data,'\n'.join('\t'.join([kind]+v) for v in spec['cases'])+'\n')
    sys.path.insert(0,str(s.ROOT/'dag/pfp'));from review_exact_json import type_shape
    s.save(run/'p1/review_contract.json',{'task_id':task,'attempts':{'p1':{'request_sha256':s.sha(run/'p1/request.json'),'source_pins':{p['path']:p['sha256'] for p in candidate['source_pins']}}},'data_type_shape':type_shape(data),'boundary':'Only identity and primitive shapes; no numeric output oracle.'})
    print(json.dumps({'task':task,'stage':'P1_DERIVE','records':len(spec['cases'])}),flush=True)
