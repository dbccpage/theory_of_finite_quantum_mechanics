"""Small source installation and artifact helper; all mathematical specs are manual."""
import importlib.util,shutil,subprocess
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');STAGING=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('stages',ROOT/'dag/results/batches/20261019T015232Z_next_ten/target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
def install(task,name,lean):
    run=s.root_run(task)
    for a,b in [(name+'.py','code/python/src/qm/'+name+'.py'),(name+'.rs','code/rust/src/finite_probability/'+name+'.rs'),(name+'_replay.rs','code/rust/src/finite_probability/examples/'+name+'_replay.rs'),('test_'+name+'.py','code/python/tests/test_'+name+'.py'),(lean+'.lean','lean4/'+lean+'.lean')]:
        if (ROOT/b).exists():raise ValueError('Already installed: '+b)
        shutil.copyfile(STAGING/a,ROOT/b)
    for a,b in [('check_'+name+'.py','check_candidate.py'),('format_'+name+'.py','format_certificate.py')]:shutil.copyfile(STAGING/a,run/b)
    subprocess.run([str(Path.home()/'.cargo/bin/rustfmt.exe'),'--edition','2021',str(ROOT/'code/rust/src/finite_probability'/ (name+'.rs')),str(ROOT/'code/rust/src/finite_probability/examples'/(name+'_replay.rs'))],check=True)
    p=ROOT/'code/rust/src/finite_probability/lib.rs';p.write_bytes((p.read_text()+'\npub mod '+name+';\n').encode())
    p=ROOT/'lean4/lakefile.lean';text=p.read_text();needle='    `PromptCechF2,'
    if needle not in text:raise ValueError('Missing insertion point')
    p.write_bytes(text.replace(needle,needle+'\n    `'+lean+',').encode())
def submit(task,name,lean,public,spec):
    sources=['code/python/src/qm/'+name+'.py','code/python/tests/test_'+name+'.py','code/rust/src/finite_probability/'+name+'.rs','code/rust/src/finite_probability/examples/'+name+'_replay.rs','lean4/'+lean+'.lean']+spec.get('extra_sources',[])
    build=['code/rust/src/finite_probability/lib.rs','code/rust/src/finite_probability/Cargo.toml','code/rust/Cargo.lock','lean4/lakefile.lean','lean4/lean-toolchain','lean4/lake-manifest.json']
    generators=[{'id':n,'ordered_inputs':ins,'output':out,'arity':len(ins),'carrier':spec['carrier'],'coefficient_ring':spec['ring'],'hypotheses':hyps,'semantic_predicate':pred} for n,ins,out,hyps,pred in spec['operations']]
    relations=[{'id':n,'equation_or_predicate':eq,'typing_conditions':typing,'evidence_status':ev,'scope':scope} for n,eq,typing,ev,scope in spec['relations']]
    delta={'add_or_refine_generators':generators,'add_or_refine_relations':relations,'checked_compositions':spec['compositions'],'failed_compositions':spec['failed'],'counterexamples':[],'open_obligations':spec['obligations']}
    anchors=['QuantumMechanics.'+lean+'.'+n for n in spec['anchor_names']]
    profile={'source_review_status':'semantics_reviewed_for_selected_step','source_scope_review':spec['review'],'carrier':spec['carrier'],'coefficient_ring':spec['ring'],'production_sources':sources,'build_sources':build,'independent_predicates':spec['predicates'],'challenge_plan':spec['challenge'],'composition_tree':spec['tree'],'anchors':sources+anchors,'checker_id':spec['checker_id'],'python_test':'code/python/tests/test_'+name+'.py','rust_filter':name,'lean_source':'lean4/'+lean+'.lean','lean_anchors':anchors,'rust_example':name+'_replay','construction':spec['construction'],'claim_boundary':spec['boundary'],'result_or_obstruction':spec['result'],'next_mathematical_step':spec['next'],'colour_meanings':spec.get('colours',{}),'report':spec['report']}
    s.p0(task,profile,public,delta);s.begin_p1(task)
    return s
