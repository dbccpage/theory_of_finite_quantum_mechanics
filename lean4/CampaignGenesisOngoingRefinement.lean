import H3V7N5QF.Answers
import CampaignGenesisOngoingRename

/-! AuthorityEffect: None. Arrays represent arbitrary finite term sets and
assertion sets, with both tracked names retained. Arrays may contain duplicate
entries; decode takes their sets. No apart-name or consecutive-label bound. -/
namespace CampaignGenesisOngoingRefinement
open Seed

structure Wire where
  terms : Array Nat
  assertions : Array (Nat × Nat)
  a : Nat
  b : Nat
deriving DecidableEq

def decode (w : Wire) : St :=
  ⟨w.terms.toList.toFinset,w.assertions.toList.toFinset,w.a,w.b⟩

noncomputable def encode (s : St) : Wire := ⟨s.T.toList.toArray,s.A.toList.toArray,s.a,s.b⟩

@[simp] theorem decode_encode (s : St) : decode (encode s) = s := by
  cases s; simp [decode,encode]

def Legal (w : Wire) : Prop := ∀ x, (x,x) ∉ w.assertions.toList
def WF (w : Wire) : Prop :=
  (∀ p ∈ w.assertions.toList, p.1 ∈ w.terms.toList ∧ p.2 ∈ w.terms.toList) ∧
  w.a ∈ w.terms.toList ∧ w.b ∈ w.terms.toList

theorem legal_iff_source (w : Wire) : Legal w ↔ (decode w).Legal := by
  simp [Legal,decode,St.Legal]

theorem wf_iff_source (w : Wire) : WF w ↔ (decode w).WF := by
  simp [WF,decode,St.WF]

def wireCostA (w : Wire) : Nat :=
  w.terms.toList.toFinset.card + w.assertions.toList.toFinset.card +
    2 * (if w.a = w.b then 2 else if (w.a,w.b) ∈ w.assertions.toList then 0 else 1)

def wireCostB (w : Wire) : Nat :=
  w.terms.toList.toFinset.card + w.assertions.toList.toFinset.card +
    2 * (if w.a = w.b then 3 else
      (if (w.a,w.b) ∈ w.assertions.toList then 0 else 1) +
      (if (w.b,w.a) ∈ w.assertions.toList then 0 else 1))

theorem costA_exact (w : Wire) : wireCostA w = Seed.costA (decode w) := by
  simp [wireCostA,Seed.costA,St.size,Seed.lostA,Seed.miss,decode]

theorem costB_exact (w : Wire) : wireCostB w = Seed.costB (decode w) := by
  simp [wireCostB,Seed.costB,St.size,Seed.lostB,Seed.miss,decode]

def addTerm (w : Wire) (x : Nat) : Wire := {w with terms := w.terms.push x}
def addAssertion (w : Wire) (x y : Nat) : Wire :=
  {w with assertions := w.assertions.push (x,y)}
def remove (w : Wire) (p : Nat × Nat) : Wire :=
  {w with assertions := w.assertions.filter (· != p)}
def identify (w : Wire) (u v : Nat) : Wire :=
  ⟨w.terms.filter (· != v), w.assertions.map (Prod.map (merge u v) (merge u v)),
    merge u v w.a,merge u v w.b⟩

theorem decode_addTerm (w : Wire) (x : Nat) :
    decode (addTerm w x) = (decode w).addTerm x := by
  simp [decode,addTerm,St.addTerm,List.toFinset_append]

theorem decode_addAssertion (w : Wire) (x y : Nat) :
    decode (addAssertion w x y) = (decode w).addAssertion x y := by
  simp [decode,addAssertion,St.addAssertion,List.toFinset_append]

theorem decode_remove (w : Wire) (p : Nat × Nat) :
    decode (remove w p) = (decode w).remove p := by
  apply St.ext <;> simp [decode,remove,St.remove,Finset.ext_iff,and_comm]

