"""Bind the unchanged mathematical integration to the advanced delivery base."""
import hashlib,importlib.util,json,re
from pathlib import Path
B=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
prior=B/'review/final_integration_after_source_review/result.json';result=json.loads(prior.read_bytes())
for path in (B/'review/final_integration_after_source_review').glob('*_receipt.json'):
 r=json.loads(path.read_bytes())
 if r['exit_code'] or not r['sources_unchanged']:raise ValueError('Nonpassing mathematical integration')
 for pin in r['source_pins']:
  if s.sha(Path(pin['path']))!=pin['sha256']:raise ValueError('Prior mathematical source drift '+pin['path'])
for name in ('atlas','pytest'):
 path=B/'review/atlas_after_fix'/(name+'_receipt.json');r=json.loads(path.read_bytes())
 if r['exit_code'] or not r['sources_unchanged']:raise ValueError('Atlas check failed')
 for pin in r['source_pins']:
  if s.sha(Path(pin['path']))!=pin['sha256']:raise ValueError('Atlas source drift')
text=(B/'review/atlas_after_fix/pytest.stdout.log').read_text();m=re.search(r'(\d+) passed',text)
if not m:raise ValueError('No actual pytest count')
added=int(m.group(1));result['prior_targeted_unique_Python_tests']=result['targeted_unique_Python_tests'];result['additional_atlas_pytest_tests']=added;result['targeted_unique_Python_tests']+=added
result['prior_mathematical_integration']={'path':prior.relative_to(s.ROOT).as_posix(),'sha256':s.sha(prior),'reuse_basis':'Every original receipt source digest remains unchanged after a disjoint upstream fast-forward. Extra source edits are limited to the atlas hook installer/tests, freshly checked separately.'}
result['delivery_base']=json.loads((B/'delivery_base.json').read_bytes())['delivery_base'];result['atlas_check_receipts']=[(B/'review/atlas_after_fix'/(n+'_receipt.json')).relative_to(s.ROOT).as_posix() for n in ('atlas','pytest')]
result['scope']+=' Required upstream atlas LOC/symbol/parity checks and five pytest cases passed under Python3.14; PFP PyYAML checks use Python3.9. No general engineering-grade assessment is claimed.'
companions=json.loads((B/'review/companion_records.json').read_bytes())
for row in companions['records']:
 if s.sha(s.ROOT/row['subject'])!=row['sha256']:raise ValueError('Companion source drift')
 for name in row['companions']:
  import yaml
  record=yaml.safe_load((s.ROOT/name).read_bytes())
  if record['subject']!=row['subject'] or record['source_sha256']!=row['sha256']:raise ValueError('Companion binding drift')
result['live_code_companion_subjects']=companions['subjects'];result['companion_records']=companions['companions'];result['engineering_grades']='unassessed; no completed score tokens'
s.save(B/'review/final_delivery_integration/result.json',result);print(json.dumps(result),flush=True)
