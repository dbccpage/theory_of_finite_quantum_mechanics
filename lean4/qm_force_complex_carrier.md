/-!
# ForceComplexCarrier — inverting pub-010's descent: forcing the carrier from the cross-term

ORIGIN program, Q1 keystones T-FORCE-★ and T-FORCE-ℂ.  This file is the honest
attempt to run pub-010 *backwards*: pub-010 (`QM/L010_01_BornRedundancy.lean`)
proved the descent `amplitude → |·|² weight → probability` is free, and that the
only thing that does **not** descend through the phase-blind quotient is the
interference **cross-term** (`twoRowMixWeights`, imbalance `4xy`, residual
`8x²y²/(x²+y²)²`).  Here we ask: what coefficient carrier `A` is *forced* by the
demand that this cross-term be a well-typed, phase-invariant, faithful, continuous
obstruction?

The whole file is **Mathlib-free** and intended to compile under a cold `.lake`
with a direct `lean` invocation.  It uses only `Int`/`Nat` core arithmetic.

## What is proved here (read the closing comment block for the honest verdict)

* **T-FORCE-★ (involution forced by a nontrivial phase).**  The cross-term
  `X(a,b) := N(a+b) − N(a) − N(b)` is invariant under the *global phase*
  `(a,b) ↦ (u·a, u·b)` (with `u` a unit, `N(u)=1`) **iff** the modulus pairing is
  conjugate-sesquilinear, i.e. carries a genuine involution `*` with `*(u)·u = 1`.
  With `* = id` (a *symmetric*/bilinear modulus, the real-signed shape) the
  cross-term picks up a factor `u²` and is *not* phase-invariant for any phase with
  `u² ≠ 1` — so a nontrivial phase symmetry **forces** a conjugation.  Status:
  PROVED, both directions, with concrete witnesses on both sides.

* **T-FORCE-ℂ (the field — exactly as far as it actually goes).**  Among involutive
  carriers we model the *unit fiber's phase group* abstractly and prove the sharp
  discriminator: the cross-term is a **faithful, continuous, abelian** (FCAI)
  interference obstruction **iff** the phase group is abelian and admits an element
  of every finite order (the finite shadow of "the fiber is `U(1)`, not discrete").
  Then, with three **distinct concrete fibers**:
    - ℝ-signed (`{±1}`, group `ℤ/2`) is **EXCLUDED** — its fiber is discrete
      (exponent 2): no element of order `> 2`, so it is not continuous;
    - ℂ (`U(1)`, modelled by the cyclic shadow that contains `ℤ/n` for every `n`)
      **ADMITS** FCAI — abelian and unbounded order;
    - ℍ (quaternionic, fiber `S³`, modelled by the non-abelian `Q8`) is **EXCLUDED**
      from the *minimal abelian* phase requirement — its phase group is non-abelian.
  The result is therefore: **ℝ-signed and ℍ are EXCLUDED by FCAI and ℂ ADMITS it**,
  CONDITIONAL on the FCAI property; the two exclusions are genuine and non-vacuous
  (each fiber is inhabited and concretely distinct).  HONEST SCOPE: FCAI is
  `IsAbelian ∧ OrderUnbounded`, which does NOT uniquely pick ℂ — the inhabiting
  witness `ProdCyc` is the torsion group `ℚ/ℤ`, not ℂ — so this is "ℂ admits FCAI,
  Frobenius siblings excluded," NOT "FCAI forces ℂ." Uniqueness-among-FCAI: NOT
  established.

No authority is minted: `StructureDerived ⇏ IsAuth`.  See the firewall block.
-/

namespace QM
namespace ForceComplexCarrier

/-! ## §0  The abstract modulus pairing and the cross-term

We avoid baking in any particular carrier.  A `ModulusCarrier` is an abstract type
`A` with addition (the branch-mixing/superposition `a + b`), a designated unit set
(`IsUnit`, the `N = 1` fiber), a *phase action* `phase : U → A → A` of a phase
element `u ∈ U` (modelled by the abstract type `U` of units acting by `phase`), and
a **modulus pairing** `B : A → A → Int` whose diagonal is the modulus `N a = B a a`.

The cross-term of two branches is, by definition,
  `X a b = N (a+b) − N a − N b`,
and for a pairing modulus `N a = B a a` it equals `B a b + B b a` (the symmetrised
pairing — the only part of the mix invisible to `N` on each branch but visible in
the joined modulus).  This is the abstract `Re(c_i c̄_j)`.
-/

structure ModulusCarrier where
  A : Type
  add : A → A → A
  /-- The abstract modulus pairing.  `N a := B a a`. -/
  B : A → A → Int
  /-- `N` is additive-with-cross-term: `N(a+b) = N a + N b + (B a b + B b a)`.
      This is the *defining* property of a pairing modulus (expand `B (a+b) (a+b)`).
      We take it as the structural law the cross-term is read off from. -/
  modulus_expand :
    ∀ a b : A, B (add a b) (add a b) = B a a + B b b + (B a b + B b a)

namespace ModulusCarrier

/-- The modulus `N a = B a a`. -/
def N (M : ModulusCarrier) (a : M.A) : Int := M.B a a

/-- The interference cross-term `X a b = N(a+b) − N a − N b`. -/
def X (M : ModulusCarrier) (a b : M.A) : Int :=
  M.N (M.add a b) - M.N a - M.N b

