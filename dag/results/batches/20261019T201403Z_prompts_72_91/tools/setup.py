"""Install twenty new scoped work units while preserving all previous evidence."""
import importlib.util,json,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent
if (SRC/'installed_batch.json').exists():raise ValueError('This creation driver already ran')
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');ID=stamp+'_prompts_72_91';RUN=stamp+'_staged';B=ROOT/'dag/results/batches'/ID;OLD=ROOT/'dag/results/batches/20261019T184100Z_prompts_52_71'
def put(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('refusing overwrite '+str(p))
    p.write_bytes(data)
put(B/'.gitattributes',b'* -text whitespace=-trailing-space,-blank-at-eof\n')
for name in ('native.py','target_stages.py'):put(B/name,(OLD/name).read_bytes().replace(b'20261019T184100Z_prompts_52_71',ID.encode()))
t=(OLD/'tools/init.py').read_text().replace('20261019T184100Z_prompts_52_71',ID).replace('20261019T184100Z_staged',RUN).replace('selected = nodes[51:71]','selected = nodes[71:91]').replace('positions 52 through 71 after the fifty-one completed nodes','positions 72 through 91 after the seventy-one completed nodes')
put(B/'tools/init.py',t.encode());subprocess.run([sys.executable,'-X','utf8',str(B/'tools/init.py')],cwd=ROOT,check=True);put(B/'index_before.json',(ROOT/'dag/operads/index.json').read_bytes())
for name,dest in [('boundaries_exact.py','code/python/src/qm/boundaries_exact.py'),('boundaries_exact.rs','code/rust/src/finite_probability/boundaries_exact.rs'),('boundaries_checker.py','dag/pfp/boundaries_checker.py'),('test_boundaries_exact.py','code/python/tests/test_boundaries_exact.py')]:put(ROOT/dest,(SRC/name).read_bytes())
p=ROOT/'code/rust/src/finite_probability/lib.rs';p.write_bytes(p.read_bytes()+b'\npub mod boundaries_exact;\n')
p=ROOT/'lean4/lakefile.lean';p.write_bytes(p.read_bytes().replace(b'    `PromptResources,',b'    `PromptResources,\n    `PromptBoundaries,'))
sp=importlib.util.spec_from_file_location('producer_for_declared_tables',SRC/'boundaries_exact.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
finite='def q8mul (a b : Fin 8) : Fin 8 :=\n  match a.val,b.val with\n'
for i in range(8):
    for j in range(8):finite+=f'  | {i},{j} => {m.qcode(m.qmul(m.quat(i),m.quat(j)))}\n'
finite+='  | _,_ => 0\n'
finite+='''def q8inv (a : Fin 8) : Fin 8 := if a.val%4=0 then a else ⟨(a.val+4)%8,Nat.mod_lt _ (by decide)⟩
theorem q8_associative : ∀ a b c : Fin 8,q8mul (q8mul a b) c=q8mul a (q8mul b c) := by decide
theorem q8_identity_inverse : ∀ a : Fin 8,q8mul 0 a=a ∧ q8mul a 0=a ∧ q8mul a (q8inv a)=0 ∧ q8mul (q8inv a) a=0 := by decide
theorem q8_pure_gauge : ∀ a b c : Fin 8,
    q8mul (q8mul (q8mul (q8inv a) b) (q8mul (q8inv b) c)) (q8mul (q8inv c) a)=0 := by decide
theorem q8_commutator : q8mul (q8mul (q8mul 1 2) (q8inv 1)) (q8inv 2)=4 := by decide
theorem parity_no_global : ∀ a b c d e f g h i : Fin 2,
    ¬ ((a.val+b.val+c.val)%2=0 ∧ (d.val+e.val+f.val)%2=0 ∧ (g.val+h.val+i.val)%2=0 ∧
      (a.val+d.val+g.val)%2=0 ∧ (b.val+e.val+h.val)%2=0 ∧ (c.val+f.val+i.val)%2=1) := by decide
def mpParity (n : ℕ) : ℕ :=
'''
contexts=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]
expr=[]
for j,c in enumerate(contexts):expr.append('(('+'+'.join(f'(n/{2**i})%2' for i in c)+f')%2)*{2**j}')
finite+='  '+'+\n  '.join(expr)+'\n'
finite+='def mpSelected (mask : ℕ) (n : Fin 512) : Bool := decide (Nat.land (Nat.xor (mpParity n.val) 32) mask=0)\n'
finite+='def droppedWitness (o : Fin 6) : Fin 512 :=\n  match o.val with\n'
for j in range(6):finite+=f'  | {j} => {m.mp_solutions(63^(1<<j))[0]}\n'
finite+='  | _ => 0\ntheorem parity_every_drop : ∀ o : Fin 6,mpSelected (63-2^o.val) (droppedWitness o)=true := by decide\n'
text=(SRC/'PromptBoundaries.lean').read_text().replace('-- FINITE_TABLES',finite);anchors=re.findall(r'^theorem (\w+)',text,re.M);text+='\n'+'\n'.join('#print axioms QuantumMechanics.PromptBoundaries.'+a for a in anchors)+'\n';put(ROOT/'lean4/PromptBoundaries.lean',text.encode())
put(ROOT/'code/rust/src/finite_probability/examples/boundaries_exact_replay.rs',(ROOT/'code/rust/src/finite_probability/examples/resources_exact_replay.rs').read_bytes().replace(b'resources_exact',b'boundaries_exact'))
put(B/'tools/specs.py',(SRC/'specs.py').read_bytes());sys.path.insert(0,str(SRC));from specs import S
checks={
 'registry':'assert_eq!(v[7],n(1));assert_eq!(v[10],n(2));',
 'uniqueness':'assert_eq!(v[21],n(0));assert_eq!(v[12..15],[n(1),n(1),n(1)]);',
 'cochain':'assert_eq!(v[16],v[17]);assert_eq!(v[17],v[18]);assert_eq!(v[22],n(0));',
 'survival':'assert_eq!(v[3],n(0));',
 'relative':'assert_eq!(v[21],n(0));assert_eq!(&v[20]+&v[23],n(1));assert_eq!(v[27],n(0));',
 'threshold':'assert_eq!(v[..5],[n(3),n(2),n(1),n(0),n(0)]);assert_eq!(v[5],n(1));',
 'syndrome':'assert!(v[2]<v[0]);assert_eq!(*v.last().unwrap(),n(2));',
 'packet':'assert_eq!(v[4],n(0));assert_eq!(v[6],n(1));assert_eq!(v[7],n(2));',
 'q8':'assert_eq!(v[3],n(0));assert_eq!(v[4],n(4));assert_eq!(*v.last().unwrap(),n(-1));',
 'parity':'assert_eq!(v[63],n(0));assert_eq!(v[64],n(0));assert_eq!(v[65],n(-1));',
 'born':'assert_eq!(v[8],v[9]);assert_ne!(v[2],v[4]);',
 'synthesis':'assert_eq!(v[0],v[2]);assert_eq!(v[5],n(0));assert!(v[10..].iter().all(|q|q.is_zero()));',
 'cascade':'assert_eq!(v[2],v[3]);assert_eq!(v[9],n(288));',
 'majorana':'assert_eq!(v[24],n(-1));assert_eq!(v[27],n(-1));assert_eq!(v[16..20],vec![n(0);4]);',
 'busch':'assert_eq!(v[24..28],[n(1),n(0),n(0),n(1)]);assert_eq!(v[35],n(3)/n(10));assert_eq!(v[40],n(1));',
 'choi':'assert_eq!(v[40],n(1));assert_eq!(v[42],n(2));',
 'proxy':'assert_eq!(v[31],n(0));assert_eq!(v[31..].iter().cloned().sum::<Q>(),n(4));',
 'maps':'assert_eq!(v[6],n(0));assert_eq!(v[7],v[8]);assert!(v[7]>=n(0));',
 'tensor':'assert_eq!(v[12],v[14]);assert_ne!(v[16],v[18]);',
 'torsion':'assert_eq!(v[9],v[10]);assert_eq!(v[5..7],v[7..9]);assert_eq!(v[11],v[12]);'}
p=ROOT/'code/rust/src/finite_probability/boundaries_exact.rs';text=p.read_text();text+='\n#[cfg(test)] mod tests { use super::*; fn run(k:&str,s:&[&str])->Vec<Q>{evaluate(k,&s.iter().map(|x|x.to_string()).collect::<Vec<_>>()).iter().map(|x|q(x)).collect()}\n'
for row in S:
    k=row['kind'];v=','.join(json.dumps(q) for q in row['cases'][0]);text+=f'#[test] fn boundaries_{k}(){{let v=run("{k}",&[{v}]);{checks[k]}}}\n'
text+='''#[test] fn boundaries_q8_all_group_products(){for a in 0..8{for b in 0..8{for c in 0..8{assert_eq!(qm(qm(quat(a),quat(b)),quat(c)),qm(quat(a),qm(quat(b),quat(c))));}}assert_eq!(qm(quat(a),qi(quat(a))),quat(0));}}
#[test] fn boundaries_parity_all_subsets(){for m in 0_usize..64{assert_eq!(solutions(m).len(),if m==63{0}else{1<<(9-m.count_ones())});}}
#[test] fn boundaries_proxy_all_rows(){for k in 0..5{let v=proxy(k);for j in 0..5{assert_eq!(v[31+j],n((k!=j as i64)as i64));}}}
#[test] #[should_panic] fn boundaries_refuse_even_repetition(){run("syndrome",&["2"]);}
}\n'''
p.write_bytes(text.encode());subprocess.run([str(Path.home()/'.cargo/bin/rustfmt.exe'),'--edition','2021',str(p),str(ROOT/'code/rust/src/finite_probability/examples/boundaries_exact_replay.rs')],check=True)
put(B/'lean_order.json',b'["PromptBoundaries"]\n')
t=(OLD/'tools/prepare.py').read_text().replace('resources_exact','boundaries_exact').replace('resources_checker','boundaries_checker').replace('PromptResources','PromptBoundaries').replace('independent-resources-','independent-boundaries-').replace("'resources_'+kind","'boundaries_'+kind").replace('resources_producer','boundaries_producer')
put(B/'tools/prepare.py',t.encode())
for tool in ('run.py','repair.py','execute_remaining.py'):put(B/'tools'/tool,(OLD/'tools'/tool).read_bytes())
put(B/'tools/setup.py',Path(__file__).read_bytes());receipt={'batch_id':ID,'run_id':RUN,'path':str(B),'Lean_anchors':len(anchors)};put(SRC/'installed_batch.json',(json.dumps(receipt,indent=2)+'\n').encode());print(json.dumps(receipt),flush=True)
