import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import yaml

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T233710Z_separator_extension'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
    with p.open('xb') as f:f.write((json.dumps(x,separators=(',',':'))+'\n').encode())
P2=RUN/'p2';req=json.loads((RUN/'p1/request.json').read_bytes())
delta=yaml.safe_load((RUN/'p1/operad_delta.yaml').read_bytes())
for g in delta['add_or_refine_generators']:g['evidence_status']='native implementation checks passed; required Lean source repair remains'
for r in delta['add_or_refine_relations']:r['evidence_status']='not accepted as general theorem: P2 Lean compilation failed'
delta['open_obligations']=['P3 repair of source/kernel acceptance without changing the target','P4 challenge after P2 recheck','General rational gluing and input transport still open']
(P2/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False,width=100).encode())
dump(P2/'request.json',{'task_id':req['task_id'],'stage_id':'P2_VERIFY','attempt_id':'p2','input_sha256':sha(RUN/'p1/candidate.json'),'candidate':'../p1/candidate.json'})
host={'task_id':req['task_id'],'stage_id':'P2_VERIFY','attempt_id':'p2','input_sha256':sha(RUN/'p1/candidate.json'),
 'candidate_sha256':sha(RUN/'p1/candidate.json'),'status':'repairable_candidate_defect','bounded_failure_codes':['G5_SCOPE'],
 'checker_pins':[{'path':(RUN/'check_candidate.py').relative_to(ROOT).as_posix(),'sha256':sha(RUN/'check_candidate.py')}],
 'predicate_results':{'G1_SCHEMA':'passed original bytes and bindings','G2_COCHAIN':'not applicable: no chain complex',
 'G3_WITNESS':json.loads((P2/'logs/certificate_0.stdout.log').read_bytes()),
 'G4_COUNTERMODEL':'all claimed obstructions verified against compatible inputs and actual violated facets',
 'G5_SCOPE':'FAILED required Lean anchors: original source has a heartbeat timeout and proof dependency errors'},
 'native_receipts':['python_receipt.json','rust_receipt.json','certificate_receipt.json','lean_receipt.json','rust_replay_receipt.json'],
 'operad_delta':delta,'claim_boundary':{'supports':'finite native certificates only at this rejected host attempt','does_not_support':'acceptance of uncompiled general theorems',
 'narrowest_claim':req['public_context']['reviewed_work']['work_unit']['objective'],'next_test':'P3 source repair followed by P2 recheck'}}
dump(P2/'host_check.json',host);dump(P2/'candidate.json',{'checked_candidate':'../p1/candidate.json','candidate_sha256':host['candidate_sha256']})
shutil.copyfile(P2/'host_check.json',P2/'raw_response.txt')
spec=importlib.util.spec_from_file_location('prepare',ROOT/'dag/pfp/prepare_stage.py');prepare=importlib.util.module_from_spec(spec);spec.loader.exec_module(prepare)
prompt=ROOT/'dag/prompts/FINITE_QM_CORE__FQ-BELL-CLASSICAL-JOINT-EXTENSION__PROVED_LEAN.yaml'
P3=RUN/'p3';P3.mkdir(exist_ok=True)
packet=prepare.build_packet(prompt,'P3_REPAIR',attempt_id='p3',reviewed_path=RUN/'p0/reviewed_missions.json',review_path=RUN/'p0/host_review.json',candidate_path=RUN/'p1/candidate.json',host_check_path=P2/'host_check.json')
dump(P3/'request.json',packet)
# Repair is local source work, not a blinded/provider/model comparison. Raw host
# diagnostics stay in the host checkpoint and are absent from the P3 packet.
lean=ROOT/'lean4/BellSeparatorExtension.lean';text=lean.read_text()
start=text.index('-- The only remaining real-valued step')
end=text.index('def TripleCellsPositive')
replacement='''-- Expand the Frechet endpoint constraints before using linear arithmetic.
-- This avoids a large simultaneous max/min case split.
theorem lower_expanded (d a c b x z r : Int) :
    lower d a c b x z ≤ r ↔
    0 ≤ r ∧ a+c-d ≤ r ∧ x+z-b ≤ r ∧ a+c-x-z-d+b ≤ r := by
  unfold lower
  omega

theorem upper_expanded (a c x z r : Int) :
    r ≤ upper a c x z ↔ r ≤ a ∧ r ≤ c ∧ r ≤ x+c-z ∧ r ≤ z+a-x := by
  unfold upper
  omega

set_option maxHeartbeats 1000000 in
theorem separator_iff_chsh (p : PairCounts) (hp : CompatiblePositive p) :
    HasSeparator p ↔ CHSHFamily p := by
  simp only [CompatiblePositive, PairPositive] at hp
  simp only [HasSeparator, lower_expanded, upper_expanded, CHSHFamily, FourCHSH, corr]
  constructor
  · rintro ⟨r,hr⟩
    omega
  · intro hc
    refine ⟨max 0 (max (p.a+p.c-p.d)
      (max (p.x00+p.x10-p.b0) (max (p.a+p.c-p.x00-p.x10-p.d+p.b0)
      (max (p.x01+p.x11-p.b1) (p.a+p.c-p.x01-p.x11-p.d+p.b1))))), ?_⟩
    omega

theorem overlap_iff_chsh (p : PairCounts) (hp : CompatiblePositive p) :
    commonLower p ≤ commonUpper p ↔ CHSHFamily p :=
  (separator_iff_overlap p).symm.trans (separator_iff_chsh p hp)

'''
text=text[:start]+replacement+text[end:]
text=text.replace('  obtain ⟨_,h00,_,h10,_⟩ := hp\n  have h01 : PairPositive p.d p.a p.b1 p.x01 := hp.2.2.1\n  have h11 : PairPositive p.d p.c p.b1 p.x11 := hp.2.2.2.2',
 '  obtain ⟨_,h00,h01,h10,h11⟩ := hp')