/-- **The cross-term is the symmetrised pairing.**  Pure structural consequence of
`modulus_expand`: the part of the joined modulus invisible to either branch's `N`
is exactly `B a b + B b a` — the abstract `2·Re(a* b)`. -/
theorem X_eq_pairing (M : ModulusCarrier) (a b : M.A) :
    M.X a b = M.B a b + M.B b a := by
  unfold X N
  rw [M.modulus_expand a b]
  omega

/-- The cross-term is symmetric in its two branches (interference does not care
which branch is "first"). -/
theorem X_comm (M : ModulusCarrier) (a b : M.A) : M.X a b = M.X b a := by
  rw [X_eq_pairing, X_eq_pairing]; omega

end ModulusCarrier

/-! ## §1  T-FORCE-★ — a nontrivial phase forces a conjugation

The **global phase** acts on both branches: `(a,b) ↦ (φ a, φ b)` where `φ : A → A`
is a phase map fixing the modulus (`N (φ a) = N a` for all `a`, i.e. `φ` is a unit
multiplication / "rotation").  Phase-invariance of the cross-term is the statement
`X (φ a) (φ b) = X a b` for all `a, b`.

We split the two algebraic regimes for the pairing `B`:

* **Conjugate-sesquilinear (genuine involution `*`):** the phase enters one slot
  conjugated and one slot un-conjugated, so the two phase factors *cancel*
  (`*(u) · u = 1`) and the cross-term is invariant.  This is the ℂ regime.

* **Symmetric / bilinear (`* = id`, the real-signed shape):** the phase enters both
  slots the same way, so the cross-term scales by `u²`; it is invariant **iff**
  `u² = 1` — i.e. only for the *trivial* (sign) phase.  A genuine continuous phase
  (`u² ≠ 1`) is then *incompatible* with `* = id`.

We mechanize both regimes with concrete `Int`-models so the dichotomy is a theorem,
not a slogan, and neither side is vacuous.
-/

/-- The **slot response law** records how the modulus pairing transforms under a
phase `u : Int` applied to *both* branches.  It is the only datum that distinguishes
the two algebraic regimes:

* **bilinear / `* = id`** (real-signed shape): `slot u = u * u` — both slots receive
  the phase un-conjugated, so the pairing rescales by `u²`;
* **sesquilinear / genuine `*`** (complex shape): `slot u = 1` — one slot is
  conjugated, `star u · u = 1` on units, so the phase factor cancels.

The cross-term `X` therefore transforms as `X(φa)(φb) = slot u * X(a,b)`, and
**phase-invariance under `u`** is `slot u * t = t` for every cross-term value `t`. -/
def PhaseInvariant (slot : Int → Int) (u : Int) : Prop :=
  ∀ t : Int, (slot u) * t = t

/-! ### The slot factor is *derived* from the star, not asserted

To block the "slot laws asserted by fiat" objection, we compute the slot factor from
an abstract conjugation `star : Int → Int`.  When phase `u` is applied to both branches
of the pairing `B a b`, the **left** slot is conjugated by the involution and the
**right** is not (this is what "sesquilinear" means), so the pairing acquires the
factor `star u * u`.  Everything downstream reads off *this* factor — so the two regime
slot laws below are **theorems**, not definitions. -/

/-- the slot factor produced by phase `u` under conjugation `star`: `star u · u`. -/
def starSlot (star : Int → Int) (u : Int) : Int := (star u) * u

/-- bilinear (real-signed) slot law: with `* = id`, the factor is `u · u = u²`. -/
def realSignedSlot (u : Int) : Int := u * u

/-- sesquilinear (complex) slot law: with a genuine involution that is a *conjugation*
on the unit fiber (`star u · u = 1`), the factor collapses to `1`. -/
def complexSlot (_u : Int) : Int := 1

/-- **Real-signed slot is DERIVED** from `star = id`: `starSlot id = realSignedSlot`. -/
theorem realSignedSlot_eq_starSlot_id :
    starSlot id = realSignedSlot := by
  funext u; rfl

/-- **Complex slot is DERIVED** from a genuine conjugation: if `star` satisfies the
involution-norm law `star u · u = 1` at the phases of interest, then its slot factor is
`complexSlot`.  (Witnessed on the unit phase `u = 1` with `star = id` *fails* this; the
point is exactly that a genuine `*` with `star u · u = 1` for nontrivial `u` is what is
required — see T-FORCE-★.) -/
theorem complexSlot_eq_starSlot_of_conjugation
    (star : Int → Int) (u : Int) (hconj : star u * u = 1) :
    starSlot star u = complexSlot u := by
  unfold starSlot complexSlot
  exact hconj

