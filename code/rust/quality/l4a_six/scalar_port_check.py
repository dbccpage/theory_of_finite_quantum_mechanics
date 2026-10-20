"""Compiler-guided staged scalar migration; never an integrated-source grade.
AuthorityEffect: None. One owned cache is retained between checks, with headroom.
"""
import argparse,json,shutil,subprocess,tomllib
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
from datetime import datetime,timezone
from replay import ROOT,RUST,snapshot,inventory,digest,write,execute,dependency_sources,remove_owned

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--tests',action='store_true');parser.add_argument('--run',action='store_true');parser.add_argument('--clean',action='store_true');args=parser.parse_args()
    q=Path(__file__).parent;work=RUST/'target/l4a-six/scalar-port-work'
    if not work.exists():snapshot(work)
    manifest=work/'Cargo.toml'
    text=manifest.read_text(encoding='utf8')
    for name in ['omega_number_theory','omega_lie_theory','omega_general_relativity']:
        if '\n'+name+' = 'not in text:
            dependency=tomllib.loads((RUST/'Cargo.toml').read_text(encoding='utf8'))['dependencies'][name]
            encoded='{ '+', '.join(k+' = '+json.dumps(v)for k,v in dependency.items())+' }'
            text=text.replace('[dependencies]\n','[dependencies]\n'+name+' = '+encoded+'\n',1)
    manifest.write_bytes(text.encode())
    stage=q/'scalar_port';staged={str(p):digest(p)for p in sorted(stage.rglob('*.rs'))}
    for p in stage.rglob('*.rs'):
        relative=p.relative_to(stage)
        destination=(work/relative if relative.parts[0]=='tests' else work/'src'/relative)
        destination.parent.mkdir(parents=True,exist_ok=True)
        _copy_record_file(p,destination)
    # Exercise the exact transport adapter at its smallest module boundary;
    # complete QM consumer composition remains a separate, sealed replay.
    bridge=(work/'src/qm/bridge.rs').as_posix()
    (work/'src/lib.rs').write_bytes(('pub mod linear_algebra;\npub mod homology;\npub mod qm { #[path='+json.dumps(bridge)+'] pub mod bridge; }\n').encode())
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-scalar-port-check';out=ROOT/'evidence/quality/l4a_six'/stamp;out.mkdir()
    _copy_record_file(__file__,out/'check.py');_copy_record_file(q/'replay.py',out/'replay.py');write(out/'staged_sources.json',staged)
    for p in stage.rglob('*.rs'):
        saved=out/'staged'/p.relative_to(stage);saved.parent.mkdir(parents=True,exist_ok=True);_copy_record_file(p,saved)
    live=inventory();write(out/'live_source_manifest.json',live)
    r={'AuthorityEffect':'None','scope':'Staged library migration only. Compiler failure is retained as unfinished work, never a current-source regression or passing baseline.','runner_sha256':digest(out/'check.py'),'helper_sha256':digest(out/'replay.py'),'staged_manifest_sha256':digest(out/'staged_sources.json'),'arguments':vars(args),'versions':{x:subprocess.check_output([x,'--version'],text=True).strip()for x in ['rustc','cargo']}}
    print(out,flush=True)
    try:
        meta=subprocess.run(['cargo','metadata','--offline','--quiet','--format-version','1'],cwd=work,text=True,capture_output=True,check=True)
        (out/'cargo_metadata.json').write_text(meta.stdout,encoding='utf8');dependencies=dependency_sources(json.loads(meta.stdout));write(out/'dependency_sources.json',dependencies);r['dependency_sources_sha256']=digest(out/'dependency_sources.json')
        if shutil.disk_usage(ROOT).free<2*1024**3:raise RuntimeError('Less than two GiB before staged compiler invocation')
        action='test'if args.run else 'check'
        command=['cargo',action,'--offline','--quiet','--target-dir',str(work/'build'),'-p','tfqm_homology_linear_audit']
        if not args.run:command+=['--message-format','short','--tests'if args.tests else '--lib']
        r['run']=execute(command,work,out/'compiler.log')
        lines=(out/'compiler.log').read_text(encoding='utf8').splitlines();errors=[line for line in lines if 'error'in line]
        print('compiler exit',r['run']['exit_code'],'error lines',len(errors),flush=True)
        print('\n'.join(errors[:45]),flush=True)
        r['dependencies_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in dependencies.items())
        _copy_record_file(work/'Cargo.lock',out/'Cargo.lock');_copy_record_file(work/'Cargo.toml',out/'Cargo.toml')
    finally:
        r['live_sources_unchanged']=live==inventory();r['staged_sources_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in staged.items())
        if args.clean:remove_owned(work/'build',work)
        r['owned_cache_retained']=not args.clean;write(out/'receipt.json',r)
if __name__=='__main__':main()