theorem decode_identify (w : Wire) (u v : Nat) :
    decode (identify w u v) = (decode w).identify u v := by
  apply St.ext <;> simp [decode,identify,St.identify,Finset.ext_iff,and_comm]

/-- Constructors contain every source guard. An obstructed attempted image
is not a performed wire step. Duplicate writes are not counted as changes. -/
inductive Step : Wire → Wire → Prop
  | addTerm (w : Wire) (x : Nat) (hx : x ∉ w.terms.toList) : Step w (addTerm w x)
  | addAssertion (w : Wire) (x y : Nat) (hx : x ∈ w.terms.toList) (hy : y ∈ w.terms.toList)
      (hne : x ≠ y) (hn : (x,y) ∉ w.assertions.toList) : Step w (addAssertion w x y)
  | remove (w : Wire) (p : Nat × Nat) (hp : p ∈ w.assertions.toList) : Step w (remove w p)
  | identify (w : Wire) (u v : Nat) (hu : u ∈ w.terms.toList) (hv : v ∈ w.terms.toList)
      (hne : u ≠ v) (h1 : (u,v) ∉ w.assertions.toList) (h2 : (v,u) ∉ w.assertions.toList) :
      Step w (identify w u v)

theorem step_sound {w v : Wire} (h : Step w v) : Seed.Step (decode w) (decode v) := by
  cases h with
  | addTerm x hx => rw [decode_addTerm]; exact Seed.Step.addTerm _ _ (by simpa [decode] using hx)
  | addAssertion x y hx hy hne hn =>
    rw [decode_addAssertion]
    exact Seed.Step.addAssertion _ _ _ (by simpa [decode] using hx)
      (by simpa [decode] using hy) hne (by simpa [decode] using hn)
  | remove p hp => rw [decode_remove]; exact Seed.Step.remove _ _ (by simpa [decode] using hp)
  | identify u v hu hv hne h1 h2 =>
    rw [decode_identify]
    exact Seed.Step.identify _ _ _ (by simpa [decode] using hu)
      (by simpa [decode] using hv) hne (by simpa [decode] using h1) (by simpa [decode] using h2)

theorem step_complete {w : Wire} {t : St} (h : Seed.Step (decode w) t) :
    ∃ v, Step w v ∧ decode v = t := by
  cases h with
  | addTerm x hx =>
    exact ⟨addTerm w x, Step.addTerm _ _ (by simpa [decode] using hx),decode_addTerm _ _⟩
  | addAssertion x y hx hy hne hn =>
    exact ⟨addAssertion w x y,Step.addAssertion _ _ _ (by simpa [decode] using hx)
      (by simpa [decode] using hy) hne (by simpa [decode] using hn),decode_addAssertion _ _ _⟩
  | remove p hp =>
    exact ⟨remove w p,Step.remove _ _ (by simpa [decode] using hp),decode_remove _ _⟩
  | identify u v hu hv hne h1 h2 =>
    exact ⟨identify w u v,Step.identify _ _ _ (by simpa [decode] using hu)
      (by simpa [decode] using hv) hne (by simpa [decode] using h1)
      (by simpa [decode] using h2),decode_identify _ _ _⟩

inductive Reach : Wire → Wire → Nat → Prop
  | refl (w : Wire) : Reach w w 0
  | step {w v z : Wire} {n : Nat} : Reach w v n → Step v z → Reach w z (n+1)

theorem reach_sound {w v : Wire} {n : Nat} (h : Reach w v n) :
    Seed.Reach (decode w) (decode v) n := by
  induction h with
  | refl => exact Seed.Reach.refl _
  | step _ st ih => exact Seed.Reach.step ih (step_sound st)