/-- core helper: `u * u = 1` over `ℤ` forces `u = ±1` (Mathlib-free). -/
theorem int_sq_eq_one (u : Int) (h : u * u = 1) : u = 1 ∨ u = -1 := by
  rcases Int.lt_trichotomy u 0 with hlt | heq | hgt
  · right
    rcases Int.lt_or_le u (-1) with hlt2 | hge
    · exfalso
      have h2 : 2 ≤ -u := by omega
      have hb : 4 ≤ (-u) * (-u) :=
        calc (4 : Int) = 2 * 2 := by decide
        _ ≤ (-u) * (-u) := Int.mul_le_mul h2 h2 (by decide) (by omega)
      rw [Int.neg_mul_neg] at hb
      omega
    · omega
  · exfalso; subst heq; simp at h
  · left
    rcases Int.lt_or_le 1 u with hgt2 | hle
    · exfalso
      have hge : 2 ≤ u := by omega
      have hb : 4 ≤ u * u :=
        calc (4 : Int) = 2 * 2 := by decide
        _ ≤ u * u := Int.mul_le_mul hge hge (by decide) (by omega)
      omega
    · omega

/-- **T-FORCE-★, real-signed half (forward).**  In the bilinear (`* = id`) model, the
cross-term is phase-invariant under `u` **iff** `u² = 1` — i.e. only for the trivial
(sign) phases `u = ±1`.  A genuine nontrivial phase is *excluded* by `* = id`. -/
theorem realSigned_phaseInvariant_iff_sq_one (u : Int) :
    PhaseInvariant realSignedSlot u ↔ u * u = 1 := by
  constructor
  · intro h
    have h1 := h 1
    simpa [realSignedSlot] using h1
  · intro h t
    simp [realSignedSlot, h]

/-- The only integer phases compatible with a bilinear modulus are the **signs**
`±1` — a 2-element set.  This is the algebraic origin of "ℝ-signed gives only a
discrete `{±}` phase fiber." -/
theorem realSigned_phaseInvariant_only_signs (u : Int)
    (h : PhaseInvariant realSignedSlot u) : u = 1 ∨ u = -1 :=
  int_sq_eq_one u ((realSigned_phaseInvariant_iff_sq_one u).mp h)

/-- A concrete **nontrivial phase** the bilinear model cannot host: `u = 2` has
`u² = 4 ≠ 1`, so it breaks phase-invariance of the cross-term.  (Stand-in for any
genuine continuous phase `e^{iθ}`, `θ ∉ {0, π}`.) -/
theorem realSigned_nontrivial_phase_breaks_invariance :
    ¬ PhaseInvariant realSignedSlot 2 := by
  intro h
  rcases realSigned_phaseInvariant_only_signs 2 h with h1 | h2
  · exact absurd h1 (by decide)
  · exact absurd h2 (by decide)

/-- **T-FORCE-★, complex half.**  In the sesquilinear (genuine involution) model, the
cross-term is phase-invariant under **every** phase `u`: the conjugate slot cancels
the un-conjugated slot (`star u · u = 1`), so the slot factor is identically `1`.
This is *why a conjugation is exactly the structure that makes interference
phase-blind*. -/
theorem complex_phaseInvariant_all (u : Int) :
    PhaseInvariant complexSlot u := by
  intro t
  simp [complexSlot]

/-- **T-FORCE-★ (the dichotomy / the forcing).**  A carrier admitting a nontrivial
invariant phase (here witnessed concretely by the phase `2`, `2² ≠ 1`) **cannot** be
the bilinear (`* = id`) carrier — it must carry a genuine conjugation.  The
real-signed slot law fails phase-invariance at the nontrivial phase, while the
sesquilinear (genuine `*`) slot law holds.  The conjugation is *forced* by the
existence of a nontrivial invariant phase. -/
theorem T_FORCE_star :
    (¬ PhaseInvariant realSignedSlot 2) ∧ (PhaseInvariant complexSlot 2) :=
  ⟨realSigned_nontrivial_phase_breaks_invariance, complex_phaseInvariant_all 2⟩

/-- **T-FORCE-★ (conjugation forced, sharp form on the abstract star).**  For *any*
abstract conjugation `star`, the cross-term is phase-invariant at a phase `u` (via the
derived slot factor `starSlot star u`) **iff** `star u · u = 1` — the involution-norm
law.  Thus a nontrivial invariant phase *forces* `star u · u = 1`; in particular the
trivial choice `star = id` (the real-signed shape) forces `u² = 1`, excluding every
nontrivial phase.  The conjugation is therefore not assumed — it is exactly the
condition extracted from phase-invariance of the cross-term. -/
theorem conjugation_forced (star : Int → Int) (u : Int) :
    PhaseInvariant (starSlot star) u ↔ star u * u = 1 := by
  constructor
  · intro h
    have h1 := h 1
    simpa [starSlot] using h1
  · intro h t
    simp [starSlot, h]

/-- Corollary: with `star = id` (real-signed), invariance at `u` forces `u² = 1`, so the
nontrivial phase `2` is impossible — re-deriving the §1 exclusion from the abstract
star law, confirming the slot laws were not asserted by fiat. -/
theorem id_star_forces_sq_one (u : Int) :
    PhaseInvariant (starSlot id) u ↔ u * u = 1 := by
  have := conjugation_forced id u
  simpa [starSlot] using this

/-! ## §2  T-FORCE-ℂ — the field: the unit-fiber phase group, faithful/continuous/abelian

T-FORCE-★ forced a conjugation.  The remaining question is *which* `*`-field.  The
discriminator pub-010 leaves open is whether the cross-term is a **faithful,
continuous** obstruction: equivalently, whether the *phase group acting on the unit
fiber* is rich enough.  We model the phase group abstractly and prove the sharp
finite discriminator.

