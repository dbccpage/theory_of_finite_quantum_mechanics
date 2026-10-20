"""Activate the reviewed staged migration after successful bounded challenges.

AuthorityEffect: None. Does not award engineering gates, commit, push or merge.
Checks target origins before writes and archives every replaced source/sidecar.
"""
import argparse,json,shutil
from pathlib import Path
from datetime import datetime,timezone
from replay import ROOT,RUST,digest,write,inventory,subjects

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--faults',type=Path,required=True);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    q=Path(__file__).parent;stage=q/'scalar_port';fault_path=args.faults.resolve();fault=json.loads(fault_path.read_text(encoding='utf8'))
    assert fault['accounting']['killed']==46 and fault['accounting']['conservative_ratio']==1
    assert all(fault[key]for key in ['staged_sources_unchanged','live_sources_unchanged','dependencies_unchanged','owned_build_removed'])
    restored=fault['restored_baseline'];assert restored['exit_code']==0 and not restored['timed_out']
    staged=json.loads((fault_path.parent/'staged_sources.json').read_text(encoding='utf8'))
    assert {str(p.resolve()):digest(p)for p in stage.rglob('*.rs')}=={str(Path(p).resolve()):h for p,h in staged.items()}
    baseline=json.loads((ROOT/fault['baseline']).read_text(encoding='utf8'));assert baseline['run']['exit_code']==0 and not baseline['run']['timed_out']
    assert digest(ROOT/restored['log'])==restored['log_sha256']
    epoch=ROOT/'evidence/quality/l4a_six/20261020T074554Z';old=json.loads((epoch/'source_manifest.json').read_text(encoding='utf8'))
    origins={}
    for name in ['homology_origins.json','qm_origins.json']:
        origins.update({str((ROOT/Path(p)).resolve()):h for p,h in json.loads((stage/name).read_text(encoding='utf8')).items()})
    updates=[]
    for candidate in sorted(stage.rglob('*.rs')):
        relative=candidate.relative_to(stage)
        if relative.parts[0]=='tests':continue
        target=RUST/'src'/relative
        if target.is_file()and digest(target)==digest(candidate):continue
        expected=old.get(target.relative_to(ROOT).as_posix(),origins.get(str(target.resolve())))
        if target.exists():assert expected is not None and digest(target)==expected,'Unrelated target drift: '+str(target)
        else:assert expected is None,'An original target disappeared: '+str(target)
        updates.append((candidate,target,expected))
    fixture=q/'scalar_boundary.rs';assert not fixture.exists(),'Do not replace another allocation fixture'
    print('Validated source replacements:',len(updates),'new allocation fixture: 1',flush=True)
    if args.check:return
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-scalar-activation';out=ROOT/'evidence/quality/l4a_six'/stamp;out.mkdir()
    shutil.copyfile(__file__,out/'activate.py');shutil.copyfile(q/'replay.py',out/'replay.py')
    for candidate,target,expected in updates:
        sealed=out/'candidate'/target.relative_to(RUST);sealed.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(candidate,sealed)
        if expected:
            saved=out/'before'/target.relative_to(RUST);saved.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(target,saved)
    for subject in subjects():
        for suffix in ['.scoring.yaml','.contract.yaml']:
            path=Path(str(subject)+suffix)
            if path.exists():
                saved=out/'previous_assessment'/path.relative_to(ROOT);saved.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,saved)
    for path in [q/'specs.json',q/'records.py',q/'replay.py',q/'mutations.py',q/'summarize.py',q/'README.md',*epoch.glob('*.json'),epoch/'REVIEW.md']:
        if path.is_file():
            saved=out/'previous_assessment'/path.relative_to(ROOT);saved.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,saved)
    changed=[]
    try:
        for candidate,target,expected in updates:
            assert (digest(target)if target.exists()else None)==expected,'Target changed during activation: '+str(target)
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(candidate.read_bytes());changed.append((target,expected))
        fixture.write_bytes((stage/'tests/scalar_boundary.rs').read_bytes())
    except BaseException:
        for target,expected in reversed(changed):
            if expected:target.write_bytes((out/'before'/target.relative_to(RUST)).read_bytes())
            else:target.unlink()
        if fixture.exists():fixture.unlink()
        raise
    event={'AuthorityEffect':'None','runner_sha256':digest(out/'activate.py'),'fault_receipt':str(fault_path.relative_to(ROOT)),'fault_receipt_sha256':digest(fault_path),'replacements':[{'path':str(t.relative_to(ROOT)),'before_sha256':h,'after_sha256':digest(t)}for _,t,h in updates],'allocation_fixture':{'path':str(fixture.relative_to(ROOT)),'sha256':digest(fixture)},'scope':'Code activation only. Previous sidecars are archived and require fresh integrated assessment; no completed goal or engineering grade is implied.'}
    write(out/'activation.json',event);write(out/'activated_inventory.json',inventory());print(out,flush=True)

if __name__=='__main__':main()
