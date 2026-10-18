import Mathlib.Tactic

/-!
# QMComposeMonoidalStructure — W6.14 / OB-COMPOSE (classical product + composition no-gos)

Programme target: DERIV-MASTER W6.14 (QMREG-64 / freeze `OB-COMPOSE` / recovery T11).

Mechanized on a finite bit toy:

1. **Cartesian product** of two residual bit weights is **constructible** (classical).
2. **Direct sum** disagrees with product on sector count for bit-2/bit-3 toys.
3. **Classical purification fails** for mixed bits: pure joints have pure marginals.
4. **Local-tomography dimension identity** for complex Hilbert counting;
   rebit $9\neq 10$ and quat $36\neq 28$ as lift-relative LT failures.
5. **Declared tensor** interface requires a `NamedLift` (ℂ/ℝ/ℍ binds share dim product).
6. **FinL1 product ⊬ complex composite LT** (`finL1_product_does_not_force_complex_lt`).

**Not claimed:** full monoidal CPTP category; uniqueness of complex tensor;
absolute LT↔OB-U1 independence outside the NamedLift registry; authority or promotion.

**LT↔OB-U1 residual (deepened):** on the three-lift registry the faces are
**COUPLED** (no NamedLift XOR-splits); residual `SPLIT-OUTSIDE-REGISTRY` stays
**OPEN** (path for future non-registry models); `ExoticHost` is exploratory only.

AuthorityEffect: None.
-/

namespace QM
namespace ComposeMonoidal

/-! ## Composition candidates (freeze labels) -/

inductive CompositionKind where
  | cartesianProduct
  | directSum
  | declaredTensor
deriving DecidableEq, Repr

def productSectorCount (nA nB : Nat) : Nat := nA * nB
def sumSectorCount (nA nB : Nat) : Nat := nA + nB

/-- 2×3: product sectors 6 ≠ sum sectors 5. (Note: 2×2 is a degenerate case 4=4.) -/
theorem product_ne_sum_bit2x3 :
    productSectorCount 2 3 ≠ sumSectorCount 2 3 := by
  decide

theorem product_ne_sum_bit3 :
    productSectorCount 3 3 ≠ sumSectorCount 3 3 := by
  decide

/-! ## Bit residual weights -/

structure BitWeight where
  w0 : Int
  w1 : Int
deriving DecidableEq, Repr

namespace BitWeight

def total (w : BitWeight) : Int := w.w0 + w.w1

def IsNonneg (w : BitWeight) : Prop := w.w0 ≥ 0 ∧ w.w1 ≥ 0

def IsPure (w : BitWeight) : Prop :=
  (w.w0 > 0 ∧ w.w1 = 0) ∨ (w.w0 = 0 ∧ w.w1 > 0)

def IsMixed (w : BitWeight) : Prop := w.w0 > 0 ∧ w.w1 > 0

theorem mixed_not_pure (w : BitWeight) (hm : IsMixed w) : ¬ IsPure w := by
  intro hp
  rcases hm with ⟨h0, h1⟩
  rcases hp with h | h
  · exact (ne_of_gt h1) h.2
  · exact (ne_of_gt h0) h.1

end BitWeight

/-! ## Joint tables on Bool × Bool -/

structure JointWeight where
  w00 : Int
  w01 : Int
  w10 : Int
  w11 : Int
deriving DecidableEq, Repr

namespace JointWeight

def total (j : JointWeight) : Int := j.w00 + j.w01 + j.w10 + j.w11

def margA (j : JointWeight) : BitWeight :=
  { w0 := j.w00 + j.w01, w1 := j.w10 + j.w11 }

def margB (j : JointWeight) : BitWeight :=
  { w0 := j.w00 + j.w10, w1 := j.w01 + j.w11 }

def IsPure (j : JointWeight) : Prop :=
  (j.w00 > 0 ∧ j.w01 = 0 ∧ j.w10 = 0 ∧ j.w11 = 0) ∨
  (j.w01 > 0 ∧ j.w00 = 0 ∧ j.w10 = 0 ∧ j.w11 = 0) ∨
  (j.w10 > 0 ∧ j.w00 = 0 ∧ j.w01 = 0 ∧ j.w11 = 0) ∨
  (j.w11 > 0 ∧ j.w00 = 0 ∧ j.w01 = 0 ∧ j.w10 = 0)

end JointWeight

/-- Classical product composition (DERIVED on the basement). -/
def productJoint (wa wb : BitWeight) : JointWeight :=
  { w00 := wa.w0 * wb.w0
    w01 := wa.w0 * wb.w1
    w10 := wa.w1 * wb.w0
    w11 := wa.w1 * wb.w1 }

theorem product_margA_w0 (wa wb : BitWeight) :
    (productJoint wa wb).margA.w0 = wa.w0 * wb.total := by
  simp [productJoint, JointWeight.margA, BitWeight.total]; ring

theorem product_margA_w1 (wa wb : BitWeight) :
    (productJoint wa wb).margA.w1 = wa.w1 * wb.total := by
  simp [productJoint, JointWeight.margA, BitWeight.total]; ring

theorem product_margB_w0 (wa wb : BitWeight) :
    (productJoint wa wb).margB.w0 = wb.w0 * wa.total := by
  simp [productJoint, JointWeight.margB, BitWeight.total]; ring

theorem product_margB_w1 (wa wb : BitWeight) :
    (productJoint wa wb).margB.w1 = wb.w1 * wa.total := by
  simp [productJoint, JointWeight.margB, BitWeight.total]; ring

theorem product_margA_of_unit_B (wa wb : BitWeight) (hB : wb.total = 1) :
    (productJoint wa wb).margA.w0 = wa.w0 ∧
    (productJoint wa wb).margA.w1 = wa.w1 := by
  constructor
  · simpa [hB] using product_margA_w0 wa wb
  · simpa [hB] using product_margA_w1 wa wb

/-! ## Classical purification no-go -/

theorem pure_joint_margA_pure (j : JointWeight) (hp : j.IsPure) :
    (j.margA).IsPure := by
  rcases hp with ⟨h00, h01, h10, h11⟩ | ⟨h01, h00, h10, h11⟩ | ⟨h10, h00, h01, h11⟩ | ⟨h11, h00, h01, h10⟩
  · -- 00
    refine Or.inl ⟨?_, ?_⟩
    · change j.w00 + j.w01 > 0
      simp [h01]; exact h00
    · change j.w10 + j.w11 = 0
      simp [h10, h11]
  · -- 01
    refine Or.inl ⟨?_, ?_⟩
    · change j.w00 + j.w01 > 0
      simp [h00]; exact h01
    · change j.w10 + j.w11 = 0
      simp [h10, h11]
  · -- 10
    refine Or.inr ⟨?_, ?_⟩
    · change j.w00 + j.w01 = 0
      simp [h00, h01]
    · change j.w10 + j.w11 > 0
      simp [h11]; exact h10
  · -- 11
    refine Or.inr ⟨?_, ?_⟩
    · change j.w00 + j.w01 = 0
      simp [h00, h01]
    · change j.w10 + j.w11 > 0
      simp [h10]; exact h11