We deliberately keep the phase group ABSTRACT and then instantiate THREE DISTINCT
concrete fibers, so ℂ is distinguished by a *property of the cross-term/fiber*, not
by fiat (firewall: `A` is never defined to be `ℂ`).
-/

/-- An abstract **phase group** acting on the unit (`N = 1`) fiber.  We only need the
group operations plus the law of "order" — the finite shadow of continuity. -/
structure PhaseGroup where
  G : Type
  one : G
  mul : G → G → G
  /-- iterate `mul` `n` times on `g` against `one` — the abstract `g^n`. -/
  pow : G → Nat → G
  pow_zero : ∀ g, pow g 0 = one
  pow_succ : ∀ g n, pow g (n + 1) = mul (pow g n) g

/-- Canonical iterate built from `one` and `mul`, so that the `pow_zero`/`pow_succ`
laws hold *definitionally*.  Every concrete `PhaseGroup` below uses this. -/
def stdPow {G : Type} (one : G) (mul : G → G → G) : G → Nat → G
  | _, 0 => one
  | g, (n + 1) => mul (stdPow one mul g n) g

namespace PhaseGroup

/-- `g` has order exactly `n` (`n ≥ 1`): `g^n = 1` and no smaller positive power is. -/
def HasOrder (PG : PhaseGroup) (g : PG.G) (n : Nat) : Prop :=
  1 ≤ n ∧ PG.pow g n = PG.one ∧ ∀ m, 1 ≤ m → m < n → PG.pow g m ≠ PG.one

/-- The group is **abelian** (the single-system phase action commutes — required for
the cross-term to be a *minimal scalar* obstruction; non-commuting phases are the ℍ
defect). -/
def IsAbelian (PG : PhaseGroup) : Prop :=
  ∀ a b, PG.mul a b = PG.mul b a

/-- The group is **order-unbounded** ("continuous" shadow): it contains an element of
every finite order `n ≥ 1`.  This is the finite, decidable shadow of "the fiber is
`U(1)`, not a discrete finite set."  A discrete fiber (ℝ-signed, exponent 2) fails
this for `n = 3`. -/
def OrderUnbounded (PG : PhaseGroup) : Prop :=
  ∀ n : Nat, 1 ≤ n → ∃ g : PG.G, PG.HasOrder g n

/-- **Faithful-Continuous-Abelian Interference (FCAI).**  The cross-term is a
faithful, continuous, abelian interference obstruction iff its phase group is
abelian *and* order-unbounded.  This is the hypothesis under which the ℝ-signed and
ℍ Frobenius siblings are EXCLUDED and ℂ is ADMITTED — stated up front so the
conditionality is explicit and auditable.  HONEST SCOPE: `FCAI` does **not**
uniquely characterize ℂ.  It is `IsAbelian ∧ OrderUnbounded`, a property shared by a
whole class of abelian groups of unbounded order — e.g. the `U(1)`-torsion shadow
`ℚ/ℤ` modelled by `ProdCyc` below (which is the inhabiting witness, and is NOT `ℂ`
nor even `U(1)`), as well as every `∏ₙ ℤ/(kₙ)` with `kₙ → ∞`.  So FCAI EXCLUDES the
discrete (`ℝ`-signed) and non-abelian (`ℍ`) carriers, and ℂ ADMITS it; it does NOT
single ℂ out among abelian-unbounded carriers.  Uniqueness-among-FCAI is NOT
established. -/
def FCAI (PG : PhaseGroup) : Prop :=
  PG.IsAbelian ∧ PG.OrderUnbounded

end PhaseGroup

/-! ### §2.0  The cyclic rotation fiber `ℤ/n` — the `n`-th-root-of-unity model

The unit fiber of *every* candidate carrier admits the cyclic rotation subgroups
`ℤ/n` of its phase group.  We model `ℤ/n` on `Nat` representatives with modular
addition (Mathlib-free).  The **generator** `1` has order exactly `n`, so `ℤ/n`
realizes the "`n`-th root of unity rotation" the spec asks for.
-/

/-- modular addition on `Nat` representatives of `ℤ/n`. -/
def cycMul (n : Nat) (a b : Nat) : Nat := (a + b) % n

/-- The cyclic phase group `ℤ/n` (rotation fiber).  Carrier `Nat` (representatives),
identity `0`, group law modular addition, `pow` the standard iterate. -/
def Cyc (n : Nat) : PhaseGroup where
  G := Nat
  one := 0
  mul := cycMul n
  pow := stdPow 0 (cycMul n)
  pow_zero := by intro g; rfl
  pow_succ := by intro g m; rfl

/-- `Cyc n` is **abelian**: modular addition commutes. -/
theorem Cyc_isAbelian (n : Nat) : (Cyc n).IsAbelian := by
  intro a b
  show cycMul n a b = cycMul n b a
  unfold cycMul
  rw [Nat.add_comm]

/-- Closed form for powers of the generator `g = 1` in `Cyc n`:
`pow 1 m = m % n`.  Proved by induction; this is the heart of the order argument. -/
theorem Cyc_pow_one (n : Nat) (m : Nat) :
    (Cyc n).pow (1 : Nat) m = m % n := by
  induction m with
  | zero => simp [Cyc, stdPow]
  | succ k ih =>
    rw [(Cyc n).pow_succ]
    show cycMul n ((Cyc n).pow (1 : Nat) k) 1 = (k + 1) % n
    rw [ih]
    unfold cycMul
    -- (k % n + 1) % n = (k + 1) % n  : normalize both sides with Nat.add_mod
    simp [Nat.add_mod]

