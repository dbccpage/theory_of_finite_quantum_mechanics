import importlib.util,json
from pathlib import Path
B=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
node=json.loads((B/'selection.json').read_bytes())['nodes'][0];run=s.ROOT/node['run'];c=json.loads((run/'p3/candidate.json').read_bytes());sources=[s.ROOT/p['path'].split('/p3/construction/',1)[1] for p in c['source_pins']]
r=s.native.record(B/'review/pre_batch','rust_all_new_tests',[str(Path.home()/'.cargo/bin/cargo.exe'),'test','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--lib','genesis_','--offline','--locked'],sources=sources+[Path(__file__)])
print(json.dumps({'gate':'all_new_Rust_unit_tests','exit_code':r['exit_code']}),flush=True)
if r['exit_code']:raise ValueError('Retained actual pre-batch native failure')
