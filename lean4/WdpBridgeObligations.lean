import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.BigOperators
import Mathlib.SetTheory.Cardinal.Finite
import Mathlib.Algebra.Order.Group.Nat
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Data.Nat.Prime.Basic

/-!
# Ledger of the five open Genesis-to-WDP bridge obligations (GEN-WDP-O01 .. O05)

AuthorityEffect: None.  Scope: bookkeeping.  An obligation carries one of three statuses: `Open`, `ControlOnly`
(a scoped control passes but the obligation is not discharged) or `Discharged`.  This vocabulary is INVENTED
here: the register (genesis_bridge_register.md rows GEN-WDP-O01..O05) labels each obligation OPEN and never says "control-only";
reading all five as `ControlOnly` (the vector 11111 of the certificate) is this node's reading of "scoped controls are done,
end-to-end claims are not".  `EndToEnd` is DEFINED as
"every obligation is Discharged": this is a modelling choice (the register gives no independent semantics for
"end-to-end", only that the end-to-end claims are not done), so `endToEnd_iff_*` below are definitional
bookkeeping lemmas, not mathematical discoveries.  The `Fin n` versions are general; `n = 5` is an instance.
The "programme order" (`PrefixOrder`) is the derivation order of genesis_to_wdp_derivation_programme.md section 6
mapped to O01 < O02 < O03 < O04 < O05 by us; the sources call it an order of derivation, not a logical
prerequisite relation.  Nothing here discharges, or says anything about the dischargeability of, any obligation.
The source witness `pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl` contains a Boolean AND of
five flags (proved here as `bool_and_iff`) and a bounded check `p*p <> 2*q*q` for `p <= 6, q <= 4`, which is
generalised here to all naturals (`no_sq_eq_two_sq`; this is the arithmetic core of the separate row GEN-WDP-68, it does not
bear on O04 as the register words it).  `wdpPairDefect` is only the symmetrisation `adj u v || adj v u` of a finite window
(`false` exactly when there is no edge in either direction); no source transition system and no map to preserve or reflect
is constructed (that is O02).  The columns `upgrades`, `completing_upgrades`, `prefix_order` and `node_reading` of the certificate
are native definitions (only `raise_completes`, `prefixOrder_of_endToEnd` have Lean counterparts).
-/

namespace WdpBridgeObligations

/-- Status of one bridge obligation in the ledger. -/
inductive Status where
  | Open
  | ControlOnly
  | Discharged
  deriving DecidableEq, Repr

instance : Fintype Status :=
  ⟨{Status.Open, Status.ControlOnly, Status.Discharged}, fun x => by cases x <;> simp⟩

/-- Numeric rank, used for the progress order. -/
def Status.rank : Status → Nat
  | .Open => 0
  | .ControlOnly => 1
  | .Discharged => 2

theorem rank_le_two (s : Status) : s.rank ≤ 2 := by cases s <;> simp [Status.rank]

theorem rank_eq_two {s : Status} : s.rank = 2 ↔ s = .Discharged := by cases s <;> simp [Status.rank]

variable {n : Nat}

/-- The end-to-end claim holds iff every obligation is discharged (definition). -/
def EndToEnd (v : Fin n → Status) : Prop := ∀ k, v k = .Discharged

/-- Every obligation has at least a scoped control. -/
def ControlsRun (v : Fin n → Status) : Prop := ∀ k, v k ≠ .Open

/-- Number of discharged obligations. -/
def dischargedCount (v : Fin n → Status) : Nat := (Finset.univ.filter (fun k => v k = .Discharged)).card

theorem endToEnd_iff_count (v : Fin n → Status) : EndToEnd v ↔ dischargedCount v = n := by
  unfold EndToEnd dischargedCount
  constructor
  · intro h
    have : Finset.univ.filter (fun k => v k = .Discharged) = Finset.univ := by
      ext k; simp [h k]
    rw [this]; simp
  · intro h k
    have hs : Finset.univ.filter (fun k => v k = .Discharged) = Finset.univ :=
      Finset.eq_univ_of_card _ (by simpa using h)
    have : k ∈ Finset.univ.filter (fun k => v k = .Discharged) := by rw [hs]; exact Finset.mem_univ k
    simpa using this

/-- Five-obligation instance: end-to-end is the conjunction of the five statuses (general in the statuses). -/
theorem endToEnd_five (v : Fin 5 → Status) :
    EndToEnd v ↔ v 0 = .Discharged ∧ v 1 = .Discharged ∧ v 2 = .Discharged ∧ v 3 = .Discharged ∧ v 4 = .Discharged := by
  simp [EndToEnd, Fin.forall_fin_succ]