theorem pure_joint_margB_pure (j : JointWeight) (hp : j.IsPure) :
    (j.margB).IsPure := by
  rcases hp with ⟨h00, h01, h10, h11⟩ | ⟨h01, h00, h10, h11⟩ | ⟨h10, h00, h01, h11⟩ | ⟨h11, h00, h01, h10⟩
  · refine Or.inl ⟨?_, ?_⟩
    · change j.w00 + j.w10 > 0
      simp [h10]; exact h00
    · change j.w01 + j.w11 = 0
      simp [h01, h11]
  · refine Or.inr ⟨?_, ?_⟩
    · change j.w00 + j.w10 = 0
      simp [h00, h10]
    · change j.w01 + j.w11 > 0
      simp [h11]; exact h01
  · refine Or.inl ⟨?_, ?_⟩
    · change j.w00 + j.w10 > 0
      simp [h00]; exact h10
    · change j.w01 + j.w11 = 0
      simp [h01, h11]
  · refine Or.inr ⟨?_, ?_⟩
    · change j.w00 + j.w10 = 0
      simp [h00, h10]
    · change j.w01 + j.w11 > 0
      simp [h01]; exact h11

theorem mixed_has_no_pure_classical_purification
    (w : BitWeight) (hm : w.IsMixed) :
    ¬ ∃ j : JointWeight, j.IsPure ∧ j.margA = w := by
  intro ⟨j, hp, heq⟩
  have hpure : (j.margA).IsPure := pure_joint_margA_pure j hp
  have : w.IsPure := by simpa [heq] using hpure
  exact BitWeight.mixed_not_pure w hm this

def fairBit : BitWeight := { w0 := 1, w1 := 1 }

theorem fairBit_mixed : fairBit.IsMixed := by
  dsimp [fairBit, BitWeight.IsMixed]
  exact ⟨Int.one_pos, Int.one_pos⟩

theorem fairBit_no_classical_purification :
    ¬ ∃ j : JointWeight, j.IsPure ∧ j.margA = fairBit :=
  mixed_has_no_pure_classical_purification fairBit fairBit_mixed

def fairProduct : JointWeight := productJoint fairBit fairBit

theorem fairProduct_cells :
    fairProduct.w00 = 1 ∧ fairProduct.w01 = 1 ∧
    fairProduct.w10 = 1 ∧ fairProduct.w11 = 1 := by
  dsimp [fairProduct, productJoint, fairBit]
  exact ⟨rfl, rfl, rfl, rfl⟩

/-! ## Local-tomography dimension counts -/

/-- **ARITHMETIC ONLY — NOT a tomography theorem.** This is `ring` on `Nat`: it
holds for any `dA dB` with no quantum structure whatsoever. It states the
*necessary* dimension condition for the product effects to span the joint effect
space, never the spanning itself. Do not cite it as evidence that complex local
tomography holds; that claim is `[OPEN]` (see the module header). The spanning
statement, and its failure in the real case, live in
`rebit_local_tomography_counterexample.lean`. -/
theorem complex_local_tomography_dim (dA dB : Nat) :
    (dA * dA) * (dB * dB) = (dA * dB) * (dA * dB) := by
  ring

/-- **VACUOUS — this is literally `X = X`.** Retained only so the defect stays on
the record rather than being silently deleted. It is reflexivity, carries no
content, and must not appear in any evidence list. -/
theorem complex_lt_dim_qubit2 :
    (2 * 2) * (2 * 2) = (2 * 2) * (2 * 2) := by
  decide

/-- Estate rebit local-tomography fence (`qm_011`: 9 ≠ 10). -/
theorem rebit_local_tomography_count_fence : (3 : Nat) * 3 ≠ 10 := by
  decide

/-! ## Declared tensor bound to a named lift (W6.14 residual)

`CompositionKind.declaredTensor` is **not** constructed from FinL1 residual
tables alone. It is an interface that requires a **named lift** (here:
complex Hilbert). This section freezes that interface and records:

1. composite Hilbert dimension = product of local dims (counting identity);
2. a pure bipartite toy whose reduced A-state is mixed (quantum purification
   *under the named lift*, not from classical pure joints);
3. rebit density-parameter count still fences local tomography ($9\neq 10$).

**Not claimed:** CPTP monoidal category; uniqueness of ℂ; derivation of
purification from the basement carrier; independence of LT from OB-U1.
-/

/-- Named lifts that may host a monoidal tensor. -/
inductive NamedLift where
  | complexHilbert
  | realHilbert
  | quaternionicHilbert
deriving DecidableEq, Repr

/-- Declared-tensor interface: composite Hilbert dim and local dims, tagged by lift. -/
structure DeclaredTensor where
  lift : NamedLift
  dimA : Nat
  dimB : Nat
  /-- Composite Hilbert-space dimension under the named lift. -/
  dimAB : Nat
  /-- Interface law: dimAB equals the product of local dims. -/
  dim_law : dimAB = dimA * dimB

/-- Bind declared tensor to the complex Hilbert lift (interface witness, not uniqueness). -/
def complexHilbertTensor (dA dB : Nat) : DeclaredTensor :=
  { lift := NamedLift.complexHilbert
    dimA := dA
    dimB := dB
    dimAB := dA * dB
    dim_law := rfl }

theorem complexHilbertTensor_lift (dA dB : Nat) :
    (complexHilbertTensor dA dB).lift = NamedLift.complexHilbert := rfl

theorem complexHilbertTensor_qubit :
    (complexHilbertTensor 2 2).dimAB = 4 := by
  rfl

/-- Declared tensor is a distinct composition kind from classical product/sum. -/
theorem declared_tensor_kind_ne_product :
    CompositionKind.declaredTensor ≠ CompositionKind.cartesianProduct := by
  decide

theorem declared_tensor_kind_ne_sum :
    CompositionKind.declaredTensor ≠ CompositionKind.directSum := by
  decide

/-- Without a named lift tag, the interface refuses "orphan" tensor claims.
    Encoded as: any `DeclaredTensor` carries a `NamedLift` field (inhabited). -/
theorem declared_tensor_requires_named_lift (t : DeclaredTensor) :
    ∃ L : NamedLift, t.lift = L :=
  ⟨t.lift, rfl⟩

/-! ### Quantum purification under the named lift (toy)

Classical pure joints cannot purify mixed marginals (above). Under a *named*
complex-Hilbert lift we admit a pure bipartite toy whose A-reduced state is
mixed. The "state" is discrete: four computational-basis amplitudes as Int
squares (Born squares only as **lift readout bookkeeping**, not basement
import discharge of OB-BORN).

Bell-like equal weights on |00⟩ and |11⟩: each cell mass 1; A-marginal fair.
-/

