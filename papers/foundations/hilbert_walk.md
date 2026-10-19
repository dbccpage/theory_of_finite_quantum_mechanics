# HILBERT_WALK — from the Primitive Difference trunk to the finite Hilbert boundary

**AuthorityEffect:** None. Candidate research object in a review
queue. Nothing here mints authority, re-proves genesis, or amends
any estate paper.

## What this is

A replayable walk of eighteen named lifts (H000–H017) from the
repaired J011 set-theoretic trunk toward Hilbert-space language,
mechanized in `lake build FableHilbertWalk20260819` (Lean core
v4.32.2, no mathlib, axiom policy `{propext, Quot.sound}`). Every
lift states what it imports, what invariant survives, what new
expression becomes possible, and what finite countermodel prevents
a stronger claim (see `countermodel_register.md`). Machine records
are in `hilbert_walk.yaml`; printed axioms in `axiom_report.txt`;
commands and hashes in `build_receipt.md`.

## What this is — and is not (honest scope, 2026-08-19)

An adversarial review of the first release correctly held the
result to a higher standard than the prose met. Corrected here:

- **It is a portfolio of typed rung witnesses, not a single
  threaded derivation.** H017's `finite_hilbert_boundary` is a
  *conjunction* of separately-proved theorems over a shared
  Bool/Int/GaussInt substrate; H000's `PresentedCarrier` object is
  not the thing later rungs transform. The one genuine cross-rung
  thread the layers do support — phase-blind equivariance linking
  the H006 isometry, the H002/H003 pushforward, and one reversible
  report map (`HWThread.phaseBlind_intertwines`) — is proved as a
  real theorem. Full end-to-end threading through one object is the
  primary open obligation (FRONTIER R0).
- **"Unitary" is the work order's rung name, not an earned
  Hilbert-space claim.** What is proved in general is a
  form-preserving *isometry* over an arbitrary *-module (degenerate
  ones included — over F2 the form is isotropic). Over the Int
  positive-definite host it is an isometric *automorphism*
  (`permU_isometric_automorphism_over_posdef`); even that is not a
  Hilbert unitary (a*-ring, not a field; no completeness).
- **The honest ceiling is a finite pre-Hilbert shadow with a
  genuine phase non-descent witness** — not a PD-to-Hilbert
  derivation of quantum mechanics.

The rung sections below have been corrected to match.

The trunk is consumed as-is: the campaign directly imports only
`J011Admitted` surfaces (`Core`, `E003`, `E005`, `E011`, `E012`,
`E018`; their compiled closure adds `E008`, `E009`, `E013`, all
likewise `J011Admitted` roots) — no cohomology, Banach, observer,
or quantum-branch modules (gate G2). Paper 0 is untouched (gate
G3, hash in the receipt).

## A host artifact, honestly bounded

Under the campaign axiom policy, the **off-the-shelf rational
route is choice-tainted**: each of the nine `Rat` arithmetic laws
the `ratPack` requires, *as proved in this Lean core*, routes
through `Classical.choice` (per-law receipts in
`axiom_report.txt`), and concrete `Rat` arithmetic does not
kernel-reduce. `#print axioms` reports what the *shipped* proofs
use, not what is *necessary* — so this is **not** an impossibility
result: a choice-free ℚ is available at the cost of reproving
those laws (itself an import/work item, FRONTIER R5), and it is
not claimed that every `Rat` lemma is tainted (`Rat.neg_zero`,
for one, is choice-free). Consequence, adopted throughout: masses
and weights are **exact integers at a declared positive scale**.
The modest, honest reading: assembling a dense mass carrier from
the core lemmas as they stand pulls in choice, so a clean ℚ is an
explicit cost the "probability simplex" rung must pay — not that
ℚ is barred.

## The walk, lift by lift

