"""Source-bound standalone trials for the staged strict A-infinity module.
AuthorityEffect: None. Prototype evidence; no source capability/grade promotion.
"""
import argparse,json,shutil,subprocess
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
from replay import ROOT,RUST,digest,write,execute,remove_owned

def recipes():
    return [
      ('AI01-prime-boundary','if p < 2 {','if p <= 2 {','unit'),
      ('AI02-composite-domain','if p % divisor == 0 {','if false {','unit'),
      ('AI03-addition-widening','u32::from(a) + u32::from(b)','u32::from(a.wrapping_add(b))','unit'),
      ('AI04-product-widening','u64::from(a) * u64::from(b)','u64::from(a.wrapping_mul(b))','unit'),
      ('AI05-differential-domain','        check_coefficients(field, "differential", &differential)?;','','unit'),
      ('AI06-product-domain','        check_coefficients(field, "product", &product)?;','','unit'),
      ('AI07-differential-grading','                self.check_d_degree(i, j)?;','','unit'),
      ('AI08-product-grading','                self.check_product_degrees(i, j)?;','','unit'),
      ('AI09-differential-square','        self.check_d_squared()?;','','unit'),
      ('AI10-leibniz','        self.check_leibniz()?;','','unit'),
      ('AI11-associativity','        self.check_associativity()\n','        Ok(())\n','unit'),
      ('AI12-koszul-sign','if self.degrees[left].rem_euclid(2) != 0 {','if false {','unit'),
      ('AI13-output-zero','values.resize(cells, 0);','values.resize(cells, 1);','unit'),
      ('AI14-field-privacy','pub struct PrimeField {\n    modulus: u16,','pub struct PrimeField {\n    pub modulus: u16,','doc'),
      ('AI15-algebra-privacy','    field: PrimeField,\n    degrees: Vec<i32>,\n    differential: Vec<u16>,\n    product: Vec<u16>,','    pub field: PrimeField,\n    pub degrees: Vec<i32>,\n    pub differential: Vec<u16>,\n    pub product: Vec<u16>,','doc'),
      ('AI16-operation-privacy',"    algebra: &'a StrictAInfinity,\n    coefficients: Option<&'a [u16]>,","    pub algebra: &'a StrictAInfinity,\n    pub coefficients: Option<&'a [u16]>,",'doc'),
      ('AI17-basis-boundary','    fn check_basis(&self, index: usize) -> Result<()> {\n        if index >= self.dimension() {','    fn check_basis(&self, index: usize) -> Result<()> {\n        if index > self.dimension() {','unit'),
      ('AI18-view-boundary','    pub fn coefficient(&self, index: usize) -> Result<u16> {\n        if index >= self.dimension() {','    pub fn coefficient(&self, index: usize) -> Result<u16> {\n        if index > self.dimension() {','unit'),
      ('AI19-inclusive-admission','if requested > limit {','if requested >= limit {','unit'),
      ('AI20-admission-refusal','if requested > limit {','if false {','unit'),
      ('AI21-differential-work','1 => mul(mul(n, n)?, 2),','1 => mul(mul(n, n)?, 1),','unit'),
      ('AI22-product-work','2 => mul(mul(mul(n, n)?, n)?, 3),','2 => mul(mul(mul(n, n)?, n)?, 2),','unit'),
      ('AI23-input-domain','            check_coefficients(self.field, "input vector", input)?;','','unit'),
      ('AI24-input-shape','            shape("input vector", self.dimension(), input.len())?;','','unit'),
      ('AI25-higher-basis-domain','            self.check_basis(index)?;','','unit'),
      ('AI26-differential-shape','    shape("differential", square, differential)?;','','unit'),
      ('AI27-product-shape','    shape("product", cube, product)\n','    Ok(())\n','unit'),
      ('AI28-identity-work','mul(cube, 5)?','mul(cube, 4)?','unit'),
      ('AI29-higher-zero-coefficient','self.coefficients.map_or(0, |values| values[index])','self.coefficients.map_or(1, |values| values[index])','unit'),
      ('AA01-output-admission-order','        self.admit_evaluation(inputs, limits)?;\n        let mut output = zero_buffer(self.dimension())?;','        let mut output = zero_buffer(self.dimension())?;\n        self.admit_evaluation(inputs, limits)?;','allocation'),
    ]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=RUST/'quality/l4a_six/a_infinity_candidate.rs');args=parser.parse_args()
    source=args.source.resolve();original=source.read_bytes();text=original.decode('utf-8-sig')
    entries=[dict(id=i,before=b,after=a,mode=m,outcome='unrun')for i,b,a,m in recipes()]
    bad=[e['id']for e in entries if text.count(e['before'])!=1]
    if bad:raise RuntimeError('Nonunique recipes: '+str(bad))
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-a-infinity-trial'
    out=ROOT/'evidence/quality/l4a_six'/stamp;out.mkdir()
    work=RUST/'target/l4a-six'/stamp;work.mkdir(parents=True);build=work/'build';build.mkdir()
    module=work/'module.rs';module.write_bytes(original);_copy_record_file(module,out/'module.rs')
    wrapper=work/'lib.rs';wrapper.write_text('#[path="module.rs"]\npub mod a_infinity;\n');_copy_record_file(wrapper,out/'lib.rs')
    allocation=work/'allocation.rs';_copy_record_file(Path(__file__).with_name('a_infinity_allocation_candidate.rs'),allocation);_copy_record_file(allocation,out/'allocation.rs')
    _copy_record_file(__file__,out/'trial.py');_copy_record_file(Path(__file__).with_name('replay.py'),out/'replay.py')
    receipt={'AuthorityEffect':'None','scope':'Standalone staged module: unit, compiler privacy and allocation challenges. Not integrated package evidence or an automatic grade.','source':str(source.relative_to(ROOT)),'source_sha256':digest(source),'runner_sha256':digest(out/'trial.py'),'helper_sha256':digest(out/'replay.py'),'allocation_sha256':digest(out/'allocation.rs'),'versions':{x:subprocess.check_output([x,'--version'],text=True).strip()for x in ['rustc','rustdoc']},'baselines':[],'restored_baselines':[]}
    print(out,flush=True)
    def run(mode,label):
        runs=[]
        if mode=='unit':compile=['rustc','--edition','2021','--test',str(module),'-o',str(build/'tests.exe')]
        else:compile=['rustc','--edition','2021','--crate-name','tfqm_homotopy_type_theory','--crate-type','rlib',str(wrapper),'-o',str(build/'libtfqm_homotopy_type_theory.rlib')]
        result=execute(compile,work,out/(label+'-compile.log'),timeout=90);runs.append(result)
        if result['timed_out']:return 'inconclusive',runs
        if result['exit_code']!=0:return 'invalid',runs
        external=['--extern','tfqm_homotopy_type_theory='+str(build/'libtfqm_homotopy_type_theory.rlib')]
        if mode=='allocation':
            result=execute(['rustc','--edition','2021','--test',str(allocation),*external,'-o',str(build/'allocation.exe')],work,out/(label+'-allocation-compile.log'),timeout=90);runs.append(result)
            if result['timed_out']:return 'inconclusive',runs
            if result['exit_code']!=0:return 'invalid',runs
        command={'unit':[str(build/'tests.exe')],'doc':['rustdoc','--edition','2021','--test',str(module),*external],'allocation':[str(build/'allocation.exe')]}[mode]
        result=execute(command,work,out/(label+'-test.log'),timeout=90);runs.append(result)
        log=(ROOT/result['log']).read_text(encoding='utf-8')
        outcome='survived'if result['exit_code']==0 else 'killed'if 'test result: FAILED'in log else 'inconclusive'
        return outcome,runs
    try:
        for mode in ['unit','doc','allocation']:
            outcome,runs=run(mode,'baseline-'+mode);receipt['baselines'].append({'mode':mode,'passed':outcome=='survived','runs':runs})
        if not all(x['passed']for x in receipt['baselines']):return
        for e in entries:
            try:
                module.write_text(text.replace(e['before'],e['after'],1),encoding='utf-8');e['candidate_sha256']=digest(module)
                e['outcome'],e['runs']=run(e['mode'],e['id']);print(e['id'],e['outcome'],flush=True)
            finally:
                module.write_bytes(original);e['source_restored']=digest(module)==digest(source);write(out/'mutations.json',entries)
        for mode in ['unit','doc','allocation']:
            outcome,runs=run(mode,'restored-'+mode);receipt['restored_baselines'].append({'mode':mode,'passed':outcome=='survived','runs':runs})
    finally:
        counts=Counter(e['outcome']for e in entries)
        for k in ['killed','survived','demonstrably_equivalent','invalid','inconclusive','unrun']:counts.setdefault(k,0)
        den=sum(counts[k]for k in ['killed','survived','inconclusive','unrun']);receipt['accounting']={**counts,'conservative_ratio':counts['killed']/den if den else None}
        write(out/'mutations.json',entries);receipt['mutations_sha256']=digest(out/'mutations.json');receipt['source_unchanged']=digest(source)==receipt['source_sha256']
        remove_owned(build,work);receipt['owned_build_removed']=True;write(out/'receipt.json',receipt);print(receipt['accounting'],flush=True)
if __name__=='__main__':main()