start=text.index('theorem full_family_joint_necessity')
end=text.index('end QuantumMechanics.BellSeparatorExtension',start)
replacement='''theorem weighted_map_facet (f : Facet) (law : List (Nat × Assignment)) :
    weightedChshSum (law.map fun p => (p.1, facetLinear f (products p.2))) =
    weighted (fun a => facetLinear f (products a)) law := by
  induction law with
  | nil => rfl
  | cons p rest ih =>
    change (p.1 : Int) * facetLinear f (products p.2) +
      weightedChshSum (rest.map fun p => (p.1, facetLinear f (products p.2))) =
      (p.1 : Int) * facetLinear f (products p.2) + weighted (fun a => facetLinear f (products a)) rest
    rw [ih]

theorem mass_map_facet (f : Facet) (law : List (Nat × Assignment)) :
    totalWeight (law.map fun p => (p.1, facetLinear f (products p.2))) = mass law := by
  induction law with
  | nil => rfl
  | cons p rest ih =>
    change (p.1 : Int) + totalWeight (rest.map fun p => (p.1, facetLinear f (products p.2))) =
      (p.1 : Int) + mass rest
    rw [ih]

theorem full_family_joint_necessity (f : Facet) (law : List (Nat × Assignment)) :
    -2 * mass law ≤ facetLinear f (expect4 products law) ∧
    facetLinear f (expect4 products law) ≤ 2 * mass law := by
  let ws := law.map fun p => (p.1, facetLinear f (products p.2))
  have hb : ∀ p ∈ ws, -2 ≤ p.2 ∧ p.2 ≤ 2 := by
    intro p hp
    obtain ⟨x,_,rfl⟩ := List.mem_map.mp hp
    exact deterministic_facet_bound f x.2
  have h := (fq_bell_classical_joint_extension_convex_bound ws hb).2
  dsimp only [ws] at h
  rw [weighted_map_facet, mass_map_facet, ← facet_expectation] at h
  exact h

'''
text=text[:start]+replacement+text[end:];lean.write_bytes(text.encode())
candidate=json.loads((RUN/'p1/candidate.json').read_bytes())
for key in ['task_id','stage_id','attempt_id','input_sha256']:candidate[key]=packet[key]
dump(P3/'candidate.json',candidate)
sources=json.loads((RUN/'p1/response.json').read_bytes())['construction'];pins=[]
for pin in sources:
    name=pin['working_source'];dest=P3/'construction'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
    pins.append({'path':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),'working_source':name})
for generator in delta['add_or_refine_generators']:generator['source_pins']=pins;generator['evidence_status']='P3 repaired source submitted; P2 recheck pending'
for relation in delta['add_or_refine_relations']:relation['source_pins']=pins;relation['evidence_status']='P3 source repair submitted; no acceptance before recheck'
(P3/'operad_delta.yaml').write_bytes(yaml.safe_dump(delta,sort_keys=False,width=100).encode())
response={**{k:packet[k] for k in ['task_id','stage_id','attempt_id','input_sha256']},
 'replacement_candidate_certificate':{'path':'candidate.json','sha256':sha(P3/'candidate.json')},
 'repaired_invariants':['source/kernel acceptance: expand max/min endpoints into linear constraints','proof dependency and induction scope'],
 'construction':pins,'remaining_obligations':delta['open_obligations'],'operad_delta':delta,
 'repair_mode':'same local researcher with normal compiler diagnostics; not a blinded model trial; public P3 packet contains bounded failure code only',
 'claim_boundary':{'supports':'complete replacement submission with unchanged mathematical inputs','does_not_support':'kernel acceptance before recheck',
 'narrowest_claim':candidate['scope'],'next_test':'P2 native and kernel recheck'}}
dump(P3/'response.json',response);shutil.copyfile(P3/'response.json',P3/'raw_response.txt')
print('Original P2 rejection retained; bounded P3 packet and repaired complete submission saved.')