### H000 — finite presented carrier
A carrier with a declared presentation packs with a supplied
`Enum` finiteness witness; the same-report relation is literally
the trunk's `fiberPD` zero-relation (`E003`), so the walk starts
INSIDE the Primitive Difference calculus, not beside it.
*Countermodel:* `Nat` with the parity presentation keeps every PD
law and admits no `Enum` — finiteness is an independent import.

### H001 — scaled-integer simplex shadow over reports
Integer weights, nonnegativity, and normalization to a declared
scale are three separate imports. This is an M-scaled integer grid,
not the ordinary rational/real probability simplex exactly: for
example, at scale 1 it contains no `(1/2, 1/2)` state. No
normalization equivalence to the full simplex is proved.
Nonnegativity and normalization each have a one-field separator
(signed vector; unnormalized vector); the mass-carrier import itself
is exposed by the `ratPack` boundary receipt. L1 distance is defined,
not selected. The dense-carrier import boundary (above) lives here.

### H002 — deterministic report dynamics
Pushforward along ANY report map preserves total mass — proved in
full generality (`pushforward_mass`, a finite Fubini over
enumerated fibers), not fixture-checked. Descent from ambient
dynamics is gated by the trunk's fiber law; the E018 model is
re-exported: fixing every section point while splitting a fiber
leaves NO descended dynamics.

### H003 — reversibility gate
Reversibility is a supplied two-sided inverse. Obligation 7 is a
theorem: the two-state collapse is deterministic and has no
inverse. Payoff invariant, proved generally: a reversible map
pushes weights forward by precomposition with its inverse — a
permutation of weights, nothing more.

### H004 — free linearization
The free module K^Q over an imported coefficient pack gives
superposition SYNTAX: `basis_expansion` proves every vector is the
pack-sum of its coordinates against the delta basis, for any pack.
The carrier is observably an import: δ_true + δ_true vanishes over
F2 and persists over Int.

### H005 — inner-product admission
The sesquilinear form with declared orthonormal report basis is
admitted, not derived: two positive-definite Grams disagree on the
same module (`gram_not_unique`, with definiteness itself proved in
`gramStd_pos_def` and `gramWeighted_pos_def`), and over F2 the
standard form has the nonzero isotropic vector (1,1)
(`f2_isotropic`) — positivity rides on the carrier import. Where
the carrier supports it, positivity is proved (`int_pos_semidef`
and the definite versions above; `gauss_self_real`: conj(z)·z is
real and nonnegative).

### H006 — permutation "unitary" (obligation 1)
**`permutation_isometry`**: for every pack, every enumerated
carrier, every reversible report map, the linear extension
U(v) = v ∘ inv *preserves the admitted form*; `permU_left_inverse`
/ `permU_right_inverse` prove U two-sided invertible; and
`permutation_on_basis` confirms U δ_q = δ_{τq}. **"Unitary" is the
work order's rung name, used only in that sense** — the general
statement is an isometry of a *possibly-degenerate* form (over F2
the form is isotropic, H005), *not* a unitary. Over the Int
positive-definite host it is an isometric *automorphism*
(`permU_isometric_automorphism_over_posdef`: isometry + two-sided
inverse of a positive-definite form) — still not a Hilbert
unitary (Int is a *-ring, not a field; no completeness). The
envelope is STRICT regardless: `swapI` (= i·SWAP over ℤ[i])
preserves the form and provably extends no report bijection.
"Permutation representation ⇒ all unitary dynamics" is refused by
theorem, not by disclaimer.

### H007 — complexification (obligation 6)
ℤ[i] is available (i² = −1; the real-like line embeds respecting
operations; i lies outside it) and NOT forced: the entire
H004–H006 pipeline re-runs over Int with trivial conjugation
(`real_pipeline_complete` — representative theorems from each of
H004/H005/H006 at the Int instantiation). In this host ℝ and ℂ do
not exist; ℤ[i] is a cheap complex-like carrier available
choice-free, and taking it is an explicit import (no minimality
over rival carriers is claimed).

