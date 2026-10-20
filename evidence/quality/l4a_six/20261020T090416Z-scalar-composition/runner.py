"""Check root module composition in a separate manifest, with staged overrides.

AuthorityEffect: None. Does not modify or claim execution of the actual root
Cargo package. Original root modules remain pinned and read in place; the audit
manifest has absolute path dependencies and excludes root dev dependencies.
"""
import argparse,json,shutil,subprocess,tomllib
from pathlib import Path
from datetime import datetime,timezone
from replay import ROOT,RUST,digest,write,execute,dependency_sources,remove_owned

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--staged',action='store_true');parser.add_argument('--clean',action='store_true');args=parser.parse_args()
    quality=Path(__file__).parent;stage=quality/'scalar_port';work=RUST/'target/l4a-six/scalar-composition-work';work.mkdir(exist_ok=True,parents=True)
    dependencies=tomllib.loads((RUST/'Cargo.toml').read_text(encoding='utf8'))['dependencies']
    lines=['[workspace]','members=["."]','resolver="2"','[package]','name="tfqm_scalar_composition_audit"','version="0.0.0"','edition="2021"','[lib]','name="theory_of_finite_qm"','path="lib.rs"','[dependencies]']
    for name,value in dependencies.items():
        if isinstance(value,dict):
            value=dict(value)
            if 'path'in value:value['path']=str((RUST/value['path']).resolve()).replace('\\','/')
            encoded='{ '+', '.join(k+' = '+json.dumps(v)for k,v in value.items())+' }'
        else:encoded=json.dumps(value)
        lines.append(name+' = '+encoded)
    lines+=['[profile.dev]','debug=0','incremental=false']
    (work/'Cargo.toml').write_bytes(('\n'.join(lines)+'\n').encode())
    # Preserve the repository's selected versions rather than resolving newest
    # compatible versions that may not be in the offline cache.
    shutil.copyfile(RUST/'Cargo.lock',work/'Cargo.lock')
    source=(RUST/'src/lib.rs').read_text(encoding='utf8')
    for name in ['linear_algebra','homology','qm','dag_witnesses']:
        folder=stage if args.staged and name in ('linear_algebra','homology')else RUST/'src'
        # Staging has only changed homology files. Use a captured complete overlay
        # so missing module files never silently fall back to live source bytes.
        if folder==stage:
            overlay=work/'overlay'/name;overlay.mkdir(parents=True,exist_ok=True)
            for p in (RUST/'src'/name).rglob('*.rs'):
                target=overlay/p.relative_to(RUST/'src'/name);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
            for p in (stage/name).rglob('*.rs'):
                target=overlay/p.relative_to(stage/name);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
            path=overlay/'mod.rs'
        else:path=folder/name/'mod.rs'
        if not path.exists():path=folder/(name+'.rs')
        assert path.is_file(),path
        token='pub mod '+name+';';assert source.count(token)==1
        source=source.replace(token,'#[path='+json.dumps(path.as_posix())+']\n'+token,1)
    (work/'lib.rs').write_bytes(source.encode())
    out=ROOT/'evidence/quality/l4a_six'/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-scalar-composition');out.mkdir()
    for name in ['Cargo.toml','lib.rs','Cargo.lock']:shutil.copyfile(work/name,out/name)
    shutil.copyfile(__file__,out/'runner.py');shutil.copyfile(quality/'replay.py',out/'replay.py')
    current={str(p):digest(p)for p in (RUST/'src').rglob('*.rs')};current[str(RUST/'Cargo.toml')]=digest(RUST/'Cargo.toml')
    staged={str(p):digest(p)for p in stage.rglob('*.rs')}if args.staged else {}
    write(out/'live_inputs.json',current);write(out/'staged_inputs.json',staged)
    r=dict(AuthorityEffect='None',claim=__doc__,arguments=vars(args),runner_sha256=digest(out/'runner.py'),helper_sha256=digest(out/'replay.py'),live_inputs_sha256=digest(out/'live_inputs.json'),staged_inputs_sha256=digest(out/'staged_inputs.json'))
    print(out,flush=True)
    try:
        verbose=subprocess.check_output(['rustc','-vV'],text=True)
        host=next(line.removeprefix('host: ')for line in verbose.splitlines()if line.startswith('host: '));r['host']=host
        meta=subprocess.run(['cargo','metadata','--offline','--quiet','--format-version','1','--filter-platform',host],cwd=work,capture_output=True,text=True)
        (out/'metadata.json').write_bytes(meta.stdout.encode());(out/'metadata_stderr.log').write_bytes(meta.stderr.encode());r['metadata_exit_code']=meta.returncode
        if meta.returncode!=0:return
        resolved=dependency_sources(json.loads(meta.stdout));write(out/'dependency_sources.json',resolved);r['dependency_sources_sha256']=digest(out/'dependency_sources.json')
        if shutil.disk_usage(ROOT).free<3*1024**3:raise RuntimeError('Three GiB free required before root composition check')
        r['run']=execute(['cargo','check','--offline','--quiet','--target-dir',str(work/'build'),'--lib','--message-format','short'],work,out/'compiler.log')
        errors=[line for line in (out/'compiler.log').read_text(encoding='utf8').splitlines()if'error'in line];print('compiler exit',r['run']['exit_code'],'error lines',len(errors),flush=True);print('\n'.join(errors[:35]),flush=True)
        r['dependencies_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in resolved.items())
        shutil.copyfile(work/'Cargo.lock',out/'Cargo.lock')
    finally:
        r['live_inputs_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in current.items());r['staged_inputs_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in staged.items())
        if args.clean:remove_owned(work/'build',work)
        r['owned_cache_retained']=not args.clean;write(out/'receipt.json',r)

if __name__=='__main__':main()
