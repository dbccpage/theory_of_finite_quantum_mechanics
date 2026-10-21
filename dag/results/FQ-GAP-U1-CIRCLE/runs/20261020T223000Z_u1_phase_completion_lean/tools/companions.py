"""Write code-companion contract/score/doc records for the sources of this run through scripts/contract_scores.py."""
from pathlib import Path
import hashlib,importlib.util,json,re,sys,yaml
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'scripts/contract_scores.py').is_file())
spec=importlib.util.spec_from_file_location('contract_scores',ROOT/'scripts/contract_scores.py');cs=importlib.util.module_from_spec(spec);spec.loader.exec_module(cs)
RUN=B.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def symbols(p):
    text=p.read_text(encoding='utf-8')
    pat={'.py':r'^def (\w+)','.rs':r'^pub (?:fn|struct|enum|const|type) (\w+)'}.get(p.suffix,r'^(?:noncomputable )?(?:theorem|def) ([\w.ₗ]+)')
    return sorted({m[1] for m in re.finditer(pat,text,re.M)})
def records(rel,purpose,boundaries):
    p=ROOT/rel;digest=sha(p);head={'schema_id':'finite-qm.code-companion.v1','subject':rel,'source_sha256':digest,'authority_effect':'None'}
    contract={**head,'contract_urn':f'urn:finite-qm:pfp:u1-phase-completion:{digest[:20]}','symbols':symbols(p),'owned_invariants':['Only the literal definitions and the declared exact replay contract of this source are claimed.','Source bytes and kernel/native receipts are retained; labels do not admit a mathematical or physical target.'],'boundaries':boundaries,'evidence':[RUN+'/README.md']}
    score={**head,'rubric':'SCORING.md v2.0.0 section1.4','capability_level':None,'engineering_grade':None,'composite_score':None,'assessment_status':'formal_scoring_not_performed','gates':{g:{'grade':None,'status':'formal_scoring_not_performed'} for g in ('G1','G2','G3','G4','G5')},'refusal_reason':'A five-gate engineering-grade assessment was not performed; kernel, native and custody receipts support only their stated bounded scopes.','evidence':[RUN+'/README.md']}
    doc={**head,'purpose':purpose,'design':{'profile':'Exact rational arithmetic or kernel-checked Lean on the declared carrier; no floating point.','frozen_sources':'Run snapshots under verification/ are immutable custody assets.'},'boundaries':boundaries,'evidence':[RUN+'/README.md']}
    return contract,score,doc
def dump(v):return yaml.safe_dump(v,sort_keys=False,allow_unicode=True,width=100)
def write(rel,purpose,boundaries):
    contract,score,doc=records(rel,purpose,boundaries);p=ROOT/rel
    cs.write_legacy(p.with_name(p.name+'.contract.yaml'),dump(contract).encode('utf-8'))
    cs.write_legacy(p.with_name(p.name+'.score.yaml'),dump(score).encode('utf-8'))
    p.with_name(p.name+'.doc.yaml').write_text(dump(doc),encoding='utf-8')
    return cs.canonical_path(p.with_name(p.name+'.contract.yaml')).relative_to(ROOT).as_posix()
if __name__=='__main__':
    for t in json.loads((B/'tools/companion_targets.json').read_text(encoding='utf-8')):print(write(t['path'],t['purpose'],t['boundaries']))