/-- A scoped control does not discharge: a model where every obligation has a passing control and the end-to-end claim fails. -/
theorem control_only_not_discharged (hn : 0 < n) : ∃ v : Fin n → Status, ControlsRun v ∧ ¬ EndToEnd v :=
  ⟨fun _ => .ControlOnly, fun k => by simp, fun h => by have := h ⟨0, hn⟩; simp at this⟩

/-- End-to-end = every obligation has a control and none is still control-only. -/
theorem endToEnd_iff_controls_and_no_control (v : Fin n → Status) :
    EndToEnd v ↔ ControlsRun v ∧ ∀ k, v k ≠ .ControlOnly := by
  constructor
  · intro h
    exact ⟨fun k => by simp [h k], fun k => by simp [h k]⟩
  · rintro ⟨h1, h2⟩ k
    cases hk : v k
    · exact absurd hk (h1 k)
    · exact absurd hk (h2 k)
    · rfl

/-- Leave-one-out: one undischarged obligation blocks the end-to-end claim. -/
theorem not_endToEnd_of_not_discharged (v : Fin n → Status) (k : Fin n) (h : v k ≠ .Discharged) : ¬ EndToEnd v :=
  fun e => h (e k)

/-- Sharpness of leave-one-out: all discharged except position `k` is end-to-end iff position `k` is discharged too. -/
theorem update_sharp [DecidableEq (Fin n)] (k : Fin n) (s : Status) :
    EndToEnd (Function.update (fun _ : Fin n => Status.Discharged) k s) ↔ s = .Discharged := by
  constructor
  · intro h; simpa using h k
  · intro hs j
    by_cases hj : j = k
    · subst hj; simp [hs]
    · simp [Function.update, hj]

/-- Pointwise progress order. -/
def Le (v w : Fin n → Status) : Prop := ∀ k, (v k).rank ≤ (w k).rank

theorem endToEnd_mono {v w : Fin n → Status} (h : Le v w) (hv : EndToEnd v) : EndToEnd w := by
  intro k
  have h1 := h k
  rw [rank_eq_two.mpr (hv k)] at h1
  exact rank_eq_two.mp (le_antisymm (rank_le_two _) h1)

/-- Monotone status update: raise obligation `k` to `s` unless that would lower it. -/
def raise [DecidableEq (Fin n)] (v : Fin n → Status) (k : Fin n) (s : Status) : Fin n → Status :=
  Function.update v k (if (v k).rank ≤ s.rank then s else v k)

theorem le_raise [DecidableEq (Fin n)] (v : Fin n → Status) (k : Fin n) (s : Status) : Le v (raise v k s) := by
  intro j
  by_cases hj : j = k
  · subst hj
    unfold raise
    simp only [Function.update_self]
    split_ifs with h
    · exact h
    · exact le_refl _
  · simp [raise, Function.update, hj]

/-- A monotone update never undoes an end-to-end claim. -/
theorem raise_preserves_endToEnd [DecidableEq (Fin n)] {v : Fin n → Status} (k : Fin n) (s : Status)
    (hv : EndToEnd v) : EndToEnd (raise v k s) :=
  endToEnd_mono (le_raise v k s) hv

/-- One monotone update completes the ledger when exactly the updated position was undischarged. -/
theorem raise_completes [DecidableEq (Fin n)] (v : Fin n → Status) (k : Fin n)
    (h : ∀ j, j ≠ k → v j = .Discharged) : EndToEnd (raise v k .Discharged) := by
  intro j
  by_cases hj : j = k
  · subst hj
    have h2 : (v j).rank ≤ Status.Discharged.rank := rank_le_two _
    simp [raise, h2]
  · simp [raise, Function.update, hj, h j hj]

/-- Programme order (our mapping of the derivation order of the programme document): discharged obligations form a prefix. -/
def PrefixOrder (v : Fin n → Status) : Prop := ∀ j k : Fin n, j ≤ k → v k = .Discharged → v j = .Discharged

theorem prefixOrder_of_endToEnd (v : Fin n → Status) (h : EndToEnd v) : PrefixOrder v :=
  fun j _ _ _ => h j

/-- Instance: discharging only the last of five obligations violates the programme order. -/
theorem prefixOrder_violation :
    ¬ PrefixOrder (fun k : Fin 5 => if k = 4 then Status.Discharged else Status.Open) := by
  intro h
  have := h 0 4 (by decide) (by simp)
  simp at this