theorem reach_complete {s t : St} {n : Nat} (h : Seed.Reach s t n) :
    ∀ w, decode w = s → ∃ v, Reach w v n ∧ decode v = t := by
  induction h with
  | refl => intro w hw; exact ⟨w,Reach.refl _,hw⟩
  | step hr st ih =>
    intro w hw
    obtain ⟨v,hv,hd⟩ := ih w hw
    obtain ⟨z,hz,he⟩ := step_complete (hd.symm ▸ st)
    exact ⟨z,Reach.step hv hz,he⟩

theorem exact_transition_representation (w : Wire) (t : St) (n : Nat) :
    (∃ v, Reach w v n ∧ decode v = t) ↔ Seed.Reach (decode w) t n := by
  constructor
  · rintro ⟨v,hv,rfl⟩; exact reach_sound hv
  · intro h; exact reach_complete h w rfl

theorem legal_wf_preserved {w v : Wire} {n : Nat} (h : Reach w v n)
    (hl : (decode w).Legal) (hw : (decode w).WF) :
    (decode v).Legal ∧ (decode v).WF :=
  ⟨(reach_sound h).legal hl,(reach_sound h).wf hw⟩

def rename (π : Nat → Nat) (w : Wire) : Wire :=
  ⟨w.terms.map π,w.assertions.map (Prod.map π π),π w.a,π w.b⟩

theorem decode_rename (π : Nat → Nat) (w : Wire) :
    decode (rename π w) = Seed.Second.rename π (decode w) := by
  apply St.ext <;> simp [decode,rename,Seed.Second.rename,Finset.ext_iff]

theorem source_step_rename (π : Nat → Nat) (hπ : Function.Injective π)
    {s t : St} (h : Seed.Step s t) :
    Seed.Step (Seed.Second.rename π s) (Seed.Second.rename π t) := Seed.Second.Step.rename hπ h

theorem source_reach_rename (π : Nat → Nat) (hπ : Function.Injective π)
    {s t : St} {n : Nat} (h : Seed.Reach s t n) :
    Seed.Reach (Seed.Second.rename π s) (Seed.Second.rename π t) n := Seed.Second.Reach.rename hπ h

theorem renaming_costs (π : Nat → Nat) (hπ : Function.Injective π) (w : Wire) :
    wireCostA (rename π w) = wireCostA w ∧ wireCostB (rename π w) = wireCostB w := by
  simp only [costA_exact,costB_exact,decode_rename]
  exact ⟨Seed.Second.costA_rename hπ _,Seed.Second.costB_rename hπ _⟩

theorem wire_reach_rename (π : Nat → Nat) (hπ : Function.Injective π)
    {w v : Wire} {n : Nat} (h : Reach w v n) :
    ∃ z, Reach (rename π w) z n ∧ decode z = Seed.Second.rename π (decode v) :=
  reach_complete (source_reach_rename π hπ (reach_sound h)) (rename π w) (decode_rename π w)

theorem tracked_obstruction_persists {s t : St} {u₀ v₀ u v n : Nat}
    (h : Seed.Second.ReachNoRemove s u₀ v₀ t u v n) (hs : s.Legal) (hp : (u₀,v₀) ∈ s.A) :
    (u,v) ∈ t.A ∧ u ≠ v ∧ ¬ (t.identify u v).Legal :=
  h.obstruction_persists hs hp

theorem identify_obstruction_iff (w : Wire) (hl : Legal w) (u v : Nat) :
    Legal (identify w u v) ↔ (u,v) ∉ w.assertions.toList ∧ (v,u) ∉ w.assertions.toList := by
  rw [legal_iff_source,decode_identify,Seed.identify_legal_iff ((legal_iff_source w).mp hl)]
  simp [decode]

theorem assertion_obstruction_iff (w : Wire) (hl : Legal w) (x y : Nat) :
    Legal (addAssertion w x y) ↔ x ≠ y := by
  rw [legal_iff_source,decode_addAssertion]
  exact Seed.addAssertion_legal_iff ((legal_iff_source w).mp hl) x y

