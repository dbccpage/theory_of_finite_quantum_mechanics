"""Add honest companion records to live code; never alter captured source bytes."""
import ast,hashlib,json,re,yaml
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=next(p for p in B.parents if (p/'dag/pfp/prepare_stage.py').is_file())
selected=json.loads((B/'selection.json').read_bytes())['nodes']
subjects=[ROOT/p for p in ['code/python/src/qm/l1_import_exact.py','code/python/tests/test_l1_import_exact.py','dag/pfp/l1_import_checker.py','code/rust/src/finite_probability/l1_import_exact.rs','code/rust/src/finite_probability/examples/l1_import_exact_replay.rs','code/rust/src/finite_probability/lib.rs','lean4/PromptL1Imports.lean','lean4/lakefile.lean']]
subjects+=list((ROOT/'lean4').glob('PromptL1ImportScope*.lean'))
subjects+=list(B.glob('*.py'))+list((B/'tools').glob('*.py'))
for row in selected:subjects += [ROOT/row['run']/name for name in ('check_candidate.py','format_certificate.py')]
subjects=sorted(set(subjects));records=[]
for path in subjects:
    rel=path.relative_to(ROOT).as_posix();data=path.read_bytes();digest=hashlib.sha256(data).hexdigest();text=data.decode('utf8')
    if path.suffix=='.py':symbols=[n.name for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    elif path.suffix=='.rs':symbols=re.findall(r'^pub (?:fn|mod|struct|enum) (\w+)',text,re.M)
    else:symbols=re.findall(r'^(?:theorem|def|lean_lib|package) (\w+)',text,re.M)
    domain=path.name in ('l1_import_exact.py','l1_import_exact.rs','l1_import_checker.py','PromptL1Imports.lean','verify_batch.py')
    level='L3' if domain else 'L2' if 'test_' in path.name or 'tools' in path.parts or B in path.parents else 'L1'
    shared={'schema_id':'finite-qm.code-companion.v1','subject':rel,'source_sha256':digest,'authority_effect':'None'}
    ref=B.relative_to(ROOT).as_posix()+'/README.md'
    contract=dict(shared,contract_urn='urn:finite-qm:pfp:112-131:'+hashlib.sha256(rel.encode()).hexdigest()[:20],symbols=symbols,owned_invariants=['Only the literal definitions and declared bounded replay contract of this source are claimed.','Source bytes and actual stage/native receipts are retained; source labels and policy flags do not admit a mathematical or physical target.'],boundaries=['No full refined-carrier operad or blanket original-target closure.','No production panic-freedom or arbitrary unreviewed-input contract is inferred for finite replay helpers.'],evidence=[ref])
    score=dict(shared,rubric='SCORING.md v2.0.0 section1.4',capability_level=level,engineering_grade=None,composite_score=None,assessment_status='incomplete_no_completed_score_token',gates={g:{'grade':None,'status':'formal_scoring_not_performed'} for g in ['G1','G2','G3','G4','G5']},refusal_reason='A complete five-gate engineering-grade assessment was not performed. Native/kernel/custody receipts support their stated bounded scopes and do not justify an invented grade.',evidence=[ref])
    doc=dict(shared,purpose='Exact domain computation/checking with explicit remaining interfaces.' if domain else 'Live batch replay, build, test or hook-installation support; not a physical or proof-authority service.',design={'profile':'Exact or symbolic on reviewed carriers; any binary64 use is diagnostic only.','frozen_sources':'Historical input/construction/source snapshots are immutable custody assets and receive no documentary backfill.'},boundaries=contract['boundaries'],evidence=[ref])
    for suffix,value in [('.contract.yaml',contract),('.score.yaml',score),('.doc.yaml',doc)]:
        target=path.with_name(path.name+suffix)
        if target.exists():
            backup=B/'review/previous_companions'/target.relative_to(ROOT);backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(target.read_bytes())
        target.write_bytes(yaml.safe_dump(value,sort_keys=False,allow_unicode=True,width=100).encode())
    records.append({'subject':rel,'sha256':digest,'capability_level':level,'engineering_grade':None,'companions':[rel+s for s in ('.contract.yaml','.score.yaml','.doc.yaml')]})
(ROOT/B.relative_to(ROOT)/'review/companion_records.json').write_bytes((json.dumps({'scope':'Live newly added/edited production and replay code only. Frozen source copies remain custody assets; no repository-wide legacy companion audit is claimed.','records':records,'subjects':len(records),'companions':3*len(records),'no_completed_grade_tokens':True},indent=2)+'\n').encode())
print(json.dumps({'live_subjects':len(records),'companions':3*len(records),'all_engineering_grades':None}))
