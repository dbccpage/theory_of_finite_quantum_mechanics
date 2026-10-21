"""Re-run the source-pinned local verification into a NEW output directory.
AuthorityEffect: None. No canonical DAG mutations, provider calls or Git writes.
"""
from pathlib import Path
import argparse, concurrent.futures, datetime, hashlib, importlib.util
import json, os, re, subprocess, sys, time

RUN = Path(__file__).resolve().parents[1]
ROOT = RUN.parents[4]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    pins = json.loads((RUN/'p2/source_pins.json').read_text(encoding='utf-8'))
    failures = [p for p,h in pins['files'].items() if digest(ROOT/p) != h]
    if digest(RUN/'p1/candidate.json') != pins['candidate_sha256']:
        failures.append('p1/candidate.json')
    if failures:
        raise ValueError('Source pin mismatch: '+str(failures))
    commands = [
        ('lean', ['lake','build','ComplexFieldSelection'], ROOT/'lean4'),
        ('rust', ['cargo','test','--manifest-path','code/rust/Cargo.toml','--offline','-p','tfqm_finite_probability','--lib','complex_selection'], ROOT),
        ('python', [sys.executable,'-X','utf8','-m','pytest','code/python/tests/test_complex_selection.py','-q'], ROOT),
        ('candidate', [sys.executable,'-I','-X','utf8','code/python/src/qm/complex_selection.py',str(RUN/'p1/candidate.json')], ROOT),
        ('dag', [sys.executable,'-I','-X','utf8','dag/validate_derivation_dag.py','--no-files'], ROOT),
        ('sync_unified', [sys.executable,'-I','-X','utf8','dag/sync_unified_dag.py','--check'], ROOT),
        ('sync_applications', [sys.executable,'-I','-X','utf8','dag/sync_application_branches.py','--check'], ROOT),
        ('sync_pregenesis', [sys.executable,'-I','-X','utf8','dag/sync_pregenesis_to_wdp.py','--check'], ROOT),
        ('contracts', [sys.executable,'-X','utf8','scripts/contract_scores.py','check'], ROOT),
        ('whitespace', ['git','diff','--check'], ROOT),
    ]
    def execute(item):
        name,cmd,cwd=item
        env=os.environ.copy()
        env.setdefault('CARGO_TARGET_DIR',str(ROOT.parent/'cfs-target'))
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        t=time.monotonic()
        p=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (out/(name+'.log')).write_bytes(p.stdout)
        return {'name':name,'argv':cmd,'cwd':str(cwd),'started_utc':start,
                'elapsed_seconds':round(time.monotonic()-t,3),'exit_code':p.returncode,
                'output':name+'.log','output_sha256':hashlib.sha256(p.stdout).hexdigest()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(execute,commands))
    (out/'commands.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    # Axiom audit is meaningful only after a successful build of pinned sources.
    lean=(out/'lean.log').read_text(encoding='utf-8',errors='replace')
    axioms={}
    for name,items in re.findall(r"'(ComplexFieldSelection\.[^']+)' depends on axioms: \[([^]]*)\]",lean):
        axioms[name]=[a.strip() for a in items.split(',') if a.strip()]
    for name in re.findall(r"'(ComplexFieldSelection\.[^']+)' does not depend on any axioms",lean):
        axioms[name]=[]
    source=(ROOT/'lean4/ComplexFieldSelection.lean').read_text(encoding='utf-8')
    expected={'ComplexFieldSelection.'+n for n in re.findall(r'^#print axioms (\w+)',source,re.M)}
    allowed={'propext','Classical.choice','Quot.sound'}
    audit={'headline_count':len(expected),'headlines':axioms,'allowed':sorted(allowed),
           'all_passed':set(axioms)==expected and all(set(a)<=allowed for a in axioms.values())
               and not re.search(r'\b(sorry|admit|native_decide)\b',source)
               and results[0]['exit_code']==0}
    (out/'axioms.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    # Load the independent test module by path, without package-import side effects.
    path=ROOT/'code/python/tests/test_complex_selection.py'
    spec=importlib.util.spec_from_file_location('complex_selection_challenges',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    raw=(RUN/'p1/candidate.json').read_bytes()
    candidate=json.loads(raw)
    control=mod.cs.verify_candidate_bytes(raw)
    challenges=[]
    for name,mutant in mod.mutants(candidate):
        try:
            mod.cs.verify_candidate_bytes(json.dumps(mutant).encode())
        except ValueError as exc:
            challenges.append({'name':name,'rejected':True,'reason':str(exc)})
        else:
            challenges.append({'name':name,'rejected':False})
    challenge={'candidate_sha256':pins['candidate_sha256'],'valid_control':control,
               'mutants':challenges,'all_rejected':all(c['rejected'] for c in challenges)}
    (out/'challenges.json').write_text(json.dumps(challenge,indent=2)+'\n',encoding='utf-8')
    # All tracked sealed files and the canonical DAG must be byte-unchanged from base.
    protected=['dag/derivation_dag.json','dag/pfp/prompt_audit.json','dag/pfp/filename_custody.json','dag/pfp/custody.py','dag/results']
    diff=subprocess.run(['git','diff','--name-only',pins['base_sha'],'--',*protected],cwd=ROOT,capture_output=True,check=True).stdout.decode().splitlines()
    current_prefix=RUN.relative_to(ROOT).as_posix()+'/'
    changed_old=[p for p in diff if not p.startswith(current_prefix)]
    custody={'pins_match':True,'protected_tracked_changes_outside_this_run':changed_old,
             'unchanged':not changed_old,'source_pins_sha256':digest(RUN/'p2/source_pins.json')}
    (out/'custody.json').write_text(json.dumps(custody,indent=2)+'\n',encoding='utf-8')
    passed=all(r['exit_code']==0 for r in results) and audit['all_passed'] and challenge['all_rejected'] and custody['unchanged']
    print(json.dumps({'all_passed':passed,'commands':[(r['name'],r['exit_code']) for r in results],
                      'headlines':len(axioms),'mutants':len(challenges),'output':str(out)},indent=2))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