theorem one_step_new_assertion_old_endpoints {s t : St} (h : Seed.Step s t)
    (hs : s.WF) {p : Nat × Nat} (hp : p ∈ t.A) (hn : p ∉ s.A) :
    p.1 ∈ s.T ∧ p.2 ∈ s.T := by
  have hw := h.wf hs
  cases h with
  | addTerm x hx => exact False.elim (hn hp)
  | addAssertion x y hx hy hne hnew =>
    rcases Finset.mem_insert.mp hp with he | ho
    · cases he; exact ⟨hx,hy⟩
    · exact False.elim (hn ho)
  | remove q hq => exact False.elim (hn (Finset.mem_of_mem_erase hp))
  | identify u v hu hv hne h1 h2 =>
    exact ⟨Finset.mem_of_mem_erase (hw.1 p hp).1,Finset.mem_of_mem_erase (hw.1 p hp).2⟩

theorem build_lower_bound {s g : St} {n : Nat} (hr : Seed.Reach s g n)
    (hs : s.WF) (hg : g.Legal) (q : Nat → Nat) (hq : ∀ x ∈ s.T, q x = x)
    {x : Nat} (himg : (x,x) ∈ g.A.image (Prod.map q q)) : 2 ≤ n := by
  obtain ⟨p,hp,hn,hout⟩ := Seed.build_needs_term_and_assertion hs hg q hq himg
  by_contra hsmall
  have hnsmall : n = 0 ∨ n = 1 := by omega
  rcases hnsmall with rfl | rfl
  · cases hr; exact hn hp
  · cases hr with
    | step hprev hstep =>
      cases hprev
      have hold := one_step_new_assertion_old_endpoints hstep hs hp hn
      exact hout.elim (fun h => h hold.1) (fun h => h hold.2)

theorem build_two_steps (w : Wire) (hl : Legal w) (hw : WF w) (x t : Nat)
    (hx : x ∈ w.terms.toList) (ht : t ∉ w.terms.toList) :
    ∃ v, Reach w v 2 ∧ Legal v ∧ decode v = ((decode w).addTerm t).addAssertion x t := by
  have hr := Seed.build_answer ((wf_iff_source w).mp hw)
    (by simpa [decode] using hx) (by simpa [decode] using ht)
  obtain ⟨v,hv,he⟩ := reach_complete hr w rfl
  exact ⟨v,hv,(legal_iff_source v).mpr ((reach_sound hv).legal ((legal_iff_source w).mp hl)),he⟩

theorem wire_build_lower_bound {w v : Wire} {n : Nat} (hr : Reach w v n)
    (hw : WF w) (hl : Legal v) (q : Nat → Nat)
    (hq : ∀ x ∈ w.terms.toList, q x = x) {x : Nat}
    (himg : (x,x) ∈ (decode v).A.image (Prod.map q q)) : 2 ≤ n :=
  build_lower_bound (reach_sound hr) ((wf_iff_source w).mp hw)
    ((legal_iff_source v).mp hl) q (by simpa [decode] using hq) himg

theorem full_fewest_A (w : Wire) (hl : (decode w).Legal) (hw : (decode w).WF) :
    (∃ (π : Equiv.Perm Nat) (n : Nat) (v : Wire),
      Reach (encode (Seed.Second.rename π Seed.givenA)) v n ∧ decode v = decode w ∧
      n+3 = wireCostA w) ∧
    ∀ (π : Equiv.Perm Nat) (v : Wire) (n : Nat),
      Reach (encode (Seed.Second.rename π Seed.givenA)) v n → decode v = decode w →
      wireCostA w ≤ n+3 := by
  simp only [costA_exact]
  obtain ⟨⟨π,n,hr,hc⟩,hlo⟩ := Seed.Second.fewest_changes_every_writing_A hl hw
  obtain ⟨v,hv,he⟩ := reach_complete hr (encode _) (decode_encode _)
  exact ⟨⟨π,n,v,hv,he,hc⟩,fun π v n hv he => hlo π n (by simpa [he] using reach_sound hv)⟩

