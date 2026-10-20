"""Source-bound staged rational/rank trial; no live-source score promotion.
AuthorityEffect: None. Keeps prototype, integration and failed evidence distinct.
"""
import json, shutil, subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from replay import ROOT, RUST, inventory, snapshot, digest, write, execute, dependency_sources, remove_owned

def recipes():
    return [
        ('ES01-denominator-domain', 'value.denom() <= &num_bigint::BigInt::zero()', 'value.denom() < &num_bigint::BigInt::zero()'),
        ('ES02-reduced-domain', '!value.numer().gcd(value.denom()).is_one()', 'false'),
        ('ES03-error-index', 'HomologicalError::InvalidRational { index }', 'HomologicalError::InvalidRational { index: 0 }'),
        ('ES04-shape-admission', 'if matrix.shape() != expected {', 'if false {'),
        ('ES05-cell-refusal', 'if count > limit {', 'if false {'),
        ('ES06-inclusive-cells', 'if count > limit {', 'if count >= limit {'),
        ('ES07-product-dimensions', 'if left.cols() != right.rows() {', 'if false {'),
        ('ES08-work-accounting', '.and_then(|n| n.checked_mul(2))', '.and_then(|n| n.checked_mul(1))'),
        ('ES09-work-refusal', 'if operations > limits.max_scalar_operations {', 'if false {'),
        ('ES10-dot-index', 'right.get_ref(inner, col)?', 'right.get_ref(0, col)?'),
        ('ES11-zero-law', 'if !dot_product(left, right, row, col)?.is_zero() {', 'if false {'),
        ('ES12-digest-denominator', 'hash_bigint(&mut hasher, value.denom());', 'hash_bigint(&mut hasher, value.numer());'),
        ('ES13-digest-shape', 'hasher.update(&(self.matrix.rows() as u64).to_le_bytes());', 'hasher.update(&(self.matrix.cols() as u64).to_le_bytes());'),
        ('ES14-token-admission', '        admit_coefficients(matrix.as_slice())?;', ''),
        ('ES15-left-domain', 'AdmittedMatrix::try_new(first)?', 'AdmittedMatrix { matrix: first }'),
        ('ES16-right-domain', 'AdmittedMatrix::try_new(second)?', 'AdmittedMatrix { matrix: second }'),
        ('ES17-zero-area', 'if left.rows() == 0 || right.cols() == 0 || left.cols() == 0 {\n            return Ok(());', 'if left.rows() == 0 || right.cols() == 0 || left.cols() == 0 {\n            return Err(violation);'),
    ]