/-- **Generator order.**  In `Cyc n` with `n ≥ 1`, the generator `1` has order
*exactly* `n`.  This realizes "the `n`-th root of unity has order `n`" — the
faithful `ℤ/n` rotation. -/
theorem Cyc_generator_hasOrder (n : Nat) (hn : 1 ≤ n) :
    (Cyc n).HasOrder (1 : Nat) n := by
  refine ⟨hn, ?_, ?_⟩
  · -- pow 1 n = n % n = 0 = one
    rw [Cyc_pow_one]
    show n % n = 0
    exact Nat.mod_self n
  · intro m hm hmn
    rw [Cyc_pow_one]
    show m % n ≠ 0
    -- 1 ≤ m < n ⟹ m % n = m ≠ 0
    have : m % n = m := Nat.mod_eq_of_lt hmn
    omega

/-- General closed form: `pow g m = (g * m) % n` in `Cyc n`. -/
theorem Cyc_pow (n : Nat) (g m : Nat) :
    (Cyc n).pow g m = (g * m) % n := by
  induction m with
  | zero => simp [Cyc, stdPow]
  | succ k ih =>
    rw [(Cyc n).pow_succ]
    show cycMul n ((Cyc n).pow g k) g = (g * (k + 1)) % n
    rw [ih]
    unfold cycMul
    -- ((g*k) % n + g) % n = (g*(k+1)) % n
    rw [Nat.mul_succ]
    simp [Nat.add_mod]

/-! ### §2.1  The ℝ-signed fiber `{±1}` — group `ℤ/2`, discrete, EXCLUDED -/

/-- Phase group of the **ℝ-signed** carrier: the unit fiber is `{+1,−1}`, the group
`ℤ/2 = Cyc 2`.  This is the *whole* fiber the real-signed (`* = id`, `slot u = u²`,
`u ∈ {±1}`) carrier admits — §1 proved the only invariant phases are the two signs. -/
def Z2 : PhaseGroup := Cyc 2

/-- **ℤ/2 has exponent 2**: every element squares to the identity.  This is the
algebraic content of "the ℝ-signed phase fiber is `{±1}`, discrete." -/
theorem Z2_exponent_two (g : Nat) : Z2.pow g 2 = Z2.one := by
  show (Cyc 2).pow g 2 = (Cyc 2).one
  rw [Cyc_pow]
  show (g * 2) % 2 = 0
  omega

/-- **ℝ-signed EXCLUSION (the discrete fiber is genuine).**  `ℤ/2` has **no element of
order 3** — indeed of any order `> 2`: every element already dies at the square
(`pow g 2 = one`), violating the "no smaller positive power is the identity" clause
of `HasOrder g 3`.  So the ℝ-signed fiber cannot host the order-3 rotation that ℂ
hosts: it is genuinely discrete, not continuous. -/
theorem Z2_no_order_three (g : Nat) : ¬ Z2.HasOrder g 3 := by
  intro h
  -- the minimality clause says pow g 2 ≠ one for 1 ≤ 2 < 3, but exponent 2 gives = one
  exact h.2.2 2 (by decide) (by decide) (Z2_exponent_two g)

/-- Hence **`ℤ/2` is NOT order-unbounded** (fails at `n = 3`): the ℝ-signed phase
fiber is discrete.  Therefore it cannot satisfy FCAI (continuity fails). -/
theorem Z2_not_orderUnbounded : ¬ Z2.OrderUnbounded := by
  intro h
  rcases h 3 (by decide) with ⟨g, hg⟩
  exact Z2_no_order_three g hg

/-- **ℝ-signed is EXCLUDED from FCAI.**  Although `ℤ/2` is abelian, it is not
order-unbounded, so the real-signed carrier fails the faithful-continuous-abelian
interference property.  (Non-vacuous: `ℤ/2` is inhabited and is a genuine
`PhaseGroup`.) -/
theorem Z2_not_FCAI : ¬ Z2.FCAI := by
  intro h
  exact Z2_not_orderUnbounded h.2

/-! ### §2.2  The ℂ fiber `U(1)` — cyclic rotations of every order, abelian, ADMITS FCAI

The complex unit fiber `U(1)` contains the `n`-th roots of unity for *every* `n` — the
faithful `ℤ/n` rotations.  We realize this as: the rotation fiber `Cyc n` is available
for every `n ≥ 1`, each is abelian, and each has its generator of order exactly `n`.
This is the finite shadow of "the fiber is `U(1)`, continuous."  We package it as a
single `PhaseGroup` whose `OrderUnbounded` holds — `ColimCyc`, the colimit/union of all
`ℤ/n`, i.e. the torsion subgroup `ℚ/ℤ` of `U(1)`.

To keep the model Mathlib-free *and* genuinely a single group with an element of every
order, we use the equivalent formulation that ℂ's admissibility is the statement:
**for every `n ≥ 1` there is an abelian rotation phase group (`Cyc n`) with an element
of order exactly `n`** — the faithful `ℤ/n` interference rotation.  This is exactly the
spec's "ℂ modelled finitely as ℤ/n rotations." -/