theorem full_fewest_B (w : Wire) (hl : (decode w).Legal) (hw : (decode w).WF) :
    (∃ (π : Equiv.Perm Nat) (n : Nat) (v : Wire),
      Reach (encode (Seed.Second.rename π Seed.givenB)) v n ∧ decode v = decode w ∧
      n+4 = wireCostB w) ∧
    ∀ (π : Equiv.Perm Nat) (v : Wire) (n : Nat),
      Reach (encode (Seed.Second.rename π Seed.givenB)) v n → decode v = decode w →
      wireCostB w ≤ n+4 := by
  simp only [costB_exact]
  obtain ⟨⟨π,n,hr,hc⟩,hlo⟩ := Seed.Second.fewest_changes_every_writing_B hl hw
  obtain ⟨v,hv,he⟩ := reach_complete hr (encode _) (decode_encode _)
  exact ⟨⟨π,n,v,hv,he,hc⟩,fun π v n hv he => hlo π n (by simpa [he] using reach_sound hv)⟩

end CampaignGenesisOngoingRefinement

#print axioms CampaignGenesisOngoingRefinement.decode_encode
#print axioms CampaignGenesisOngoingRefinement.decode_addTerm
#print axioms CampaignGenesisOngoingRefinement.decode_addAssertion
#print axioms CampaignGenesisOngoingRefinement.decode_remove
#print axioms CampaignGenesisOngoingRefinement.decode_identify
#print axioms CampaignGenesisOngoingRefinement.step_sound
#print axioms CampaignGenesisOngoingRefinement.step_complete
#print axioms CampaignGenesisOngoingRefinement.reach_sound
#print axioms CampaignGenesisOngoingRefinement.reach_complete
#print axioms CampaignGenesisOngoingRefinement.exact_transition_representation
#print axioms CampaignGenesisOngoingRefinement.legal_wf_preserved
#print axioms CampaignGenesisOngoingRefinement.full_fewest_A
#print axioms CampaignGenesisOngoingRefinement.full_fewest_B
#print axioms Seed.Second.Step.rename
#print axioms Seed.Second.Reach.rename
#print axioms Seed.Second.costA_rename
#print axioms Seed.Second.costB_rename
#print axioms Seed.Second.ReachNoRemove.obstruction_persists
#print axioms Seed.build_answer
#print axioms Seed.build_answer_reverse
#print axioms Seed.build_gives_back
#print axioms Seed.build_needs_term_and_assertion

#print axioms CampaignGenesisOngoingRefinement.legal_iff_source
#print axioms CampaignGenesisOngoingRefinement.wf_iff_source
#print axioms CampaignGenesisOngoingRefinement.costA_exact
#print axioms CampaignGenesisOngoingRefinement.costB_exact

#print axioms CampaignGenesisOngoingRefinement.one_step_new_assertion_old_endpoints
#print axioms CampaignGenesisOngoingRefinement.build_lower_bound
#print axioms CampaignGenesisOngoingRefinement.build_two_steps
#print axioms CampaignGenesisOngoingRefinement.wire_build_lower_bound

#print axioms CampaignGenesisOngoingRefinement.decode_rename
#print axioms CampaignGenesisOngoingRefinement.source_step_rename
#print axioms CampaignGenesisOngoingRefinement.source_reach_rename
#print axioms CampaignGenesisOngoingRefinement.renaming_costs
#print axioms CampaignGenesisOngoingRefinement.wire_reach_rename
#print axioms CampaignGenesisOngoingRefinement.tracked_obstruction_persists

#print axioms CampaignGenesisOngoingRefinement.identify_obstruction_iff
#print axioms CampaignGenesisOngoingRefinement.assertion_obstruction_iff