def main():
    q=Path(__file__).parent
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-rank-trial'
    out=ROOT/'evidence/quality/l4a_six'/stamp;out.mkdir()
    work=RUST/'target/l4a-six'/stamp;snapshot(work)
    shutil.copyfile(__file__,out/'trial.py');shutil.copyfile(q/'replay.py',out/'replay.py')
    sources=inventory();write(out/'live_source_manifest.json',sources)
    overrides={'homology/exact_scalar.rs':'exact_scalar_candidate.rs',
               'homology/hashing.rs':'hashing_candidate.rs',
               'homology/rank_certificate.rs':'rank_certificate_candidate.rs',
               'local_green_global_red_lggr/tests/lggr_allocation.rs':'lggr_allocation_candidate.rs'}
    for target, candidate in overrides.items():
        shutil.copyfile(q/candidate,work/'src'/target)
        shutil.copyfile(q/candidate,out/candidate)
    pinned={str(q/name):digest(q/name)for name in overrides.values()}
    receipt={'AuthorityEffect':'None','scope':'Staged replacements in an owned source snapshot. No live-source score or package-baseline promotion.',
        'versions':{x:subprocess.check_output([x,'--version'],text=True).strip()for x in ['cargo','rustc']},
        'live_source_manifest_sha256':digest(out/'live_source_manifest.json'),
        'runner_sha256':digest(out/'trial.py'),'helper_sha256':digest(out/'replay.py'),
        'overrides':{target:dict(candidate=name,sha256=digest(q/name))for target,name in overrides.items()},
        'baselines':[],'restored_baselines':[]}
    entries=[dict(id=i,before=b,after=a,outcome='unrun')for i,b,a in recipes()]
    print(out,flush=True)
    try:
        meta=subprocess.run(['cargo','metadata','--offline','--quiet','--format-version','1'],cwd=work,capture_output=True,text=True,check=True)
        (out/'cargo_metadata.json').write_text(meta.stdout,encoding='utf8')
        dependencies=dependency_sources(json.loads(meta.stdout));write(out/'dependency_sources.json',dependencies)
        receipt['dependency_sources_sha256']=digest(out/'dependency_sources.json')
        common=['--offline','--quiet','--target-dir',str(work/'build')]
        def run(package,label,filter=None,integration=None):
            if shutil.disk_usage(ROOT).free<2*1024**3:raise RuntimeError('Less than two GiB before staged command')
            target=['--test',integration]if integration else ['--lib']if filter else []
            command=['cargo','test',*common,'-p',package,*target,*([filter]if filter else [])]
            r=execute(command,work,out/(label+'.log'));print(label,r['exit_code'],flush=True);return r
        root='tfqm_homology_linear_audit';lggr='tfqm_local_green_global_red_lggr'
        receipt['baselines']=[run(root,'root-baseline'),run(lggr,'lggr-baseline',integration='lggr_allocation')]
        if any(r['exit_code']!=0 for r in receipt['baselines']):return
        path=work/'src/homology/exact_scalar.rs';original=path.read_bytes();source=original.decode('utf8')
        for e in entries:
            try:
                if source.count(e['before'])!=1:e.update(outcome='invalid',reason='Nonunique recipe');continue
                path.write_text(source.replace(e['before'],e['after'],1),encoding='utf8');e['candidate_sha256']=digest(path)
                r=run(root,e['id'],filter='homology::exact_scalar');e['run']=r
                log=(ROOT/r['log']).read_text(encoding='utf8')
                e['outcome']='inconclusive'if r['timed_out']else 'survived'if r['exit_code']==0 else 'invalid'if 'could not compile'in log or 'error[E'in log else 'killed'if 'test result: FAILED'in log else 'inconclusive'
            finally:path.write_bytes(original);e['source_restored']=digest(path)==pinned[str(q/'exact_scalar_candidate.rs')];write(out/'mutations.json',entries)
        path=work/'src/local_green_global_red_lggr/lggr_v.rs';original=path.read_bytes();source=original.decode('utf8');e=dict(id='LG06-witness-nonzero',outcome='unrun');entries.append(e)
        try:
            assert source.count('if !dv_nonzero {')==1
            path.write_text(source.replace('if !dv_nonzero {','if false {',1),encoding='utf8');e['candidate_sha256']=digest(path)
            r=run(lggr,e['id'],integration='lggr_allocation');e['run']=r
            log=(ROOT/r['log']).read_text(encoding='utf8')
            e['outcome']='inconclusive'if r['timed_out']else 'survived'if r['exit_code']==0 else 'invalid'if 'could not compile'in log or 'error[E'in log else 'killed'if 'test result: FAILED'in log else 'inconclusive'
        finally:path.write_bytes(original);e['source_restored']=True;write(out/'mutations.json',entries)
        receipt['restored_baselines']=[run(root,'root-restored'),run(lggr,'lggr-restored',integration='lggr_allocation')]
        receipt['snapshot_dependencies_unchanged']=all(Path(p).is_file()and digest(Path(p))==h for p,h in dependencies.items())
        shutil.copyfile(work/'Cargo.lock',out/'Cargo.lock')
    finally:
        counts=Counter(e['outcome']for e in entries)
        for k in ['killed','survived','demonstrably_equivalent','invalid','inconclusive','unrun']:counts.setdefault(k,0)
        den=sum(counts[k]for k in ['killed','survived','inconclusive','unrun']);receipt['accounting']={**counts,'conservative_ratio':counts['killed']/den if den else None}
        write(out/'mutations.json',entries);receipt['mutations_sha256']=digest(out/'mutations.json')
        receipt['live_sources_unchanged']=sources==inventory();receipt['candidates_unchanged']=all(digest(Path(p))==h for p,h in pinned.items())
        remove_owned(work/'build',work);receipt['owned_build_removed']=True;write(out/'receipt.json',receipt)
if __name__=='__main__':main()