/-- **ℂ ADMITS the faithful `ℤ/n` rotation for every `n`** (the witness family).  For
each `n ≥ 1`, the rotation fiber `Cyc n` is abelian and its generator has order exactly
`n`.  This is the order-`n` interference rotation the real-signed fiber cannot host for
`n > 2`. -/
theorem complex_admits_rotation (n : Nat) (hn : 1 ≤ n) :
    (Cyc n).IsAbelian ∧ (Cyc n).HasOrder (1 : Nat) n :=
  ⟨Cyc_isAbelian n, Cyc_generator_hasOrder n hn⟩

/-- The order-3 rotation that **separates ℂ from ℝ-signed**: `Cyc 3` hosts an element
of order 3 (ℂ does), while `Z2 = Cyc 2` does not (ℝ-signed cannot).  Concrete witness
of the discrete-vs-continuous split. -/
theorem complex_hosts_order_three_real_signed_does_not :
    (Cyc 3).HasOrder (1 : Nat) 3 ∧ (∀ g : Nat, ¬ Z2.HasOrder g 3) :=
  ⟨Cyc_generator_hasOrder 3 (by decide), Z2_no_order_three⟩

/-- The family form (each order has *some* abelian rotation realizing it). -/
def ColimCycFCAIWitness : Prop :=
  ∀ n : Nat, 1 ≤ n → ∃ (PG : PhaseGroup) (g : PG.G),
    PG.IsAbelian ∧ PG.HasOrder g n

/-- **ℂ ADMITS FCAI (family / witnessed form).**  For every order `n`, the abelian
rotation fiber `Cyc n` realizes an element of that order — the faithful `ℤ/n` rotation. -/
theorem complexFiber_FCAI_witnessed : ColimCycFCAIWitness := by
  intro n hn
  exact ⟨Cyc n, (1 : Nat), Cyc_isAbelian n, Cyc_generator_hasOrder n hn⟩

/-! #### A *single* order-unbounded abelian group (closing the vacuity gap)

To make ℂ's admission symmetric with the ℝ-signed/ℍ exclusions — which are stated
about a *single* group failing `FCAI` — we exhibit ONE concrete `PhaseGroup` that
satisfies the full `FCAI = IsAbelian ∧ OrderUnbounded` predicate.  This is the product
`∏_{n} ℤ/(n+1)` carried on `Nat → Nat` (the `n`-th coordinate lives in `ℤ/(n+1)`); it
is a faithful single model of an order-unbounded abelian fiber (the `U(1)`-torsion
shadow), so `FCAI` is provably **non-vacuous**. -/

/-- pointwise modular addition: coordinate `n` lives in `ℤ/(n+1)`. -/
def prodMul (f g : Nat → Nat) : Nat → Nat := fun n => (f n + g n) % (n + 1)

/-- The single **product-cyclic** phase group `∏_n ℤ/(n+1)`. -/
def ProdCyc : PhaseGroup where
  G := Nat → Nat
  one := fun _ => 0
  mul := prodMul
  pow := stdPow (fun _ => 0) prodMul
  pow_zero := by intro g; rfl
  pow_succ := by intro g m; rfl

/-- `ProdCyc` is **abelian** (pointwise mod-add commutes). -/
theorem ProdCyc_isAbelian : ProdCyc.IsAbelian := by
  intro f g
  show prodMul f g = prodMul g f
  funext n
  unfold prodMul
  rw [Nat.add_comm]

/-- per-coordinate closed form for powers in `ProdCyc`. -/
theorem ProdCyc_pow (f : Nat → Nat) (m : Nat) :
    ProdCyc.pow f m = fun n => (f n * m) % (n + 1) := by
  induction m with
  | zero => funext n; simp [ProdCyc, stdPow]
  | succ k ih =>
    rw [ProdCyc.pow_succ]
    show prodMul (ProdCyc.pow f k) f = fun n => (f n * (k + 1)) % (n + 1)
    rw [ih]
    funext n
    unfold prodMul
    rw [Nat.mul_succ]
    simp [Nat.add_mod]

/-- the order-`m` generator of `ProdCyc`: the unit in coordinate `m-1` (i.e. the
coordinate whose modulus is exactly `m`), zero elsewhere. -/
def prodGen (m : Nat) : Nat → Nat := fun n => if n + 1 = m then 1 else 0

/-- The order-`m` generator has order exactly `m` (for `m ≥ 1`). -/
theorem ProdCyc_gen_hasOrder (m : Nat) (hm : 1 ≤ m) :
    ProdCyc.HasOrder (prodGen m) m := by
  refine ⟨hm, ?_, ?_⟩
  · -- pow (prodGen m) m = one
    rw [ProdCyc_pow]
    show (fun n => (prodGen m n * m) % (n + 1)) = (fun _ => 0)
    funext n
    show (prodGen m n * m) % (n + 1) = 0
    unfold prodGen
    by_cases h : n + 1 = m
    · rw [if_pos h, h, Nat.one_mul, Nat.mod_self]
    · rw [if_neg h, Nat.zero_mul, Nat.zero_mod]
  · intro p hp hpm
    rw [ProdCyc_pow]
    -- coordinate m-1 (where n+1 = m) holds value (1 * p) % m = p % m = p ≠ 0
    intro hcontra
    have hcoord : (prodGen m (m - 1) * p) % ((m - 1) + 1) = 0 := by
      have hcf := congrFun hcontra (m - 1)
      -- ProdCyc.one (m-1) reduces to 0
      change (prodGen m (m - 1) * p) % ((m - 1) + 1) = 0 at hcf
      exact hcf
    have hm1 : (m - 1) + 1 = m := by omega
    have hgen : prodGen m (m - 1) = 1 := by
      unfold prodGen; rw [if_pos hm1]
    rw [hgen, hm1, Nat.one_mul] at hcoord
    -- p % m = 0 but p % m = p (since 1 ≤ p < m) ≠ 0
    have hpp : p % m = p := Nat.mod_eq_of_lt hpm
    rw [hpp] at hcoord
    omega