/-- Pure bipartite toy under declared complex-Hilbert tensor (Bell diagonal support). -/
def bellLikeJoint : JointWeight :=
  { w00 := 1, w01 := 0, w10 := 0, w11 := 1 }

/-- Support size 2 with equal positive masses — pure under a 2D lift subspace
    span{|00⟩,|11⟩} with equal |amp|²; *not* classical `JointWeight.IsPure`
    (single atom). This is the purification distinction. -/
def IsQuantumPureSupport (j : JointWeight) : Prop :=
  (j.w00 > 0 ∧ j.w01 = 0 ∧ j.w10 = 0 ∧ j.w11 > 0) ∨
  (j.w00 = 0 ∧ j.w01 > 0 ∧ j.w10 > 0 ∧ j.w11 = 0)

theorem bellLike_quantum_pure_support : IsQuantumPureSupport bellLikeJoint := by
  dsimp [IsQuantumPureSupport, bellLikeJoint]
  exact Or.inl ⟨Int.one_pos, rfl, rfl, Int.one_pos⟩

theorem bellLike_not_classically_pure : ¬ bellLikeJoint.IsPure := by
  intro hp
  -- bellLike = {1,0,0,1}: every classical single-atom disjunct fails a zero cell.
  rcases hp with h | h | h | h
  · -- w11 must be 0
    exact absurd h.2.2.2 (by decide : ¬ ((1 : Int) = 0))
  · -- w00 must be 0
    exact absurd h.2.1 (by decide : ¬ ((1 : Int) = 0))
  · exact absurd h.2.1 (by decide : ¬ ((1 : Int) = 0))
  · exact absurd h.2.1 (by decide : ¬ ((1 : Int) = 0))

theorem bellLike_margA_fair : bellLikeJoint.margA = fairBit := rfl

theorem bellLike_margA_mixed : (bellLikeJoint.margA).IsMixed := by
  simpa [bellLike_margA_fair] using fairBit_mixed

/-- Under the named complex-Hilbert tensor, mixed fairBit admits a
    quantum-pure-support purification (Bell-like). Contrast classical no-go. -/
theorem fairBit_has_quantum_purification_under_complex_lift :
    ∃ j : JointWeight, IsQuantumPureSupport j ∧ j.margA = fairBit :=
  ⟨bellLikeJoint, bellLike_quantum_pure_support, bellLike_margA_fair⟩

/-- The classical pure-joint model still refuses the same mixed state. -/
theorem fairBit_classical_vs_lift_purification_split :
    (¬ ∃ j : JointWeight, j.IsPure ∧ j.margA = fairBit) ∧
    (∃ j : JointWeight, IsQuantumPureSupport j ∧ j.margA = fairBit) :=
  ⟨fairBit_no_classical_purification, fairBit_has_quantum_purification_under_complex_lift⟩

/-- Binding receipt: qubit×qubit declared tensor is the complex-Hilbert lift. -/
def qubitTensor : DeclaredTensor := complexHilbertTensor 2 2

theorem qubitTensor_bound :
    qubitTensor.lift = NamedLift.complexHilbert ∧ qubitTensor.dimAB = 4 :=
  ⟨rfl, rfl⟩

theorem qubitTensor_dim_law : qubitTensor.dimAB = qubitTensor.dimA * qubitTensor.dimB :=
  qubitTensor.dim_law

/-! ## W6.14 residual: composite LT underivable from FinL1 product alone

Classical product only supplies **sector counts** $n_A n_B$. Composite local
tomography compares density-parameter counts under a **named lift**. Same
sector product can host:

* complex: localProd = compositeParams (LT identity holds);
* real / quaternionic: localProd ≠ compositeParams at qubits.

Therefore complex composite LT is **not** forced by FinL1 product composition.
LT law is lift-relative (INTERFACE-BOUND). Composite LT vs `OB-U1` phase-carrier
is **COUPLED** on the NamedLift registry (below); outside-registry split remains
**OPEN** (`SPLIT-OUTSIDE-REGISTRY`).
-/

/-- Free real parameters of a density operator on $d$-dim Hilbert over the field. -/
def densityParams : NamedLift → Nat → Nat
  | .complexHilbert, d => d * d
  | .realHilbert, d => d * (d + 1) / 2
  | .quaternionicHilbert, d => d * (2 * d - 1)

