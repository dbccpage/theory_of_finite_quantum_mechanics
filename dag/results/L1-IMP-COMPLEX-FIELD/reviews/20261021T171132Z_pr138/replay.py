"""Re-run the source-pinned local verification into a NEW output directory.
AuthorityEffect: None. No canonical DAG mutations, provider calls or Git writes.
"""
from pathlib import Path
import argparse, concurrent.futures, datetime, hashlib, importlib.util
import json, os, re, subprocess, sys, time

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[4]
RUN = ROOT/'dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection'
REVIEWED_HEAD = '169abaaef04055384c37cfb85e830a0c7c234bcd'
HEADLINES = set("""dimension_formula complex_dimension complex_multiplicative
zero_multiplicative real_count quaternion_count rho_quadratic gaussian_product_span
dimension_selection unrestricted_selection two_pair_selects failing_pair_refutes
real_refuted quaternion_refuted trivial_factor_passes conditional_discharge
real_product_orthogonality delta_symmetric delta_nonzero rho_states rho_distinct
rho_same_product_statistics""".split())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

BASELINE_PINS_SHA = '0fc9743f8257d05a3cdd1e4bdd86d729ede93b8c7d16fb69059a7bc259f4e656'
EXTRA_SOURCES = ['dag/results/L1-IMP-COMPLEX-FIELD/reviews/20261021T171132Z_pr138/independent_oracle.py', 'dag/results/L1-IMP-COMPLEX-FIELD/reviews/20261021T171132Z_pr138/replay.py', 'dag/results/L1-IMP-COMPLEX-FIELD/reviews/20261021T171132Z_pr138/review.json', 'code/python/src/qm/complex_selection.py.doc.yaml', 'code/python/src/qm/complex_selection.contract.score.yaml', 'code/python/tests/test_complex_selection.py.doc.yaml', 'code/python/tests/test_complex_selection.contract.score.yaml', 'code/rust/src/finite_probability/complex_selection.rs.doc.yaml', 'code/rust/src/finite_probability/complex_selection.contract.score.yaml']

def verify_pins(pins):
    baseline = RUN/'p2/commit_source_pins.json'
    if digest(baseline) != BASELINE_PINS_SHA:
        raise ValueError('baseline pin envelope changed')
    required = set(json.loads(baseline.read_bytes())['files']) | set(EXTRA_SOURCES)
    if set(pins) != {'base_sha','candidate_sha256','reviewed_head','files'}:
        raise ValueError('pin envelope fields')
    if pins['reviewed_head'] != REVIEWED_HEAD or pins['base_sha'] != '5c6887bf881af025540653b95c5ba345df73b0a4':
        raise ValueError('review revision identity')
    if set(pins['files']) != required:
        raise ValueError('pin coverage')
    for name, sha in pins['files'].items():
        if not isinstance(sha,str) or not re.fullmatch('[0-9a-f]{64}',sha):
            raise ValueError('invalid pin digest')
        path = (ROOT/name).resolve()
        if not path.is_relative_to(ROOT) or digest(path) != sha:
            raise ValueError('source pin mismatch: '+name)
    if pins['candidate_sha256'] != '2838ec68abb732f11e7862dd8c94ea2d67d8845c2582d09ca07f2f530d391124' or digest(RUN/'p1/candidate.json') != pins['candidate_sha256']:
        raise ValueError('candidate mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    pins = json.loads((REVIEW/'source_pins.json').read_text(encoding='utf-8'))
    verify_pins(pins)
    # Regression controls: an omitted source or corrupted digest cannot pass.
    import copy
    for mode in ('missing','corrupt','extra'):
        bad = copy.deepcopy(pins)
        key = next(iter(bad['files']))
        if mode == 'missing':
            del bad['files'][key]
        elif mode == 'extra':
            bad['files']['../escape'] = '0'*64
        else:
            bad['files'][key] = '0'*64
        try:
            verify_pins(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('pin regression accepted: '+mode)
    commands = [
        ('lean', ['lake','build','ComplexFieldSelection'], ROOT/'lean4'),
        ('rust', ['cargo','test','--manifest-path','code/rust/Cargo.toml','--offline','-p','tfqm_finite_probability','--lib','complex_selection'], ROOT),
        ('python', [sys.executable,'-X','utf8','-m','pytest','code/python/tests/test_complex_selection.py','-q'], ROOT),
        ('independent_oracle', [sys.executable,'-I','-X','utf8',str(REVIEW/'independent_oracle.py'),str(RUN/'p1/candidate.json')], ROOT),
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
        output=p.stdout
        steps=[{'argv':cmd,'exit_code':p.returncode}]
        if name == 'lean' and p.returncode == 0:
            # Re-elaborate current source rather than trusting a cached build message.
            kernel_cmd=['lake','env','lean','ComplexFieldSelection.lean']
            p=subprocess.run(kernel_cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output+=p.stdout
            steps.append({'argv':kernel_cmd,'exit_code':p.returncode})
        (out/(name+'.log')).write_bytes(output)
        return {'name':name,'argv':cmd,'cwd':str(cwd),'started_utc':start,
                'elapsed_seconds':round(time.monotonic()-t,3),'exit_code':p.returncode,
                'steps':steps,'output':name+'.log','output_sha256':hashlib.sha256(output).hexdigest()}
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
    expected={'ComplexFieldSelection.'+n for n in HEADLINES}
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
               'mutants':challenges,'all_rejected':len(challenges)==291 and len({c['name'] for c in challenges})==291 and all(c['rejected'] for c in challenges)}
    (out/'challenges.json').write_text(json.dumps(challenge,indent=2)+'\n',encoding='utf-8')
    verify_pins(pins)
    # Compare protected paths to the reviewed PR, not the mutable base branch.
    protected=['dag/derivation_dag.json','dag/pfp','dag/prompts','dag/operads','dag/results']
    diff=subprocess.run(['git','diff','--name-only',REVIEWED_HEAD,'--',*protected],cwd=ROOT,capture_output=True,check=True).stdout.decode().splitlines()
    current_prefix=REVIEW.relative_to(ROOT).as_posix()+'/'
    changed_old=[p for p in diff if not p.startswith(current_prefix)]
    custody={'pins_match_before_and_after':True,'pin_regressions_rejected':3,
             'protected_tracked_changes_outside_this_review':changed_old,
             'unchanged':not changed_old,'source_pins_sha256':digest(REVIEW/'source_pins.json')}
    (out/'custody.json').write_text(json.dumps(custody,indent=2)+'\n',encoding='utf-8')
    passed=all(r['exit_code']==0 for r in results) and audit['all_passed'] and challenge['all_rejected'] and custody['unchanged']
    print(json.dumps({'all_passed':passed,'commands':[(r['name'],r['exit_code']) for r in results],
                      'headlines':len(axioms),'mutants':len(challenges),'output':str(out)},indent=2))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