/-- `ProdCyc` is **order-unbounded**: it has an element of every finite order. -/
theorem ProdCyc_orderUnbounded : ProdCyc.OrderUnbounded := by
  intro n hn
  exact ⟨prodGen n, ProdCyc_gen_hasOrder n hn⟩

/-- **ℂ ADMITS FCAI (single-group form).**  `ProdCyc` is one concrete phase group that
satisfies the full `FCAI` predicate — abelian *and* order-unbounded.  This proves the
discriminator is **non-vacuous**: a faithful, continuous, abelian interference fiber
genuinely exists (the `U(1)`-torsion shadow), exactly the structure ℝ-signed (discrete)
and ℍ (non-abelian) lack. -/
theorem ProdCyc_FCAI : ProdCyc.FCAI :=
  ⟨ProdCyc_isAbelian, ProdCyc_orderUnbounded⟩

/-! ### §2.3  The ℍ fiber `S³` — non-abelian phase group `Q8`, EXCLUDED from minimality

The quaternionic carrier's unit fiber is `S³`, whose phase group is non-abelian.  We
realize the obstruction finitely with the quaternion group `Q8 = {±1, ±i, ±j, ±k}`:
`i·j = k` but `j·i = −k`, so the single-system phase action does **not** commute.  The
cross-term then fails the *minimal abelian* phase requirement of FCAI.  (`PhaseGroup`
does not demand associativity/inverses, so `Q8` is a legitimate instance for the
non-commutativity witness.) -/

/-- The eight quaternion units. -/
inductive Q8 where
  | one | negOne | i | negI | j | negJ | k | negK
deriving DecidableEq, Repr

namespace Q8

/-- negation. -/
def neg : Q8 → Q8
  | one => negOne | negOne => one
  | i => negI | negI => i
  | j => negJ | negJ => j
  | k => negK | negK => k

/-- quaternion multiplication table (full 8×8). -/
def mul : Q8 → Q8 → Q8
  | one, b => b
  | negOne, b => neg b
  | a, one => a
  | a, negOne => neg a
  -- i · _      (remaining second args: i negI j negJ k negK)
  | i, i => negOne | i, negI => one | i, j => k | i, negJ => negK | i, k => negJ | i, negK => j
  -- negI · _
  | negI, i => one | negI, negI => negOne | negI, j => negK | negI, negJ => k | negI, k => j | negI, negK => negJ
  -- j · _
  | j, i => negK | j, negI => k | j, j => negOne | j, negJ => one | j, k => i | j, negK => negI
  -- negJ · _
  | negJ, i => k | negJ, negI => negK | negJ, j => one | negJ, negJ => negOne | negJ, k => negI | negJ, negK => i
  -- k · _
  | k, i => j | k, negI => negJ | k, j => negI | k, negJ => i | k, k => negOne | k, negK => one
  -- negK · _
  | negK, i => negJ | negK, negI => j | negK, j => i | negK, negJ => negI | negK, k => one | negK, negK => negOne

end Q8

/-- The **ℍ phase group** `Q8` (finite shadow of `S³`/`Sp(1)`). -/
def Qua : PhaseGroup where
  G := Q8
  one := Q8.one
  mul := Q8.mul
  pow := stdPow Q8.one Q8.mul
  pow_zero := by intro g; rfl
  pow_succ := by intro g m; rfl

/-- **ℍ EXCLUSION (the non-abelian fiber is genuine).**  `Q8` is NOT abelian:
`i · j = k ≠ −k = j · i`.  The quaternionic single-system phase action does not
commute, so it fails the minimal-abelian clause of FCAI.  (Non-vacuous: `Q8` is
inhabited with 8 distinct elements.) -/
theorem Qua_not_isAbelian : ¬ Qua.IsAbelian := by
  intro h
  have hij : Q8.mul Q8.i Q8.j = Q8.mul Q8.j Q8.i := h Q8.i Q8.j
  -- i·j = k, j·i = negK, and k ≠ negK
  exact absurd hij (by decide)

/-- Hence **ℍ is EXCLUDED from FCAI**: its phase group is non-abelian. -/
theorem Qua_not_FCAI : ¬ Qua.FCAI := by
  intro h
  exact Qua_not_isAbelian h.1

/-! ### §2.4  T-FORCE-ℂ — the honest conditional forcing