/-- Product of local density-param counts (tomography of product experiments). -/
def localProd (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L dA * densityParams L dB

/-- Composite-system density-param count at tensor dim $d_A d_B$. -/
def compositeParams (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L (dA * dB)

/-- **ARITHMETIC ONLY.** Unfolds to `(dA*dA)*(dB*dB) = (dA*dB)*(dA*dB)`; the
`densityParams` wrapper makes it *look* like a composition obligation, but no
composition is involved. The `.realHilbert` and `.quaternionicHilbert` cases of
`densityParams` do carry content (they are the failures), and those are recorded
below. This complex case is the necessary dimension condition, not a discharge of
the LT obligation. -/
theorem complex_lt_identity (dA dB : Nat) :
    localProd .complexHilbert dA dB = compositeParams .complexHilbert dA dB := by
  simp [localProd, compositeParams, densityParams]
  ring

theorem complex_lt_qubit_pair :
    localProd .complexHilbert 2 2 = compositeParams .complexHilbert 2 2 := by
  decide

/-- Rebit composite LT fails at qubits: $3\cdot 3 = 9 \neq 10 = 4\cdot 5/2$. -/
theorem rebit_lt_fails_qubit_pair :
    localProd .realHilbert 2 2 ≠ compositeParams .realHilbert 2 2 := by
  decide

theorem rebit_lt_numbers :
    localProd .realHilbert 2 2 = 9 ∧ compositeParams .realHilbert 2 2 = 10 := by
  decide

/-- Quaternionic composite LT fails at qubits: $6\cdot 6 = 36 \neq 28 = 4\cdot 7$. -/
theorem quat_lt_fails_qubit_pair :
    localProd .quaternionicHilbert 2 2 ≠ compositeParams .quaternionicHilbert 2 2 := by
  decide

theorem quat_lt_numbers :
    localProd .quaternionicHilbert 2 2 = 36 ∧
    compositeParams .quaternionicHilbert 2 2 = 28 := by
  decide

/-- Classical product sector count agrees with Hilbert dim product (counting only). -/
theorem product_sector_eq_hilbert_dim_count (nA nB : Nat) :
    productSectorCount nA nB = nA * nB := rfl

/-- Same classical product of sector dims hosts all three named-lift tensors. -/
def realHilbertTensor (dA dB : Nat) : DeclaredTensor :=
  { lift := NamedLift.realHilbert
    dimA := dA
    dimB := dB
    dimAB := dA * dB
    dim_law := rfl }

def quaternionicHilbertTensor (dA dB : Nat) : DeclaredTensor :=
  { lift := NamedLift.quaternionicHilbert
    dimA := dA
    dimB := dB
    dimAB := dA * dB
    dim_law := rfl }

theorem real_quat_complex_share_dim_law (dA dB : Nat) :
    (complexHilbertTensor dA dB).dimAB =
      (realHilbertTensor dA dB).dimAB ∧
    (realHilbertTensor dA dB).dimAB =
      (quaternionicHilbertTensor dA dB).dimAB :=
  ⟨rfl, rfl⟩

/-- FinL1 product sector agreement does **not** force complex LT identity:
    real and quaternionic lifts share the dim product but fail LT at qubits. -/
theorem finL1_product_does_not_force_complex_lt :
    productSectorCount 2 2 = (complexHilbertTensor 2 2).dimAB ∧
    productSectorCount 2 2 = (realHilbertTensor 2 2).dimAB ∧
    productSectorCount 2 2 = (quaternionicHilbertTensor 2 2).dimAB ∧
    localProd .complexHilbert 2 2 = compositeParams .complexHilbert 2 2 ∧
    localProd .realHilbert 2 2 ≠ compositeParams .realHilbert 2 2 ∧
    localProd .quaternionicHilbert 2 2 ≠ compositeParams .quaternionicHilbert 2 2 := by
  refine ⟨rfl, rfl, rfl, ?_, ?_, ?_⟩
  · exact complex_lt_qubit_pair
  · exact rebit_lt_fails_qubit_pair
  · exact quat_lt_fails_qubit_pair

/-- LT law is a predicate on the named lift, not on sector product alone. -/
def SatisfiesCompositeLT (L : NamedLift) (dA dB : Nat) : Prop :=
  localProd L dA dB = compositeParams L dA dB

theorem complex_satisfies_composite_lt_qubits :
    SatisfiesCompositeLT .complexHilbert 2 2 :=
  complex_lt_qubit_pair

theorem real_fails_composite_lt_qubits :
    ¬ SatisfiesCompositeLT .realHilbert 2 2 :=
  rebit_lt_fails_qubit_pair

theorem quat_fails_composite_lt_qubits :
    ¬ SatisfiesCompositeLT .quaternionicHilbert 2 2 :=
  quat_lt_fails_qubit_pair

/-- Only `complexHilbert` among the three registry lifts satisfies composite LT
    on the qubit×qubit toy (classification relative to this discrete param model). -/
theorem only_complex_among_three_satisfies_lt_qubits :
    SatisfiesCompositeLT .complexHilbert 2 2 ∧
    ¬ SatisfiesCompositeLT .realHilbert 2 2 ∧
    ¬ SatisfiesCompositeLT .quaternionicHilbert 2 2 :=
  ⟨complex_satisfies_composite_lt_qubits,
    real_fails_composite_lt_qubits,
    quat_fails_composite_lt_qubits⟩

/-! ## W6.14 residual: composite LT ↔ OB-U1 packaged as COUPLED (terminal honesty)

Freeze nesting caveat: the QM_121 / QM_062 *phase-carrier residue* “local
tomography / global field-uniqueness” stays nested under `OB-U1` until a
Wave-6 **independence** argument splits it from `OB-COMPOSE`.

On this **NamedLift registry** toy `{complexHilbert, realHilbert, quaternionicHilbert}`:

* `HasComplexPhaseCarrier` is true only for `complexHilbert` (ℂ/$U(1)$ host).
* `SatisfiesCompositeLT` at qubits is true only for `complexHilbert`.
* Therefore every registry model that carries composite LT also carries the
  complex phase host, and every model that drops the complex phase host also
  drops composite LT — **no NamedLift XOR-splits** ⇒ independence **REFUSED**
  on the registry; status **COUPLED**.

**Dual residual (honest, non-absolute):** `SPLIT-OUTSIDE-REGISTRY` remains
**OPEN** — models outside `{ℂ,ℝ,ℍ}` may still separate the faces. Registry
COUPLED does **not** claim absolute couple for all hosts.

Not claimed: continuum $U(1)$; BASIS-CANDIDATE independence; authority.
-/

/-- Phase-carrier face of `OB-U1` on the named-lift registry (toy predicate). -/
def HasComplexPhaseCarrier : NamedLift → Prop
  | .complexHilbert => True
  | .realHilbert => False
  | .quaternionicHilbert => False

theorem complex_has_phase_carrier :
    HasComplexPhaseCarrier .complexHilbert := trivial

theorem real_no_complex_phase_carrier :
    ¬ HasComplexPhaseCarrier .realHilbert := fun h => h

theorem quat_no_complex_phase_carrier :
    ¬ HasComplexPhaseCarrier .quaternionicHilbert := fun h => h

/-- Coupling witness: LT and complex phase carrier agree on the three-lift registry. -/
theorem lt_iff_complex_phase_on_registry (L : NamedLift) :
    SatisfiesCompositeLT L 2 2 ↔ HasComplexPhaseCarrier L := by
  cases L with
  | complexHilbert =>
    constructor
    · intro _; exact trivial
    · intro _; exact complex_satisfies_composite_lt_qubits
  | realHilbert =>
    constructor
    · intro h; exact (real_fails_composite_lt_qubits h).elim
    · intro h; exact h.elim
  | quaternionicHilbert =>
    constructor
    · intro h; exact (quat_fails_composite_lt_qubits h).elim
    · intro h; exact h.elim

/-- Dual form: phase face ↔ LT face (same biconditional, order flipped for dual packaging). -/
theorem phase_iff_composite_lt_on_registry (L : NamedLift) :
    HasComplexPhaseCarrier L ↔ SatisfiesCompositeLT L 2 2 :=
  (lt_iff_complex_phase_on_registry L).symm

/-- Independence / XOR face split: exactly one of composite LT and complex phase. -/
def IndependentlySplitsLtFromPhase (L : NamedLift) : Prop :=
  (SatisfiesCompositeLT L 2 2 ∧ ¬ HasComplexPhaseCarrier L) ∨
  (¬ SatisfiesCompositeLT L 2 2 ∧ HasComplexPhaseCarrier L)

/-- Alias: XOR split of the two faces on a NamedLift (same Prop; dual packaging name). -/
def XorSplitsLtFromPhase (L : NamedLift) : Prop :=
  IndependentlySplitsLtFromPhase L

theorem no_registry_model_splits_lt_from_phase (L : NamedLift) :
    ¬ IndependentlySplitsLtFromPhase L := by
  intro h
  have heq := lt_iff_complex_phase_on_registry L
  rcases h with ⟨hlt, hnp⟩ | ⟨hnlt, hp⟩
  · exact hnp (heq.mp hlt)
  · exact hnlt (heq.mpr hp)

/-- Formal dual: no NamedLift XOR-splits the two faces (∀ on registry). -/
theorem no_named_lift_xor_splits_lt_from_phase (L : NamedLift) :
    ¬ XorSplitsLtFromPhase L :=
  no_registry_model_splits_lt_from_phase L

/-- Exhaustive registry scan: zero of the three NamedLifts XOR-splits. -/
theorem no_named_lift_xor_registry_scan :
    ¬ IndependentlySplitsLtFromPhase .complexHilbert ∧
    ¬ IndependentlySplitsLtFromPhase .realHilbert ∧
    ¬ IndependentlySplitsLtFromPhase .quaternionicHilbert :=
  ⟨no_registry_model_splits_lt_from_phase _,
    no_registry_model_splits_lt_from_phase _,
    no_registry_model_splits_lt_from_phase _⟩

/-- Boolean dual for decide-friendly face agreement on each NamedLift constructor. -/
def namedLiftHasPhaseBool : NamedLift → Bool
  | .complexHilbert => true
  | .realHilbert => false
  | .quaternionicHilbert => false

def namedLiftSatisfiesLtBool : NamedLift → Bool
  | .complexHilbert => true
  | .realHilbert => false
  | .quaternionicHilbert => false

theorem named_lift_faces_agree_bool (L : NamedLift) :
    namedLiftHasPhaseBool L = namedLiftSatisfiesLtBool L := by
  cases L <;> rfl

theorem named_lift_no_bool_xor (L : NamedLift) :
    namedLiftHasPhaseBool L = namedLiftSatisfiesLtBool L :=
  named_lift_faces_agree_bool L

theorem named_lift_bool_xor_scan :
    namedLiftHasPhaseBool .complexHilbert = namedLiftSatisfiesLtBool .complexHilbert ∧
    namedLiftHasPhaseBool .realHilbert = namedLiftSatisfiesLtBool .realHilbert ∧
    namedLiftHasPhaseBool .quaternionicHilbert = namedLiftSatisfiesLtBool .quaternionicHilbert := by
  decide

/-- Registry face classification: only both / neither (no one-sided class). -/
inductive RegistryFaceClass where
  | both
  | neither
  deriving DecidableEq, Repr

def registryFaceClass : NamedLift → RegistryFaceClass
  | .complexHilbert => .both
  | .realHilbert => .neither
  | .quaternionicHilbert => .neither

theorem registry_face_class_only_both_or_neither (L : NamedLift) :
    registryFaceClass L = .both ∨ registryFaceClass L = .neither := by
  cases L with
  | complexHilbert => exact Or.inl rfl
  | realHilbert => exact Or.inr rfl
  | quaternionicHilbert => exact Or.inr rfl

theorem registry_face_class_both_iff (L : NamedLift) :
    registryFaceClass L = .both ↔
      (SatisfiesCompositeLT L 2 2 ∧ HasComplexPhaseCarrier L) := by
  cases L with
  | complexHilbert =>
    constructor
    · intro _; exact ⟨complex_satisfies_composite_lt_qubits, trivial⟩
    · intro _; rfl
  | realHilbert =>
    constructor
    · intro h; cases h
    · intro ⟨hlt, _⟩; exact (real_fails_composite_lt_qubits hlt).elim
  | quaternionicHilbert =>
    constructor
    · intro h; cases h
    · intro ⟨hlt, _⟩; exact (quat_fails_composite_lt_qubits hlt).elim

theorem registry_face_class_neither_iff (L : NamedLift) :
    registryFaceClass L = .neither ↔
      (¬ SatisfiesCompositeLT L 2 2 ∧ ¬ HasComplexPhaseCarrier L) := by
  cases L with
  | complexHilbert =>
    constructor
    · intro h; cases h
    · intro ⟨hnlt, _⟩; exact (hnlt complex_satisfies_composite_lt_qubits).elim
  | realHilbert =>
    constructor
    · intro _; exact ⟨real_fails_composite_lt_qubits, fun h => h⟩
    · intro _; rfl
  | quaternionicHilbert =>
    constructor
    · intro _; exact ⟨quat_fails_composite_lt_qubits, fun h => h⟩
    · intro _; rfl

/-- FinL1 classical product host: neither complex phase nor composite LT. -/
inductive HostTag where
  | finL1Product
  | namedLift (L : NamedLift)
  deriving DecidableEq, Repr

def hostHasComplexPhase : HostTag → Prop
  | .finL1Product => False
  | .namedLift L => HasComplexPhaseCarrier L

def hostSatisfiesCompositeLT : HostTag → Prop
  | .finL1Product => False
  | .namedLift L => SatisfiesCompositeLT L 2 2

theorem finL1_host_neither_phase_nor_lt :
    ¬ hostHasComplexPhase .finL1Product ∧
    ¬ hostSatisfiesCompositeLT .finL1Product :=
  ⟨fun h => h, fun h => h⟩

theorem complex_host_both_phase_and_lt :
    hostHasComplexPhase (.namedLift .complexHilbert) ∧
    hostSatisfiesCompositeLT (.namedLift .complexHilbert) :=
  ⟨trivial, complex_satisfies_composite_lt_qubits⟩

inductive IndependenceStatus where
  | independent
  | coupled
  | open
  deriving DecidableEq, Repr

/-- Terminal honesty for `OB-COMPOSE.local_tomography_vs_OB-U1` on the NamedLift registry. -/
def ltVsObU1Status : IndependenceStatus := .coupled

theorem lt_vs_ob_u1_coupled :
    ltVsObU1Status = IndependenceStatus.coupled := rfl

theorem lt_vs_ob_u1_not_independent :
    ltVsObU1Status ≠ IndependenceStatus.independent := by
  decide

/-! ### Residual OPEN: SPLIT-OUTSIDE-REGISTRY

Independence models that live **outside** the NamedLift registry `{ℂ,ℝ,ℍ}`
remain OPEN. Registry COUPLED refuses split *on the named three*; it does
**not** seal absolute couple for every conceivable host.
-/

/-- Residual id for outside-registry split work (not a Wave-6 exit criterion alone). -/
def splitOutsideRegistryStatus : IndependenceStatus := .open

theorem split_outside_registry_open :
    splitOutsideRegistryStatus = IndependenceStatus.open := rfl

theorem split_outside_registry_not_coupled :
    splitOutsideRegistryStatus ≠ IndependenceStatus.coupled := by
  decide

theorem split_outside_registry_not_independent :
    splitOutsideRegistryStatus ≠ IndependenceStatus.independent := by
  decide

/-! ### Exploratory toy: `ExoticHost` (OutsideRegistry, not a NamedLift)

Pure boolean face assignment that *can* XOR-split LT from phase. This is a
**design probe** only: it is **not** a NamedLift, **not** a DeclaredTensor host,
**not** a BASIS independence model, and does **not** discharge
`SPLIT-OUTSIDE-REGISTRY` to `independent`.
-/

/-- Extended host tags: NamedLift registry + FinL1 product + outside-registry exotic. -/
inductive ExtendedHostTag where
  | finL1Product
  | namedLift (L : NamedLift)
  | exoticHost
  deriving DecidableEq, Repr

/-- Mark for hosts outside the three-lift NamedLift registry. -/
def IsOutsideRegistry : ExtendedHostTag → Bool
  | .exoticHost => true
  | .finL1Product => false
  | .namedLift _ => false

theorem exotic_is_outside_registry :
    IsOutsideRegistry .exoticHost = true := rfl

theorem named_lifts_not_outside_registry (L : NamedLift) :
    IsOutsideRegistry (.namedLift L) = false := rfl

theorem finL1_not_outside_registry :
    IsOutsideRegistry .finL1Product = false := rfl

theorem exotic_ne_named_lift (L : NamedLift) :
    ExtendedHostTag.exoticHost ≠ ExtendedHostTag.namedLift L := by
  intro h
  cases h

/-- Exploratory face booleans: LT without complex phase (XOR split toy). -/
def exoticHasComplexPhase : Bool := false
def exoticSatisfiesCompositeLT : Bool := true

theorem exotic_host_xor_split_exploratory :
    exoticSatisfiesCompositeLT = true ∧
    exoticHasComplexPhase = false ∧
    exoticSatisfiesCompositeLT ≠ exoticHasComplexPhase := by
  decide

/-- Honesty level: exploratory XOR is not BASIS independence. -/
inductive ExploratoryClaimLevel where
  | notBasisIndependence
  deriving DecidableEq, Repr

def exoticXorClaimLevel : ExploratoryClaimLevel := .notBasisIndependence

theorem exotic_xor_not_basis_independence :
    exoticXorClaimLevel = ExploratoryClaimLevel.notBasisIndependence := rfl

/-- Exploratory XOR does **not** flip the outside-registry residual to independent. -/
theorem exotic_xor_does_not_discharge_outside_open :
    exoticSatisfiesCompositeLT ≠ exoticHasComplexPhase ∧
    splitOutsideRegistryStatus = IndependenceStatus.open :=
  ⟨by decide, rfl⟩

/-- Residual status table (registry COUPLED; outside OPEN; exotic exploratory). -/
theorem residual_status_table :
    ltVsObU1Status = IndependenceStatus.coupled ∧
    splitOutsideRegistryStatus = IndependenceStatus.open ∧
    exoticXorClaimLevel = ExploratoryClaimLevel.notBasisIndependence ∧
    IsOutsideRegistry .exoticHost = true :=
  ⟨rfl, rfl, rfl, rfl⟩

/-- **COUPLED package (deepened):** biconditional dual + exhaustive no-XOR on
    NamedLift registry + FinL1 neither + residual outside OPEN. -/
theorem lt_ob_u1_coupled_package :
    (∀ L : NamedLift, SatisfiesCompositeLT L 2 2 ↔ HasComplexPhaseCarrier L) ∧
    (∀ L : NamedLift, ¬ IndependentlySplitsLtFromPhase L) ∧
    (∀ L : NamedLift, ¬ XorSplitsLtFromPhase L) ∧
    hostHasComplexPhase (.namedLift .complexHilbert) ∧
    hostSatisfiesCompositeLT (.namedLift .complexHilbert) ∧
    ¬ hostHasComplexPhase .finL1Product ∧
    ¬ hostSatisfiesCompositeLT .finL1Product ∧
    ltVsObU1Status = IndependenceStatus.coupled ∧
    splitOutsideRegistryStatus = IndependenceStatus.open :=
  ⟨lt_iff_complex_phase_on_registry,
    no_registry_model_splits_lt_from_phase,
    no_named_lift_xor_splits_lt_from_phase,
    trivial, complex_satisfies_composite_lt_qubits,
    fun h => h, fun h => h, rfl, rfl⟩

/-! ## BASIS unblocking residual: CoupledImportBundle (`BUNDLE-U1-LT`)

Honest path for W6.19 full-basis packaging **without** XOR independence lie:

On NamedLift the faces co-vary. Treat them as a **single** import-basis slot
`BUNDLE-U1-LT` (drop both together / admit both together). This unblocks a
provisional **B8 design** (= nested B7 + bundle slot) while keeping
`separateObU1RowInIndependenceMatrix = false`.

**Not claimed:** XOR independence of OB-U1 from composite LT; Wave-6 exit;
ExoticHost as BASIS; absolute couple outside registry.
-/

/-- Bundle faces for the coupled phase-carrier / composite-LT pair. -/
structure BundleFaces where
  hasPhaseCarrier : Bool
  satisfiesCompositeLT : Bool
  deriving DecidableEq, Repr

/-- Honest covariance: faces agree (both present or both absent). -/
def bundleCovaries (f : BundleFaces) : Bool :=
  decide (f.hasPhaseCarrier = f.satisfiesCompositeLT)

/-- NamedLift → bundle faces (discrete dual of registry Prop faces). -/
def namedLiftBundleFaces : NamedLift → BundleFaces
  | .complexHilbert => { hasPhaseCarrier := true, satisfiesCompositeLT := true }
  | .realHilbert => { hasPhaseCarrier := false, satisfiesCompositeLT := false }
  | .quaternionicHilbert => { hasPhaseCarrier := false, satisfiesCompositeLT := false }

theorem named_lift_bundle_covaries (L : NamedLift) :
    bundleCovaries (namedLiftBundleFaces L) = true := by
  cases L <;> rfl

theorem complex_bundle_admits_both :
    (namedLiftBundleFaces .complexHilbert).hasPhaseCarrier = true ∧
    (namedLiftBundleFaces .complexHilbert).satisfiesCompositeLT = true := by
  decide

theorem rebit_bundle_admits_neither :
    (namedLiftBundleFaces .realHilbert).hasPhaseCarrier = false ∧
    (namedLiftBundleFaces .realHilbert).satisfiesCompositeLT = false := by
  decide

/-- Drop-exactly-bundle model: both faces absent (single independence slot). -/
def bundleDropModel : BundleFaces :=
  { hasPhaseCarrier := false, satisfiesCompositeLT := false }

/-- Admit-bundle model: both faces present (complex host). -/
def bundleAdmitModel : BundleFaces :=
  { hasPhaseCarrier := true, satisfiesCompositeLT := true }

def failsExactlyBundle (f : BundleFaces) : Bool :=
  decide (f.hasPhaseCarrier = false ∧ f.satisfiesCompositeLT = false)

def admitsBundle (f : BundleFaces) : Bool :=
  decide (f.hasPhaseCarrier = true ∧ f.satisfiesCompositeLT = true)

theorem bundle_drop_fails_exactly :
    failsExactlyBundle bundleDropModel = true ∧
    bundleCovaries bundleDropModel = true := by
  decide

theorem bundle_admit_admits_both :
    admitsBundle bundleAdmitModel = true ∧
    bundleCovaries bundleAdmitModel = true := by
  decide

/-- Illegal one-sided models (XOR) are **not** bundle-honest. -/
def illegalXorLtWithoutPhase : BundleFaces :=
  { hasPhaseCarrier := false, satisfiesCompositeLT := true }

def illegalXorPhaseWithoutLt : BundleFaces :=
  { hasPhaseCarrier := true, satisfiesCompositeLT := false }

theorem illegal_xor_not_bundle_covariant :
    bundleCovaries illegalXorLtWithoutPhase = false ∧
    bundleCovaries illegalXorPhaseWithoutLt = false := by
  decide

/-- BASIS design IDs (W6.19 handoff; packaging only). -/
def basisBundleSlotId : String := "BUNDLE-U1-LT"
/-- Nested B7 (from W6.19) + one coupled bundle slot. -/
def provisionalB8DesignCard : Nat := 8
/-- Separate OB-U1 row remains forbidden in the independence matrix. -/
def separateObU1RowInIndependenceMatrix : Bool := false
/-- Bundle slot is legal for BASIS packaging. -/
def bundleSlotAdmittedToBasisDesign : Bool := true

theorem basis_unblock_via_coupled_bundle :
    basisBundleSlotId = "BUNDLE-U1-LT" ∧
    provisionalB8DesignCard = 8 ∧
    separateObU1RowInIndependenceMatrix = false ∧
    bundleSlotAdmittedToBasisDesign = true ∧
    failsExactlyBundle bundleDropModel = true ∧
    admitsBundle bundleAdmitModel = true ∧
    (∀ L : NamedLift, bundleCovaries (namedLiftBundleFaces L) = true) ∧
    ltVsObU1Status = IndependenceStatus.coupled ∧
    splitOutsideRegistryStatus = IndependenceStatus.open ∧
    exoticXorClaimLevel = ExploratoryClaimLevel.notBasisIndependence :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl, named_lift_bundle_covaries, rfl, rfl, rfl⟩

/-- **BUNDLE package:** registry COUPLED + bundle drop/admit + B8 design handoff. -/
theorem coupled_import_bundle_package :
    basisBundleSlotId = "BUNDLE-U1-LT" ∧
    provisionalB8DesignCard = 8 ∧
    separateObU1RowInIndependenceMatrix = false ∧
    failsExactlyBundle bundleDropModel = true ∧
    admitsBundle bundleAdmitModel = true ∧
    bundleCovaries illegalXorLtWithoutPhase = false ∧
    failsExactlyBundle illegalXorLtWithoutPhase = false ∧
    admitsBundle illegalXorLtWithoutPhase = false ∧
    ltVsObU1Status = IndependenceStatus.coupled ∧
    splitOutsideRegistryStatus = IndependenceStatus.open := by
  decide

/-! ## SPLIT-OUTSIDE-REGISTRY residual deepen (outside XOR witnesses)

Honest deepen of the outside-registry residual:

1. **NamedLift XOR remains REFUSED** (no uncouple on registry).
2. **Outside-registry XOR face witnesses exist** as structured tags
   (not pure anonymous booleans alone): LT-without-phase and
   phase-without-LT hosts live outside NamedLift.
3. Existence of XOR witnesses does **not** discharge
   `SPLIT-OUTSIDE-REGISTRY` to `independent` — BASIS admission criteria
   (tensor host not NamedLift + admitted independence row) remain unmet.
4. Absolute couple outside registry is still **not** claimed.
-/

/-- Structured outside-registry host tags (not NamedLift constructors). -/
inductive OutsideRegistryHost where
  | ltWithoutPhase
  | phaseWithoutLt
  | bothAbsent
  deriving DecidableEq, Repr

def outsideHasPhase : OutsideRegistryHost → Bool
  | .ltWithoutPhase => false
  | .phaseWithoutLt => true
  | .bothAbsent => false

def outsideHasCompositeLT : OutsideRegistryHost → Bool
  | .ltWithoutPhase => true
  | .phaseWithoutLt => false
  | .bothAbsent => false

/-- XOR face split on an outside-registry host. -/
def outsideXorFaces (h : OutsideRegistryHost) : Bool :=
  decide (outsideHasPhase h ≠ outsideHasCompositeLT h)

theorem outside_registry_xor_witnesses_exist :
    outsideXorFaces .ltWithoutPhase = true ∧
    outsideXorFaces .phaseWithoutLt = true ∧
    outsideXorFaces .bothAbsent = false ∧
    outsideHasCompositeLT .ltWithoutPhase = true ∧
    outsideHasPhase .ltWithoutPhase = false ∧
    outsideHasPhase .phaseWithoutLt = true ∧
    outsideHasCompositeLT .phaseWithoutLt = false := by
  decide

/-- Every outside host is not a NamedLift constructor (type-level fence). -/
theorem outside_hosts_not_named_lift_constructors :
    OutsideRegistryHost.ltWithoutPhase ≠
      OutsideRegistryHost.phaseWithoutLt ∧
    OutsideRegistryHost.phaseWithoutLt ≠
      OutsideRegistryHost.bothAbsent := by
  decide

/-- Discharge criteria for flipping residual to independent (ledger). -/
structure SplitOutsideDischargeCriteria where
  /-- DeclaredTensor (or equivalent) host outside NamedLift registry. -/
  hasTensorHostNotNamedLift : Bool
  /-- Structured XOR face witnesses exist outside registry. -/
  hasXorFaceWitness : Bool
  /-- Admitted as BASIS independence row (not exploratory). -/
  admitsToBasisIndependence : Bool
  /-- NamedLift XOR remains refused (must stay true). -/
  namedLiftXorRefused : Bool
  /-- Residual status flipped to independent. -/
  residualStatusIndependent : Bool
  deriving DecidableEq, Repr

def splitOutsideDischargeCriteria : SplitOutsideDischargeCriteria :=
  { hasTensorHostNotNamedLift := false
    hasXorFaceWitness := true
    admitsToBasisIndependence := false
    namedLiftXorRefused := true
    residualStatusIndependent := false }

theorem split_outside_not_discharged :
    splitOutsideDischargeCriteria.hasXorFaceWitness = true ∧
    splitOutsideDischargeCriteria.hasTensorHostNotNamedLift = false ∧
    splitOutsideDischargeCriteria.admitsToBasisIndependence = false ∧
    splitOutsideDischargeCriteria.namedLiftXorRefused = true ∧
    splitOutsideDischargeCriteria.residualStatusIndependent = false ∧
    splitOutsideRegistryStatus = IndependenceStatus.open ∧
    ltVsObU1Status = IndependenceStatus.coupled := by
  decide

/-- NamedLift still has no XOR (reaffirm refuse uncouple). -/
theorem named_lift_xor_still_refused :
    (∀ L : NamedLift, ¬ XorSplitsLtFromPhase L) ∧
    splitOutsideDischargeCriteria.namedLiftXorRefused = true ∧
    separateObU1RowInIndependenceMatrix = false :=
  ⟨no_named_lift_xor_splits_lt_from_phase, rfl, rfl⟩

/-- SPLIT-OUTSIDE residual deepen package. -/
theorem split_outside_registry_deepen_package :
    outsideXorFaces .ltWithoutPhase = true ∧
    outsideXorFaces .phaseWithoutLt = true ∧
    splitOutsideDischargeCriteria.hasXorFaceWitness = true ∧
    splitOutsideDischargeCriteria.admitsToBasisIndependence = false ∧
    splitOutsideDischargeCriteria.residualStatusIndependent = false ∧
    splitOutsideRegistryStatus = IndependenceStatus.open ∧
    ltVsObU1Status = IndependenceStatus.coupled ∧
    separateObU1RowInIndependenceMatrix = false ∧
    exoticXorClaimLevel = ExploratoryClaimLevel.notBasisIndependence ∧
    (∀ L : NamedLift, ¬ IndependentlySplitsLtFromPhase L) :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl,
    no_registry_model_splits_lt_from_phase⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

/-! ## Typed monoidal structure (W6.14 structural half)

The `Nat` statements earlier in this file are dimension bookkeeping. This section
states the monoidal laws about **actual matrices whose source and target index
types are declared**, so a wrong index convention fails rather than being absorbed
by `ring`.

The arrow map is the Kronecker product. The object map is the product of index
types, which keeps the tensor structure explicit instead of flattening to `Fin n`.

Mirrors the executable Rust surface in
`omega_engine/crates/omega_quantum_physics/src/composition_tomography.rs`
(`tensor_morphisms`, `identity_is_preserved`, `interchange_law_holds`,
`associativity_on_morphisms`).

AuthorityEffect: None. -/

section TypedMonoidal

open Matrix
open scoped Kronecker

/-- A typed finite morphism: a matrix together with declared source and target
index types. The types *are* the dimension declaration. -/
structure TypedMor (S T : Type) [Fintype S] [Fintype T] where
  mat : Matrix T S ℚ

namespace TypedMor

variable {S T U S' T' U' : Type}
  [Fintype S] [Fintype T] [Fintype U] [Fintype S'] [Fintype T'] [Fintype U']

/-- Arrow map of the composition functor. -/
def tensor (f : TypedMor S T) (g : TypedMor S' T') : TypedMor (S × S') (T × T') :=
  ⟨f.mat ⊗ₖ g.mat⟩

/-- Composition of typed morphisms. -/
def comp (g : TypedMor T U) (f : TypedMor S T) : TypedMor S U :=
  ⟨g.mat * f.mat⟩

/-- The typed identity. -/
def id' (S : Type) [Fintype S] [DecidableEq S] : TypedMor S S := ⟨1⟩

/-- **Object dimension law**: the tensor of index types multiplies cardinalities.
Unlike `productSectorCount`, this is a statement about the actual object map. -/
theorem tensor_card (S S' : Type) [Fintype S] [Fintype S'] :
    Fintype.card (S × S') = Fintype.card S * Fintype.card S' :=
  Fintype.card_prod S S'

/-- **Functor law (unit)**: identities are preserved. -/
theorem tensor_id (S S' : Type) [Fintype S] [DecidableEq S] [Fintype S']
    [DecidableEq S'] :
    (id' S).tensor (id' S') = id' (S × S') := by
  simp [tensor, id', Matrix.one_kronecker_one]

/-- **Functor law (interchange / bifunctoriality)**:
`(g ∘ f) ⊗ (g' ∘ f') = (g ⊗ g') ∘ (f ⊗ f')`.

This is the law that makes `⊗` a functor on the product category. It is a genuine
matrix identity — it fails for a wrong index convention, which `ring` on `Nat`
cannot detect. -/
theorem tensor_comp (g : TypedMor T U) (f : TypedMor S T)
    (g' : TypedMor T' U') (f' : TypedMor S' T') :
    (g.comp f).tensor (g'.comp f') = (g.tensor g').comp (f.tensor f') := by
  simp [tensor, comp, Matrix.mul_kronecker_mul]

/-- **Associativity under an explicit canonical identification.**

`(f ⊗ g) ⊗ h` and `f ⊗ (g ⊗ h)` live on `(S × S') × S''` and `S × (S' × S'')`
respectively — *different* types. They are equal only after the canonical
reindexing `Equiv.prodAssoc`, which is named here rather than hidden. -/
theorem tensor_assoc (f : TypedMor S T) (g : TypedMor S' T') (h : TypedMor U U') :
    Matrix.submatrix ((f.tensor g).tensor h).mat
        (Equiv.prodAssoc T T' U').symm (Equiv.prodAssoc S S' U).symm
      = (f.tensor (g.tensor h)).mat := by
  simp [tensor, Matrix.kronecker_assoc']

end TypedMor

/-! ### Dimension-mismatch refusal

Composition of typed morphisms is only defined when the intermediate index types
agree. At the type level a mismatch is a *type error*, so the refusal is checked
by the elaborator. For the runtime/declared-dimension surface the refusal must be
explicit, which is what `DeclaredComp` records. -/

/-- A declared composition request with runtime dimensions. -/
structure DeclaredComp where
  srcDim : Nat
  midOut : Nat
  midIn : Nat
  tgtDim : Nat
deriving DecidableEq, Repr

/-- A request composes only when the intermediate dimensions agree. -/
def DeclaredComp.admissible (c : DeclaredComp) : Bool := c.midOut == c.midIn

/-- **Refusal is reachable**: a mismatched request is rejected, so the gate can
fail. A predicate that accepted everything would be no gate at all. -/
theorem declared_comp_refuses_mismatch :
    (DeclaredComp.mk 2 3 4 5).admissible = false := by decide

theorem declared_comp_accepts_match :
    (DeclaredComp.mk 2 3 3 5).admissible = true := by decide

end TypedMonoidal

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ComposeMonoidal
end QM

#print axioms QM.ComposeMonoidal.product_ne_sum_bit2x3
#print axioms QM.ComposeMonoidal.mixed_has_no_pure_classical_purification
#print axioms QM.ComposeMonoidal.complex_local_tomography_dim
#print axioms QM.ComposeMonoidal.fairBit_no_classical_purification
#print axioms QM.ComposeMonoidal.fairBit_classical_vs_lift_purification_split
#print axioms QM.ComposeMonoidal.declared_tensor_requires_named_lift
#print axioms QM.ComposeMonoidal.finL1_product_does_not_force_complex_lt
#print axioms QM.ComposeMonoidal.only_complex_among_three_satisfies_lt_qubits
#print axioms QM.ComposeMonoidal.lt_ob_u1_coupled_package
#print axioms QM.ComposeMonoidal.no_named_lift_xor_registry_scan
#print axioms QM.ComposeMonoidal.residual_status_table
#print axioms QM.ComposeMonoidal.exotic_xor_does_not_discharge_outside_open
#print axioms QM.ComposeMonoidal.split_outside_registry_deepen_package
#print axioms QM.ComposeMonoidal.named_lift_xor_still_refused
#print axioms QM.ComposeMonoidal.structure_not_auth
#print axioms QM.ComposeMonoidal.TypedMor.tensor_id
#print axioms QM.ComposeMonoidal.TypedMor.tensor_comp
#print axioms QM.ComposeMonoidal.TypedMor.tensor_assoc
#print axioms QM.ComposeMonoidal.TypedMor.tensor_card
#print axioms QM.ComposeMonoidal.declared_comp_refuses_mismatch
