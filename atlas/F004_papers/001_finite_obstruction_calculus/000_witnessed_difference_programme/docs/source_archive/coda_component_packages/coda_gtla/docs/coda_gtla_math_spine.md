# Local records: presentations, spans, traces, and a firewall (CODA-GTLA companion)

**Author:** Jeremy H. Carroll

**Date:** 2026-09-28

**Version:** 3.2.1

**License:** Creative Commons Attribution 4.0 International

This companion lists the local definitions and theorems of the public note
`coda_gtla_monograph.md`. It is not a new calculus. Theorems that live in
FOC, FDA, MUR, OR, CS, and A are cited there, not re-proved here.
The vendored `Coda.A` source is shipped in `lean4/A.lean`. Other companion results remain external. Local Lean is the
namespace `CodaGtla` on declared records; Python supplies the finite restrictions.

---

## 1. Presentations, spans, traces

### Definition GTLA-D1

The Lean presentation record is a type $V$ with decidable equality (finiteness is required by Python, not stored in this Lean record) and a map
$\mathrm{diff}:V\to V\to\mathbb{N}$ with $\mathrm{diff}(x,x)=0$. Lean:
`CodaGtla.Presentation`.

### Definition GTLA-D2

A comparison span $P_1\leftarrow M\to P_2$ carries a cost in $\mathbb{N}$.
The diagonal span has cost $0$. Composite cost is the sum of costs along
the pullback of middle points. Lean: `CodaGtla.ComparisonSpan`,
`diagSpan`, `compSpan`.

### Theorem GTLA-T1

$\mathrm{extCost}(\mathrm{diagSpan}\,P)=0$. Lean:
`CodaGtla.diagSpan_cost_zero`. Proof: `rfl`.

### Theorem GTLA-T2

$\mathrm{extCost}(\mathrm{compSpan}\,S_1\,S_2)\le
\mathrm{extCost}\,S_1+\mathrm{extCost}\,S_2$. Lean:
`CodaGtla.compSpan_cost_subadditive`. Proof: the composite cost *is* the
sum, so $\le$ is `Nat.le_refl`.

### Definition GTLA-D3

A trace is a span plus steps and work in $\mathbb{N}$. Erasure returns the
span. Lean: `CodaGtla.Trace`, `idTrace`, `compTrace`, `eraseTrace`.

### Theorem GTLA-T3

$\mathrm{traceCost}(\mathrm{idTrace}\,P)=0$. Lean:
`CodaGtla.idTrace_work_zero`. Proof: `rfl`.

### Theorem GTLA-T4

$\mathrm{eraseTrace}(\mathrm{idTrace}\,P)=\mathrm{diagSpan}\,P$. Lean:
`CodaGtla.eraseTrace_id`. Proof: `rfl`.

### Theorem GTLA-T5

$\mathrm{eraseTrace}(\mathrm{compTrace}\,T_1\,T_2)
=\mathrm{compSpan}(\mathrm{eraseTrace}\,T_1)(\mathrm{eraseTrace}\,T_2)$.
Lean: `CodaGtla.eraseTrace_comp`. Proof: `rfl`.

These five theorems are record equalities. They are not OR-T1 (pair
gluing) and not a bicategory of comparison systems.

---

## 2. Finite evaluator and leftover $\neq$ standing

### Definition GTLA-D4

```
inductive TerminalOutcome
  | authorized (payloadId : String)
  | closedResidual (anomalonId : String) (phi1Distance : Nat)
  | refused (reason : String)
```

Predicates `IsAuth`, `IsAnomalon`, `IsRefused` read the constructors.
The residual constructor stores a diagnostic identifier and a natural-number
distance. It does not construct an A quotient class or an FDA standing record.

### Definition GTLA-D5

A pipeline input is a declared tuple of Booleans and leftover numbers.
`evaluatePipeline` reads them in order: empty sieve $\to$ refuse;
failed refinement or glue $\to$ refuse; $\Gamma_2>0$ $\to$ refuse;
$\Phi_1=0$ and licence $\to$ standing branch; $\Phi_1=0$ and no licence
$\to$ refuse; $\Phi_1>0$ and $\Gamma_2=0$ $\to$ leftover class.

### Theorem GTLA-T6

Empty sieve $\Rightarrow$ `IsRefused`. Lean:
`CodaGtla.pipeline_empty_sieve_refused`.

### Theorem GTLA-T7

Nonempty sieve, consistent refinement, successful glue, $\Gamma_2=0$,
$\Phi_1>0$ $\Rightarrow$ `IsAnomalon` (leftover class, not standing).
Lean: `CodaGtla.pipeline_closed_residual_anomalon`.

### Theorem GTLA-T8

The three predicates are pairwise disjoint. Lean:
`CodaGtla.auth_disjoint_anomalon`, `auth_disjoint_refused`,
`anomalon_disjoint_refused`. Proof: cases on the inductive.

### Theorem GTLA-T9

There exists an input with $\Phi_1=0$ and licence false whose output is
refused and not standing. Lean: `CodaGtla.non_promotion_firewall`.

### Theorem GTLA-T10

There exist two inputs with equal $\Phi_1$ and equal $\Gamma_2$ such that
one is standing and the other is not. Lean:
`CodaGtla.observation_collision_distinct_authority`.

A licensed zero-leftover input takes the standing branch of this
evaluator (`pipeline_licensed_exact_authorized`). That clause is a finite
`if`, not FDA standing soundness.

---

## 3. Citation, not replay

| Job | Home paper | What this package does |
|---|---|---|
| Obstruction leftover $\Phi_1,\Gamma_2$ | FOC | Reads declared numbers; Python may call the FOC solver |
| Standing pair | FDA | Reads a licence flag; does not inhabit FDA `Standing` |
| Transport square | MUR | Not re-proved |
| Overlap glue | OR | Boolean `gluingSucceeded`; not OR-T1 |
| Coarse/fine look | CS | Boolean `refinementConsistent`; not CS-T3 |
| Leftover vector $x-Cx$ | A | Leftover constructor; `Algebra.lean` wraps A |

`Algebra.lean` `#check`s `Coda.A.residual_zero_iff` and the
neighbouring A identities from the reconstruction library. Those
identifiers are proved in the vendored `A.lean` source.
They are separate residual-algebra results, not proofs of general GTLA category claims.

No bicategory, no H3'' glue, no general LP duality, no `sorry`.
