"""Executable source-grounded witness for the provider's native i64 protocol.
AuthorityEffect: None. Exact item excerpts, not a whole-package build.
"""
import json,re,shutil,subprocess,tomllib
from datetime import datetime,timezone
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
from replay import ROOT,RUST,digest,write,inventory,execute,remove_owned

def item(source,header):
    if source.count(header)!=1:raise RuntimeError('Item header is not unique: '+header)
    start=source.index(header);opening=source.index('{',start);depth=0
    for position in range(opening,len(source)):
        if source[position]=='{':depth+=1
        elif source[position]=='}':
            depth-=1
            if depth==0:return source[start:position+1]
    raise RuntimeError('Unbalanced selected source item')

def main():
    package=tomllib.loads((RUST/'Cargo.toml').read_text(encoding='utf-8'))['dependencies']['linear_algebra']
    provider=Path(package['path']).resolve()
    scalar=RUST/'src/linear_algebra/scalars.rs';module=RUST/'src/linear_algebra/mod.rs'
    exported=re.search(r'pub use ::linear_algebra::scalars::\{([^}]+)\};',scalar.read_text())
    if not exported or not {'Semiring','ExactRing'}<=set(x.strip()for x in exported[1].split(',')):
        raise RuntimeError('Public alias surface changed: reassess the boundary; do not reuse this witness')
    provider_manifest=tomllib.loads((provider/'Cargo.toml').read_text())
    provider_lib=provider/provider_manifest.get('lib',{}).get('path','src/lib.rs')
    if 'pub mod scalars;'not in provider_lib.read_text():raise RuntimeError('Provider module binding changed')
    path=provider/'src/scalars.rs';source=path.read_bytes().decode('utf-8')
    headers=['pub trait Semiring:','pub trait Ring:','pub trait ExactRing:',
             'impl Semiring for i64 {','impl Ring for i64 {','impl ExactRing for i64 {}']
    excerpts=[item(source,h)for h in headers]
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-native-scalar-control'
    out=ROOT/'evidence/quality/l4a_six'/stamp;out.mkdir()
    work=RUST/'target/l4a-six'/stamp;work.mkdir(parents=True);build=work/'build';build.mkdir()
    code='use std::fmt;\n'+'\n\n'.join(excerpts)+r'''
fn exact_ring<T:ExactRing>(){}
fn main(){
    exact_ring::<i64>();
    let observed=std::panic::catch_unwind(||Semiring::add(&i64::MAX,&1)).is_err();
    assert!(observed,"the source-grounded overflow witness did not reproduce");
    println!("DEFECT_CONFIRMED:provider_marks_overflowing_i64_as_exact");
}
'''
    (out/'native_items.rs').write_bytes(code.encode('utf-8'));_copy_record_file(__file__,out/'probe.py');_copy_record_file(Path(__file__).with_name('replay.py'),out/'replay.py')
    sources=inventory();write(out/'source_manifest.json',sources)
    dependencies={str(p):digest(p)for p in [scalar,module,RUST/'Cargo.toml',provider/'Cargo.toml',provider_lib,path]}
    write(out/'dependency_sources.json',dependencies)
    write(out/'extraction.json',{'AuthorityEffect':'None','headers':headers,'provider_source_sha256':digest(path),'excerpt_items_sha256':[__import__('hashlib').sha256(x.encode()).hexdigest()for x in excerpts],'public_alias_binding':exported[0],'scope':'Unconditional primitive-only items are copied byte-for-byte. Their operator is the built-in i64 addition under explicit overflow checks. This does not compile the whole provider or root package.'})
    receipt={'AuthorityEffect':'None','evaluation_timestamp':datetime.now(timezone.utc).isoformat(),'claim':'Source-grounded executable counterexample at an unchanged public re-export. No whole-package or whole-workspace build is claimed.','versions':{x:subprocess.check_output([x,'--version'],text=True).strip()for x in ['rustc','cargo']},'source_manifest_sha256':digest(out/'source_manifest.json'),'dependency_sources_sha256':digest(out/'dependency_sources.json'),'runner_sha256':digest(out/'probe.py'),'helper_sha256':digest(out/'replay.py'),'excerpt_sha256':digest(out/'native_items.rs'),'extraction_sha256':digest(out/'extraction.json')}
    print(out,flush=True)
    try:
        compilation=execute(['rustc','--edition','2021','-C','overflow-checks=on',str(out/'native_items.rs'),'-o',str(build/'witness.exe')],work,out/'compile.log',timeout=90)
        receipt['compilation']=compilation
        if compilation['exit_code']!=0:return
        run=execute([str(build/'witness.exe')],work,out/'witness.log',timeout=90);receipt['run']=run
        reproduced=run['exit_code']==0 and 'DEFECT_CONFIRMED:provider_marks_overflowing_i64_as_exact'in(out/'witness.log').read_text()
        findings=[{'id':'provider_marks_overflowing_i64_as_exact','source':'code/rust/src/linear_algebra/scalars.rs','gate':'G3','affected_gates':['G2','G3'],'grade':'E','reproduced':reproduced,'observation_kind':'source-grounded-native-overflow','witness':'The public Semiring/ExactRing re-export still binds to the pinned provider i64 implementation. Exact unchanged trait/impl source items, compiled with the pinned Rust compiler and overflow checks enabled, admit i64 as ExactRing and panic on MAX+1. Alias, Cargo-path and provider-module bindings are checked. This is an executable source-grounded counterexample, not a fresh direct invocation of the whole root package.'}]
        write(out/'findings.json',findings);receipt['findings_sha256']=digest(out/'findings.json');print('native exact-ring overflow reproduced',reproduced,flush=True)
    finally:
        receipt['sources_unchanged']=sources==inventory();receipt['dependency_sources_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in dependencies.items())
        remove_owned(build,work);receipt['owned_build_removed']=True;write(out/'receipt.json',receipt)
if __name__=='__main__':main()