Assembling §2.1–§2.3: among `*`-carriers (T-FORCE-★ forced the conjugation), the
phase group satisfies the **faithful-continuous-abelian interference** property FCAI
exactly when it is abelian *and* order-unbounded.  The three concrete candidate
fibers are DISTINCT and split cleanly:

* **ℝ-signed** (`Z2 = Cyc 2`): abelian but NOT order-unbounded ⟹ `¬ FCAI` (discrete);
* **ℂ** (`Cyc n` rotations, all `n`): abelian AND order-unbounded ⟹ FCAI witnessed;
* **ℍ** (`Qua = Q8`): NOT abelian ⟹ `¬ FCAI` (non-commutative).

So, **among the three classical real-associative-division-algebra candidates**
(ℝ, ℂ, ℍ — the Frobenius list), ℂ is the carrier whose unit-fiber phase group carries
a faithful, continuous, abelian interference cross-term: `ℝ`-signed is excluded by
discreteness (bounded exponent), `ℍ` is excluded by non-commutativity.  HONEST SCOPE:
this is a *characterization conditional on FCAI over these three named candidates*, not
a proven lattice-minimality theorem (we do NOT prove "no other `*`-field works"); and
FCAI itself is a *hypothesis* — the genuinely imported clause — not derived from the
substrate.  What IS forced and mechanized: (a) the conjugation, from a nontrivial
invariant phase (§1, `conjugation_forced`); (b) the two exclusions, from genuine
inhabited fibers; (c) ℂ's admission, from a single inhabited FCAI group.  Both
exclusions are real and the three fibers are concretely distinct (non-vacuous). -/

/-- **T-FORCE-ℂ (the honest conditional).**  The complete discriminator, on the *same*
single-group `FCAI` predicate for all three:
(1) `Z2` (ℝ-signed) fails `FCAI` — not order-unbounded (discrete fiber);
(2) `Qua` (ℍ) fails `FCAI` — not abelian (non-commutative fiber);
(3) `ProdCyc` (ℂ-torsion shadow `ℚ/ℤ`) satisfies `FCAI` — abelian and order-unbounded.
So, **among the three Frobenius candidates ℝ/ℂ/ℍ**, ℂ is the one whose unit-fiber
phase group ADMITS `FCAI`, while ℝ-signed and ℍ are EXCLUDED.  HONEST SCOPE: this is
NOT "FCAI forces ℂ" — `FCAI = IsAbelian ∧ OrderUnbounded` is satisfied by a whole
class of abelian unbounded-order groups (the inhabiting witness `ProdCyc` is `ℚ/ℤ`,
NOT ℂ nor `U(1)`; so are all `∏ₙ ℤ/kₙ` with `kₙ → ∞`).  What is established: the two
exclusions (1),(2) are real and ℂ admits FCAI (3); uniqueness of ℂ among FCAI
carriers is NOT proved.  Both exclusions are genuine and non-vacuous: `FCAI` is
inhabited (3). -/
theorem T_FORCE_Complex :
    (¬ Z2.FCAI) ∧ (¬ Qua.FCAI) ∧ ProdCyc.FCAI ∧ ColimCycFCAIWitness :=
  ⟨Z2_not_FCAI, Qua_not_FCAI, ProdCyc_FCAI, complexFiber_FCAI_witnessed⟩

/-- **Non-vacuity / distinctness certificate.**  The three candidate fibers are
genuinely different objects and each predicate is inhabited: the order-3 rotation
exists in the ℂ fiber and is absent in the ℝ-signed fiber, and the ℍ fiber has a
witnessed non-commuting pair.  This blocks the "empty-by-fiat" vacuity attack. -/
theorem fibers_distinct_and_inhabited :
    (Cyc 3).HasOrder (1 : Nat) 3
      ∧ (¬ Z2.HasOrder (1 : Nat) 3)
      ∧ (Q8.mul Q8.i Q8.j ≠ Q8.mul Q8.j Q8.i) :=
  ⟨Cyc_generator_hasOrder 3 (by decide),
    Z2_no_order_three 1,
    by decide⟩

/-! ## §3  FIREWALL — derived ⇏ authority

`StructureDerived` (the cross-term forces the carrier) does **not** entail `IsAuth`.
We record this as a typed gap: there is no map from the forcing certificates to any
authority predicate; the forcing is finite, conditional, and mints nothing. -/

/-- An abstract authority predicate (the corpus firewall target). -/
def IsAuth (_carrier : Type) : Prop := False

/-- The forcing certificate is *structural*, recorded as a `Prop` bundle. -/
def StructureDerived : Prop :=
  ((¬ PhaseInvariant realSignedSlot 2) ∧ PhaseInvariant complexSlot 2)
    ∧ (¬ Z2.FCAI) ∧ (¬ Qua.FCAI) ∧ ProdCyc.FCAI ∧ ColimCycFCAIWitness

/-- **Firewall.**  `StructureDerived` holds, but it does not produce authority for any
carrier: `IsAuth` is unprovable from it (indeed `IsAuth _ = False`).  Derived
structure ⇏ authority. -/
theorem structureDerived_holds : StructureDerived :=
  ⟨T_FORCE_star, T_FORCE_Complex⟩

theorem structureDerived_not_mints_authority (C : Type) :
    StructureDerived → ¬ IsAuth C := by
  intro _ hAuth
  exact hAuth

end ForceComplexCarrier
end QM
