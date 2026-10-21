# TFQ-0084 — sharpened research target supplied for this P0 turn

AuthorityEffect: None. This is the caller-supplied sharpening of the TFQ-0084 target that was pasted
into the P0_MINE_OPERAD turn of 2026-10-21 (run `20261021T161243Z_staged`). The committed prompt
`dag/prompts/finite_qg_tfq_0084_open.yaml` still carries only the generic source statement; this file
preserves the sharpened target the mining turn actually worked against. The paste reached the model
clipped at a fixed column, so a few fragments are lost; they are marked `[clipped]` rather than
reconstructed. Nothing below is an accepted result.

Source claim (unchanged, from the DAG node): a finite gravity shadow is relational point coincidence, a
Regge deficit on a finite simplicial complex, a spin-foam or area-spectrum control, and kinematical
shadows; the exact rational proxy that sums squared areas times deficits is not the Einstein-Hilbert
action; the float script l1_regge.py is not that proxy; a certificate on a small complex is not a
derivation of the Einstein equation.

## Research target (sharpened; four parts)

**T1 — Schläfli identity, arccos-free.** For an n-simplex with squared edge lengths x = (x_e) as
indeterminates, prove `sum_h A_h * d(theta_h)/d(x_e) = 0` for every edge e, where h runs over
codimension-2 faces, A_h is the (n-2)-volume of h and theta_h the interior dihedral angle at h. Never
evaluate theta_h itself. Use `d(theta_h) = -d(cos theta_h)/sin theta_h`. Take cos theta_h from Gram /
Cayley-Menger minors, and sin theta_h from `(n/(n-1)) * V_sigma * A_h / (V_a * V_b)`, where V_a and V_b
are the facets meeting at h. The statement then lives in the field
`Q(x)(sqrt(CM_sigma), sqrt(CM_facets), s...[clipped])`; clear the roots into a polynomial identity, and
state exactly which nondegeneracy hypotheses (positive Cayley-Menger determinants) it needs. Order of
attack: n = 3 (tetrahedron, 6 indeterminates, hinges = edges) first, then n = 4 (pentatope, 10
indeterminates, hinges = triangles).

**T2 — Regge equations.** With `S(x) = sum_h A_h eps_h - Lambda * sum_sigma V_sigma`, where eps_h is the
deficit angle (2*pi minus the sum of the dihedral angles at h) and Lambda is a declared rational
parameter, derive from T1 that `dS/dx_e = sum_h eps_h dA_h/dx_e - Lambda * sum_sigma dV_sigma/dx_e`.
The derivative-of-angle terms cancel. The identity is between derivative structures. eps_h is
transcendental in general, so certify e...[clipped] on configurations whose dihedral angles are rational
multiples of pi (e.g. Kuhn/Freudenthal triangulations of hypercubes). Lambda is a caller-supplied
parameter, never a derived quantity (cf. TFQ-0106 and TFQ-0108).

**T3 — Flat-background gauge modes** (the "broken diffeomorphism" obstruction, made exact). On a
declared flat triangulated region with at least one interior vertex (the Kuhn triangulation of the
2x2x2x2 hypercube grid; also a 3D analogue), compute the Regge Hessian `d^2 S / dx dx` at the flat
lengths EXACTLY. Its entries are algebraic, with square roots (sqrt2, sqrt3, ...). Report its exact
rank, and show that vertex translations span a kernel of dimension d * (number of interior vertices).
Then perturb the boundary data ...[clipped] and report the exact change in kernel dimension. That is
the finite, checkable content of "diffeomorphism symmetry broken away from flatness".

**T4 — Task-specific near miss (mandatory).** The repo's proxy is
`code/rust/src/general_relativity/exact_regge/...` `proxy = sum_h A_h^2 * kappa_h` (the paste names it
`exact_ge_proxy`; the actual declaration is `rational_regge_proxy`, exact_regge/action.rs:47).
Exhibit an explicit rational simplex where `sum_h A_h^2 * d(theta_h)/d(x_e) != 0` exactly, so the
squared-area weighting is not Schläfli-invariant and does not give Regge equations. The valid control
is T1 holding on the same simplex.

## Fences (keep explicit in every stage)

- The continuum Einstein equation `G + Lambda g = ...` is not a target. Convergence of the Regge action
  to the integral of `R*sqrt(g)` for fat triangulations (Cheeger-Müller-Schrader) is a literature
  theorem: record it as IMPORTED; do not derive it.
- Euclidean signature only. Lorentzian Regge, spin-foam dynamics, Wheeler-DeWitt and physical Lambda are
  out of scope.
- `field_equation.rs` and `hamiltonian_constraint.rs` write formulae; a formula is not a derivation.

## Declared assumptions

- Euclidean simplicial complex with declared squared edge lengths in Q (or in a declared real quadratic
  field), satisfying strict Cayley-Menger positivity on every simplex.
- Lambda: declared rational parameter.
- Imported, not derived: Cheeger-Müller-Schrader convergence (cite only).

## Sources named for mining (pins recorded in `source_inventory.json`)

- `regge_exact::cayley_menger` (external crate `linear_algebra`, used by `exact_regge/action.rs`)
- `code/rust/src/general_relativity/exact_regge/{action,closure,connection,manifold,refinement,orientation}.rs`
- `code/rust/src/general_relativity/cayley_menger.rs` (float only, never a certificate)
- `code/rust/src/general_relativity/field_equation.rs`, `hamiltonian_constraint.rs` (formula stubs; TFQ-0107)
- `papers/core/constraint_closure/lean4/GR002.lean` (hexagonal-disk count; TFQ-0102)
- `papers/core/constraint_closure/code/l1_regge.py` (float; TFQ-0099, fenced)
- DAG nodes: DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS (PFP review), TFQ-0090, TFQ-0100, TFQ-0101,
  TFQ-0106, TFQ-0107

## Checker contract to fix in M4 before P1 (as supplied)

- Lean 4 (`leanprover/lean4:v4.35.0`, Mathlib pinned as in the v4.35.0 migration): `lean4/ReggeSchlafli.lean`.
  T1 for n = 3 as a polynomial identity after clearing square roots. Axioms limited to `propext`,
  `Classical.choice`, `Quot.sound`; no `sorry`.
- Rust: exact checker over BigRational / quadratic fields, reusing `regge_exact::cayley_menger`. T1 and
  T4 on declared rational simplices; T3 Hessian by exact elimination.
- Python: an independent exact checker (fractions + an explicit quadratic-field class, or SymPy exact)
  that re-derives T1, T3 and T4 on the same inputs.
- P4 semantic mutants: `A_h^2` weighting (T4); dropping one hinge; wrong `sin theta` formula (missing
  `n/(n-1)`); a degenerate simplex (Cayley-Menger = 0) that must be refused; a perturbed flat
  configuration claimed flat.

## P0 task for this turn (as supplied)

Open the operad record, review candidates, and collect typed generators for the colours: simplex, face,
squared-length vector, Cayley-Menger minor, dihedral cosine and sine, hinge volume, deficit, action;
and the operations: Cayley-Menger volume, the dihedral-sine product formula, Schläfli, and the
cancellation in T2. Record what is missing (e.g. no exact dihedral-sine routine in the sources). The
most useful unresolved dependency is the n = 3 Schläfli identity in arccos-free form. If it needs more
work, remain at P0 and save the partial collection. Do not attempt the final derivation in this turn.
