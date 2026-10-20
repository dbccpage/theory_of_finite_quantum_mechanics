"""Staged scalar/matrix semantic fault replay. AuthorityEffect: None.

Uses the completed staged baseline's owned cache, never a live-source grade.
The complete baseline, staged bytes, recipes and restored package are retained.
"""
import argparse, json, shutil
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from replay import ROOT, RUST, digest, write, execute, inventory, remove_owned


def block(source, prefix):
    start = source.index(prefix)
    opening = source.index('{', start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def recipes(stage):
    result = []
    def add(identifier, filename, prefix, before, after, target='lib', selected=None):
        text = (stage / 'linear_algebra' / filename).read_bytes().decode('utf8')
        original = block(text, prefix)
        assert original.count(before) == 1, identifier
        result.append(dict(id=identifier, source='linear_algebra/'+filename,
            before=original, after=original.replace(before, after, 1), outcome='unrun',
            target=target, filter=selected or 'linear_algebra::scalars'))
    for code,method,operation in [('01','add','Add'),('02','mul','Multiply'),('03','sub','Subtract'),('04','neg','Negate')]:
        trait='Ring' if method in ('sub','neg') else 'Semiring'
        argument='' if method=='neg' else '*rhs'
        before=f'self.checked_{method}({argument}).ok_or(ScalarError::OutOfRange {{\n            operation: Operation::{operation},\n        }})'
        after=f'Ok(self.wrapping_{method}({argument}))'
        add('CP'+code+'-native-range','scalars.rs',f'impl {trait} for i64 {{',before,after)
    add('CP05-zero-denominator','scalars.rs','pub fn validate_rational(', 'if num_traits::Zero::is_zero(value.denom()) {','if false {')
    add('CP06-negative-denominator','scalars.rs','pub fn validate_rational(', 'if value.denom() < &BigInt::from(0) {','if false {')
    add('CP07-reduced-domain','scalars.rs','pub fn validate_rational(', 'if !value.numer().gcd(value.denom()).is_one() {','if false {')
    add('CP08-left-domain','scalars.rs','fn validate_pair<','left.validate()?;','')
    add('CP09-right-domain','scalars.rs','fn validate_pair<','right.validate()','Ok(())')
    add('CP10-zero-query','scalars.rs','impl Semiring for BigRational {','self.validate()?;','')
    add('CP11-zero-inverse','scalars.rs','impl Field for BigRational {','if Zero::is_zero(self) {','if false {')
    add('CP12-numerator-range','scalars.rs','fn narrow(','.numer()\n        .to_i64()', '.numer()\n        .to_i64().or(Some(0))')
    add('CP13-denominator-range','scalars.rs','fn narrow(','.denom()\n        .to_i64()', '.denom()\n        .to_i64().or(Some(1))')
    add('CP14-gaussian-product','scalars.rs','impl Semiring for GaussianRational {','real: &self.real * &rhs.real - &self.imag * &rhs.imag,','real: &self.real * &rhs.real + &self.imag * &rhs.imag,')
    add('CP15-gaussian-zero-inverse','scalars.rs','impl Field for GaussianRational {','if Zero::is_zero(&norm) {','if false {')
    add('CP16-order-domain','ordered.rs','impl OrderedExactField for BigRational {','crate::linear_algebra::scalars::Semiring::validate(self)?;','',selected='linear_algebra::ordered::scalar_query_admission')
    add('CP17-fixed-field','ordered.rs','impl HermitianOrdered for crate::linear_algebra::scalars::GaussianRational {','if crate::linear_algebra::scalars::Semiring::try_is_zero(self.imag())? {','if true {',selected='linear_algebra::ordered::scalar_query_admission')
    mul='    pub fn checked_mul_with_limits('
    vec='    pub fn checked_mul_vec_with_limits('
    basic=lambda code,prefix,before,after,target='lib':add(code,'basic_matrix.rs',prefix,before,after,target, 'linear_algebra::basic_matrix')
    basic('MB01-left-admission',mul,'admit(self.as_slice())?;','')
    basic('MB02-right-admission',mul,'admit(rhs.as_slice())?;','')
    basic('MB03-output-order',mul,'admit(self.as_slice())?;\n        admit(rhs.as_slice())?;\n        let mut out = super::reserve(count)?;','let mut out = super::reserve(count)?;\n        admit(self.as_slice())?;\n        admit(rhs.as_slice())?;',target='allocation')
    basic('MB04-work-accounting','fn preflight(','super::times(2, elements)?','super::times(1, elements)?')
    basic('MB05-work-admission',mul,'preflight(self.rows(), rhs.cols(), self.cols(), limits)?','preflight(self.rows(), rhs.cols(), self.cols(), OperationLimits::UNLIMITED)?',target='allocation')
    basic('MB06-product-coordinate',mul,'k * rhs.cols() + c','c * rhs.cols() + k')
    basic('MB07-accumulation',mul,'sum = sum.try_add(&product).map_err(scalar)?;','sum = product;')
    basic('MB08-vector-domain',vec,'admit(rhs)?;','')
    basic('MB09-vector-output-order',vec,'admit(self.as_slice())?;\n        admit(rhs)?;\n        let mut out = super::reserve(count)?;','let mut out = super::reserve(count)?;\n        admit(self.as_slice())?;\n        admit(rhs)?;',target='allocation')
    text=(stage/'linear_algebra/basic_matrix.rs').read_bytes().decode('utf8')
    before='pub struct BasicMatrix<T>(storage::BasicMatrix<T>);'
    assert text.count(before)==1
    result.append(dict(id='MB10-provider-escape',source='linear_algebra/basic_matrix.rs',before=before,after='pub struct BasicMatrix<T>(pub storage::BasicMatrix<T>);',outcome='unrun',target='doc',filter=''))
    assert len({e['id']for e in result})==len(result)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path,required=True);parser.add_argument('--preflight-only',action='store_true');args=parser.parse_args()
    stage=Path(__file__).parent/'scalar_port';entries=recipes(stage)
    if args.preflight_only:
        print('Unique staged recipes:',len(entries));return
    baseline_path=args.baseline.resolve();baseline=json.loads(baseline_path.read_text(encoding='utf8'))
    staged=json.loads((baseline_path.parent/'staged_sources.json').read_text(encoding='utf8'))
    assert baseline['run']['exit_code']==0 and not baseline['run']['timed_out']
    assert baseline['live_sources_unchanged'] and baseline['staged_sources_unchanged'] and baseline['dependencies_unchanged']
    assert all(digest(Path(p))==h for p,h in staged.items())
    assert digest(ROOT/baseline['run']['log'])==baseline['run']['log_sha256']
    work=Path(baseline['run']['cwd']);assert work.resolve()==(RUST/'target/l4a-six/scalar-port-work').resolve()
    out=ROOT/'evidence/quality/l4a_six'/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-scalar-port-faults');out.mkdir()
    shutil.copyfile(__file__,out/'runner.py');shutil.copyfile(Path(__file__).parent/'replay.py',out/'replay.py')
    shutil.copyfile(baseline_path,out/'baseline_receipt.json');shutil.copyfile(baseline_path.parent/'staged_sources.json',out/'staged_sources.json')
    shutil.copyfile(baseline_path.parent/'dependency_sources.json',out/'dependency_sources.json')
    dependencies=json.loads((out/'dependency_sources.json').read_text(encoding='utf8'))
    assert all(digest(Path(p))==h for p,h in dependencies.items())
    for p in stage.rglob('*.rs'):
        saved=out/'staged'/p.relative_to(stage);saved.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,saved)
    live=inventory();write(out/'live_source_manifest.json',live)
    receipt=dict(AuthorityEffect='None',scope='Staged scalar/matrix boundaries only; no integrated-source grading.',baseline=str(baseline_path.relative_to(ROOT)),baseline_sha256=digest(baseline_path),runner_sha256=digest(out/'runner.py'),helper_sha256=digest(out/'replay.py'))
    common=['cargo','test','--offline','--quiet','--target-dir',str(work/'build'),'-p','tfqm_homology_linear_audit']
    print(out,flush=True)
    try:
        for entry in entries:
            path=work/'src'/entry['source'];original=path.read_bytes();source=original.decode('utf8')
            assert digest(path)==digest(stage/entry['source'])
            try:
                assert source.count(entry['before'])==1,entry['id']
                path.write_bytes(source.replace(entry['before'],entry['after'],1).encode('utf8'));entry['candidate_sha256']=digest(path)
                target=['--doc']if entry['target']=='doc'else ['--test','scalar_boundary']if entry['target']=='allocation'else ['--lib',entry['filter']]
                if shutil.disk_usage(ROOT).free<2*1024**3:raise RuntimeError('Two GiB headroom required before staged fault execution')
                run=execute(common+target,work,out/(entry['id']+'.log'));entry['run']=run;log=(ROOT/run['log']).read_text(encoding='utf8')
                entry['outcome']='inconclusive'if run['timed_out']else 'survived'if run['exit_code']==0 else 'invalid'if 'could not compile'in log or 'error[E'in log else 'killed'if 'test result: FAILED'in log else 'inconclusive'
                print(entry['id'],entry['outcome'],flush=True)
            finally:
                path.write_bytes(original);entry['source_restored']=digest(path)==digest(stage/entry['source']);write(out/'mutations.json',entries)
        receipt['restored_baseline']=execute(common,work,out/'restored.log')
    finally:
        counts=Counter(e['outcome']for e in entries)
        for k in ['killed','survived','demonstrably_equivalent','invalid','inconclusive','unrun']:counts.setdefault(k,0)
        denominator=sum(counts[k]for k in ['killed','survived','inconclusive','unrun'])
        receipt['accounting']={**counts,'conservative_ratio':counts['killed']/denominator if denominator else None}
        receipt['staged_sources_unchanged']=all(digest(Path(p))==h for p,h in staged.items());receipt['live_sources_unchanged']=live==inventory();receipt['dependencies_unchanged']=all(digest(Path(p))==h for p,h in dependencies.items())
        receipt['mutations_sha256']=digest(out/'mutations.json');remove_owned(work/'build',work);receipt['owned_build_removed']=True
        write(out/'receipt.json',receipt);print(receipt['accounting'],flush=True)

if __name__=='__main__':main()
