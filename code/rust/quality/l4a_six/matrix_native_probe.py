"""Direct provider witness behind the root matrix re-export. AuthorityEffect: None."""
import json,shutil,subprocess,tomllib
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
from datetime import datetime,timezone
from replay import ROOT,RUST,inventory,digest,write,execute,dependency_sources,remove_owned

def main():
    alias=RUST/'src/linear_algebra/basic_matrix.rs'
    if alias.read_text(encoding='utf8').strip()!='pub use ::linear_algebra::backend::basic_matrix::*;':
        raise RuntimeError('Matrix public boundary changed: reassess this witness')
    dependency=tomllib.loads((RUST/'Cargo.toml').read_text(encoding='utf8'))['dependencies']['linear_algebra']
    encoded='{ '+', '.join(f'{key} = {json.dumps(value)}'for key,value in dependency.items())+' }'
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-native-matrix-control'
    out=ROOT/'evidence/quality/l4a_six'/stamp;out.mkdir();work=RUST/'target/l4a-six'/stamp;work.mkdir()
    manifest='[workspace]\n[package]\nname="tfqm_native_matrix_control"\nversion="0.0.0"\nedition="2021"\n[dependencies]\nlinear_algebra = '+encoded+'\n[[bin]]\nname="witness"\npath="main.rs"\n[profile.dev]\ndebug=0\noverflow-checks=true\n'
    (work/'Cargo.toml').write_bytes(manifest.encode('utf8'))
    code='''use linear_algebra::backend::basic_matrix::BasicMatrix;
fn main(){
    let left=BasicMatrix::from_row_major(1,1,vec![i64::MAX]).unwrap();
    let right=BasicMatrix::from_row_major(1,1,vec![2i64]).unwrap();
    let observed=std::panic::catch_unwind(||left.mul(&right)).is_err();
    assert!(observed,"native matrix overflow did not reproduce");
    println!("DEFECT_CONFIRMED:provider_native_matrix_multiply_overflow");
}
'''
    (work/'main.rs').write_bytes(code.encode('utf8'));_copy_record_file(work/'main.rs',out/'main.rs');_copy_record_file(__file__,out/'probe.py');_copy_record_file(Path(__file__).with_name('replay.py'),out/'replay.py')
    sources=inventory();write(out/'source_manifest.json',sources)
    receipt={'AuthorityEffect':'None','evaluation_timestamp':datetime.now(timezone.utc).isoformat(),'claim':'Direct invocation of the exact provider type/method behind an unchanged root public re-export. This does not build the whole root package.','versions':{x:subprocess.check_output([x,'--version'],text=True).strip()for x in ['cargo','rustc']},'source_manifest_sha256':digest(out/'source_manifest.json'),'runner_sha256':digest(out/'probe.py'),'helper_sha256':digest(out/'replay.py')}
    print(out,flush=True)
    try:
        metadata=subprocess.run(['cargo','metadata','--offline','--quiet','--format-version','1'],cwd=work,text=True,capture_output=True,check=True);(out/'cargo_metadata.json').write_text(metadata.stdout,encoding='utf8');dependencies=dependency_sources(json.loads(metadata.stdout));dependencies.update({str(p):digest(p)for p in [alias,RUST/'Cargo.toml']});write(out/'dependency_sources.json',dependencies);receipt['dependency_sources_sha256']=digest(out/'dependency_sources.json')
        if shutil.disk_usage(ROOT).free<2*1024**3:raise RuntimeError('Less than two GiB before direct provider build')
        run=execute(['cargo','run','--offline','--quiet','--target-dir',str(work/'build'),'--bin','witness'],work,out/'witness.log');receipt['run']=run
        reproduced=run['exit_code']==0 and 'DEFECT_CONFIRMED:provider_native_matrix_multiply_overflow'in(out/'witness.log').read_text(encoding='utf8')
        write(out/'findings.json',[{'id':'provider_native_matrix_multiply_overflow','source':'code/rust/src/linear_algebra/basic_matrix.rs','gate':'G3','affected_gates':['G2','G3'],'grade':'E','reproduced':reproduced,'witness':'Root BasicMatrix re-exports this exact pinned provider type. Its public legacy mul on valid 1x1 i64 inputs [MAX] and [2] panics under explicit overflow checks instead of returning typed refusal. Cargo-path/re-export bindings and actual provider execution are pinned; no whole-root build is claimed.'}]);receipt['findings_sha256']=digest(out/'findings.json')
        receipt['dependency_sources_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in dependencies.items());_copy_record_file(work/'Cargo.toml',out/'Cargo.toml');_copy_record_file(work/'Cargo.lock',out/'Cargo.lock');print('native matrix overflow reproduced',reproduced,flush=True)
    finally:
        receipt['sources_unchanged']=sources==inventory();remove_owned(work/'build',work);receipt['owned_build_removed']=True;write(out/'receipt.json',receipt)
if __name__=='__main__':main()