/-- There are 3^5 = 243 ledger vectors and exactly one is end-to-end. -/
theorem card_vectors : Fintype.card (Fin 5 → Status) = 243 := by
  simp
  decide

theorem endToEnd_unique : Nat.card {v : Fin 5 → Status // EndToEnd v} = 1 := by
  have : Unique {v : Fin 5 → Status // EndToEnd v} :=
    { default := ⟨fun _ => .Discharged, fun _ => rfl⟩
      uniq := fun y => Subtype.ext (funext fun k => y.2 k) }
  exact Nat.card_unique

/-! ### Source declarations re-proved at their general scope -/

/-- The source's five-flag Boolean AND is exactly the conjunction. -/
theorem bool_and_iff (o1 o2 o3 o4 o5 : Bool) :
    (o1 && o2 && o3 && o4 && o5) = true ↔ (o1 = true ∧ o2 = true ∧ o3 = true ∧ o4 = true ∧ o5 = true) := by
  cases o1 <;> cases o2 <;> cases o3 <;> cases o4 <;> cases o5 <;> simp

/-- Source: finite window and its symmetrised adjacency (genesis_to_wdp_bridge_preserves_and_reflects). -/
structure FiniteGenesisWindow (m : Nat) where
  adj : Fin m → Fin m → Bool

def wdpPairDefect {m : Nat} (w : FiniteGenesisWindow m) (u v : Fin m) : Bool := w.adj u v || w.adj v u

theorem pairDefect_preserves_and_reflects {m : Nat} (w : FiniteGenesisWindow m) (u v : Fin m) :
    wdpPairDefect w u v = false ↔ (w.adj u v = false ∧ w.adj v u = false) := by
  unfold wdpPairDefect
  rw [Bool.or_eq_false_iff]

/-- Limit of that map: it forgets orientation, so two different windows have the same symmetrisation. -/
theorem pairDefect_forgets_orientation :
    ∃ w w' : FiniteGenesisWindow 2, (∃ u v, w.adj u v ≠ w'.adj u v) ∧ ∀ u v, wdpPairDefect w u v = wdpPairDefect w' u v := by
  refine ⟨⟨fun u v => decide (u = 0 ∧ v = 1)⟩, ⟨fun u v => decide (u = 1 ∧ v = 0)⟩, ⟨0, 1, by decide⟩, ?_⟩
  intro u v
  unfold wdpPairDefect
  revert u v
  decide

/-- Arithmetic core of GEN-WDP-68 at general scope (the source checks only q <= 4, p <= 6): no p, q > 0 with p^2 = 2 q^2. -/
theorem no_sq_eq_two_sq : ∀ q : Nat, 0 < q → ∀ p : Nat, p * p ≠ 2 * (q * q) := by
  intro q
  induction q using Nat.strong_induction_on with
  | _ q ih =>
    intro hq p hp
    have h2p : 2 ∣ p * p := ⟨q * q, hp⟩
    have hpe : 2 ∣ p := (Nat.Prime.dvd_mul Nat.prime_two).mp h2p |>.elim id id
    obtain ⟨r, rfl⟩ := hpe
    have h2 : q * q = 2 * (r * r) := by nlinarith
    have hr : 0 < r := by
      rcases Nat.eq_zero_or_pos r with h | h
      · subst h; simp at h2; omega
      · exact h
    have hrq : r < q := by nlinarith
    exact ih r hrq hr q h2

end WdpBridgeObligations

#print axioms WdpBridgeObligations.endToEnd_iff_count
#print axioms WdpBridgeObligations.endToEnd_five
#print axioms WdpBridgeObligations.control_only_not_discharged
#print axioms WdpBridgeObligations.endToEnd_iff_controls_and_no_control
#print axioms WdpBridgeObligations.not_endToEnd_of_not_discharged
#print axioms WdpBridgeObligations.update_sharp
#print axioms WdpBridgeObligations.endToEnd_mono
#print axioms WdpBridgeObligations.le_raise
#print axioms WdpBridgeObligations.raise_preserves_endToEnd
#print axioms WdpBridgeObligations.raise_completes
#print axioms WdpBridgeObligations.prefixOrder_of_endToEnd
#print axioms WdpBridgeObligations.prefixOrder_violation
#print axioms WdpBridgeObligations.card_vectors
#print axioms WdpBridgeObligations.endToEnd_unique
#print axioms WdpBridgeObligations.bool_and_iff
#print axioms WdpBridgeObligations.pairDefect_preserves_and_reflects
#print axioms WdpBridgeObligations.pairDefect_forgets_orientation
#print axioms WdpBridgeObligations.no_sq_eq_two_sq