### H008 — phase-blind presentation
ψ_q ↦ |ψ_q|² lands in honest integer weights (real, nonnegative,
total explicit). It is deliberately NOT named Born: the quadratic
rule is the import here, and its uniqueness is priced at H013.
Witnesses: ψ₁ = (1,1), ψ₂ = (1,−1) — equal weights, unequal
vectors. Global i-multiplication preserves all weights (general
theorem).

### H009 — phase-fiber invariant (obligation 5)
The phase-blind map induces a `Core.PrimitiveDifference` on
amplitude vectors — the trunk's own kernel shape, so "phase is the
hidden information of a PD presentation" is a statement IN the
trunk calculus (QM_060's claim, made exact). Global phase lies in
the fiber (general); ψ₁, ψ₂ are distinct members of one fiber; and
the fiber STRICTLY exceeds the global-unit orbit: ψ₂ is no unit
multiple of ψ₁ over ℤ[i].

### H010 — interference non-descent (obligations 2, 3, 4; gate G6)
The QM_061 witness replayed exactly at integer scale: the
unnormalized Hadamard (entries 1,1,1,−1; total-weight doubling
disclosed and proved on the witnesses — the general scale law is
open residue R1) sends ψ₁ ↦ weights (4,0) and ψ₂ ↦ (0,4).
**`no_descent_through_fiber`**: no function of the phase-blind
report reproduces the mixed readout. Mutations, as theorems:
removing the phase (ψ₂ ↦ (1,1)) collapses the separation;
removing the mixing makes the readout descend (phase invisible to
diagonal measurement). And the sharpest finding of the walk:
**`int_realization` / `int_no_descent` — the entire obstruction
runs over ℤ, using only the sign group {±1}.** Interference
non-descent does not select i, ℂ, or U(1).

### H011 — U(1) selector boundary
QM_062's selector assumptions are represented as a named import
pack; with every assumption granted except a rival-exclusion
theorem, the selector predicate is false, and the rival is real:
the sign carrier realizes the witness (H010). U(1)/ℂ is neither
selected nor refuted — the exclusion theorem is open residue O-1.

### H012 — operator-algebra host
2×2 integer matrices give a noncommutativity witness; the diagonal
subalgebra — the shadow visible to the weight layer — commutes
(general theorem). Noncommutativity is a property of the operator
import, absent from the L1 simplex. No adjoint, C*-structure, or
spectral theorem is constructed: each stays a priced import.

### H013 — Born pairing boundary (obligation 9)
**Corrected 2026-08-19.** A bilinear state-effect pairing exists
(bilinearity proved in both slots: `pair_linear_state`,
`pair_linear_effect`). Obligation 9 asks to *identify* the
Born-uniqueness hypotheses and bind them or *mark them imported*;
`GleasonPack` names them (dimension ≥ 3, noncontextuality,
σ-additivity, continuity), all imported/absent here. What is
**not** proved (earlier overstated as "existence is not
uniqueness"): a *same-normalization-contract* Born non-uniqueness.
The quartic readout is positive, non-proportional to the quadratic
one (`quartic_not_proportional`), and differs pointwise — but it
normalizes to a **different total** (17 vs 5), so the two do not
share one normalization contract on a common state/effect domain.
It shows only that the quadratic rule is not the unique positive
scale-distinct readout. A genuine same-contract effect-bearing
rival is open obligation **O-6** (`born_nonuniqueness_open` =
false), consistent with Gleason failing at dimension 2.

### H014 — tensor composition boundary
**Corrected 2026-08-19** (an earlier version claimed a false
"different coordinate count" for Bool×Bool vs Bool+Bool — both
have four elements; the claim and its never-implemented
`composite_sizes_differ` are withdrawn). What is actually proved:
`bell_not_product` — the correlation vector δ(ff)+δ(tt) over ℤ (the
2×2 identity as a function) has no rank-one factorization u⊗v (the
only nontrivial ring input is `Int.mul_eq_zero`; the rest is ring
bookkeeping): a **genuine finite entanglement witness**. And
`sum_component_embedding_surjective` — every direct-sum vector is
the join of its two component vectors, so that host is exhausted
by its component embedding, whereas the tensor host is not. The
two composition rules are therefore *structurally inequivalent*.
**Not proved** — that a rival satisfies the same composition
interface, hence that tensor is "not forced": that is an
undischarged boundary (`tensor_not_forced_open` = false), on par
with the H011 selector and the H013 Gleason package.

### H015 — irreversible dynamics fork (obligation 8)
`collapse_no_isometry`: no form-preserving map sends both basis
vectors to δ_false — two basis values and one inner product
suffice, linearity not even assumed. A selected dilation is not
canonical: two distinct reversible ambient dynamics induce the
same reduced report dynamics (here the identity —
`same_reduction`, `dilations_distinct`). Whether the collapse
itself admits a reversible dilation depends on an
ancilla-preparation convention this host does not formalize (open
obligation O-4 in the register).

### H016 — continuous dynamics fork (obligation 10)
The toggle has no report-level square root (exhaustive over the
four Bool endomaps). After the complex import, interpolants exist
at disclosed scale 4 (M² = 4·SWAP over ℤ[i]) and are not unique
(−M works too). The continuum itself — topology, one-parameter
group, Stone hypotheses — is named and not taken.

### H017 — the finite Hilbert boundary theorem
The work order supplied this target sentence:

> A finite presented carrier with reversible report dynamics
> admits, after explicit coefficient and inner-product choices, a
> permutation-unitary representation. A phase-blind quadratic
> presentation has fibers containing states with equal L1 data,
> and a supplied mixing presentation can distinguish members of
> such a fiber. Complex phase, Born uniqueness, tensor
> composition, general quantum channels, and continuous unitary
> dynamics remain separate imports unless discharged by additional
> theorems.

`finite_hilbert_boundary` does **not** prove that sentence as one
threaded implication. It is the strongest compiled assembly in this
campaign: a conjunction of separately proved rung witnesses. Its
first conjunct is the general permutation-isometry statement, not
the positive-definite-host automorphism; its other conjuncts are
fixed fixtures. The quoted sentence is therefore the work-order
target and scope guide, not the formal theorem type.

The `ImportLedger` is a **hand-maintained status ledger
(metadata), not a theorem-bound gate**: its Bool flags are set by
hand and `AllDischarged walkLedger = false` is `rfl` over those
flags, which binds nothing on its own — the actual evidence is the
individual named theorems. Read that way, it records: three flags
up (envelope, fiber, non-descent), five down (complex phase, Born
uniqueness, tensor, channels, continuum).

The tensor component is only the entanglement witness plus the open
non-forcing boundary from H014. The theorem is not a single object
threaded through the spine (see "What this is — and is not").
`HWThread.phaseBlind_intertwines` proves one genuine commuting square
across the dynamics/isometry/phase layers; its Bool specialization
reuses H000's `enumQ` field but not H000's carrier or presentation.

## Relationship to Paper 0

Contact only, no edits (byte-identity in `build_receipt.md`). The
walk uses the trunk's projection/retraction/escape/descent
language through `Core`/`E003`/`E005`/`E018` and adds the finite
Hilbert envelope as a separate branch:

```text
Primitive Difference trunk
  -> quotient/fiber presentation
  -> split/retraction calculus
       +-> Paper 0 application            (untouched)
       +-> finite Hilbert envelope        (H000-H006)
            -> phase-blind fibers          (H008-H009)
            -> interference non-descent    (H010)
            -> operator and information hosts (H012-H014, priced)
```

Nothing here claims Paper 0 derives any later Hilbert structure.

**AuthorityEffect:** None.
