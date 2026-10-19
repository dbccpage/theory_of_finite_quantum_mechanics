> **Current audited separator evidence:** [Separator claim and operad audit](reviews/20261018_separator_audit/README.md). Use its `verify_review.py --working-sources` for the current checkout. The sealed run remains historical; full formal rational Fine converse remains open.

> **Latest separator stage:** [20261018 separator extension](runs/20261018T233710Z_separator_extension/README.md). Use that run's replay for current source checks. Earlier audit/source pins remain historical. Stopped for review; full formal rational Fine converse remains open.

> **Audited verification:** [Bell claim and checker review](reviews/20261018_claim_audit/README.md). Use the hardened review checker; historical run bytes are preserved.

> **Latest staged run:** [20261018 expectation/operad run](runs/20261018T225117Z_operad_expectation/README.md). P0/P1/P2/P4/P5 completed; stopped for review. Fine converse remains open.

> **Historical pilot; contract superseded.** The old 18-field response and C4 arithmetic are not the staged execution contract. See `pilot_status.yaml` and `../../pfp/README.md`. The native Bell implication remains a scoped reusable result; no Fine-theorem equivalence or completed formal operad is claimed.

# FQ-BELL-CLASSICAL-JOINT-EXTENSION

This folder contains the execution of this single prompt. `response.json` is the
requested 18-field response; `certificate.json` contains the actual mathematical
checks. `prompt.yaml` preserves the executed prompt bytes. `checks.json` records
the native commands, exit statuses, source hashes, and logs. No other prompt was
executed, and no external model API was called. AuthorityEffect: None.

## Target and assumptions (M1)

Let Ω = {−1,+1}⁴, with coordinates A0, A1, B0, B1. Supply nonnegative rational
weights p(ω) with Σp = 1. Define E_xy = Σ p(ω) A_x(ω)B_y(ω) and
S = E00 + E01 + E10 − E11. The target is −2 ≤ S ≤ 2, with both bounds attained.
Zero weights are allowed: “positive joint law” means a nonnegative probability law.

The finite rational law is admitted. No complex scalar field, Hilbert space,
positive operator cone, Born pairing, tensor product, or unitary dynamics is
required. The prompt's generic Z[i]/Q(ζ_n) carrier wording is not used by this
claim. Locality and setting independence remain additional assumptions for a
physical reading. The prompt's carrier sentence is truncated; the full target is
recovered from the named local theorem and the existing finite-CHSH source record.

## Operadic construction (M2)

Use these operations on the same fixed carrier:

1. `response_products : Ω → {−1,+1}⁴`, taking (a0,a1,b0,b1) to
   (a0b0,a0b1,a1b0,a1b1).
2. `expectation : (Prob_Q(Ω), (Ω → Q⁴)) → Q⁴`, summing with the supplied law.
3. `chsh : Q⁴ → Q`, with coefficients (1,1,1,−1).

Finite distributivity licenses `chsh(expectation(p,f)) = expectation(p,chsh∘f)`.
The insertion matches the same Ω, coordinate order, scalar field, and single law.
This is finite affine composition; a larger operad catalog is unnecessary.

## Derivation

For every assignment,

    s(ω) = a0(b0+b1) + a1(b0−b1).

If b0=b1, the second term vanishes and s=2a0b0. If b0=−b1, the first term
vanishes and s=2a1b0. Thus s is exactly +2 or −2. Let P+ and P− be the total
weights on these two classes. Then P+,P− ≥ 0, P++P−=1, and

    S = 2(P+−P−),     2+S = 4P+ ≥ 0,     2−S = 4P− ≥ 0.

This proves the bound and supplies exact nonnegative slack certificates. A point
mass at (−1,−1,−1,−1) attains +2; a point mass at (+1,−1,−1,−1) attains −2.
A 3/5,2/5 mixture of those points gives S=2/5.

For Lean, clear the finitely many rational denominators: choose D>0 and natural
numerators n_i with Σn_i=D. The proved conclusion −2D ≤ Σn_i s_i ≤ 2D is exactly
the rational statement after division by D. The new theorem binds each score to
its actual binary assignment before reusing the existing weighted convexity
theorem. It does not take the score bound as an extra caller-supplied hypothesis.
`numerator_eq_four_correlations` also proves the finite distributivity step, so
`normalized_four_correlation_bound` states the bound directly for the four
correlation sums. Lean reports only its standard logical axioms (`propext`,
`Classical.choice`, and `Quot.sound`) for the general bound; the concrete
positivity counterexample uses no axioms.

## Independent checks and decoys (M3)

Rust and Python independently compute four correlators and the factored-score
class masses. Tests cover all 16 vertices (eight at each bound), the uniform law,
an asymmetric rational law, every ordered vertex pair at three rational mixture
weights (768 cases), and a denominator larger than 10¹⁰⁰.

The signed, normalized weights 3/2 and −1/2 on the two saturation points give
S=4. The APIs reject their negative weight. A mass-two point weight also gives
S=4 and is rejected for failed normalization. Replacing the minus sign before
E11 by plus produces 4 even on the valid all-minus point mass; that expression
is not the CHSH functional. These are distinct mathematical failure modes.

The supplied C4 exercise is checked separately. With edge orientations
(0→1,1→2,2→3,0→3), d1=(1,1,1,−1), and the incidence matrix in
`certificate.json`, d1·d0=0. The potential is (0,1140,−2280,1710), residual is
(0,0,0,−2280), and Γ2=2280. The dual w=(1,1,1,−1) has d0ᵀw=0,
||w||∞=1, and ⟨w,c⟩=2280=||r||1, certifying that L1 optimum. Reversing only
the last face sign breaks d1·d0=0. This diagnostic does not prove the Bell claim.

The requested 480 is index/stage/route arithmetic. The requested 128 is
263−128−7. The prompt supplies no algebraic map establishing those subtracted
scalars as a gauge ideal for CHSH. Their arithmetic is reproduced in
`response.json`; a mathematical quotient interpretation remains unsupported.

## Certificate anchors and validation (M4)

- Python: `code/python/src/qm/bell_joint_extension.py::certify_joint_law`.
- Rust: `code/rust/src/finite_probability/bell_joint_extension.rs::certify_joint_law`,
  exported by `tfqm_finite_probability`.
- Lean: `lean4/BellClassicalJointExtension.lean`, especially
  `QuantumMechanics.BellClassicalJointExtension.normalized_four_correlation_bound` and
  `no_joint_law_above_two`.
- Existing proof reused: `lean4/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound`.
- Existing paper: `dag/derivations/12_finite_qm_structure/TFQ-0259_finite_chsh_ceiling_on_one_global_joint_table.md`.

The legacy anchor strings are retained verbatim in the requested JSON. Their
current local paths are `lean4/DerivationDagQMClosure.lean` and
`code/rust/src/dag_witnesses.rs`; the historical paths in the prompt are not
asserted to be current local paths. Use the new anchors above for this execution.

From this folder, `python replay.py` compares both saved JSON artifacts with an
exact replay. `python validate.py` runs the targeted Python and Rust tests,
compiles the existing Lean dependency and new theorem with the pinned toolchain,
and records actual output in `logs/` and `checks.json`. Consult that receipt for
the observed validation status; this report does not substitute for the logs.

## Result and remaining obstruction

The classical joint-law CHSH bound has an exact finite proof and executable
certificates. A CHSH value outside [−2,2] excludes such a positive joint law for
the same four correlations. The bound alone is not asserted sufficient for a
joint extension, and constructing quantum correlations is outside this run.

Supports: the CHSH bound for one admitted finite rational joint probability law.

Does not support: derivation of locality, setting independence, quantum theory,
or the prompt's unsubstantiated gauge-quotient interpretation.

Narrowest defensible claim: the assignment-bound, common-denominator theorem
and the explicitly logged native certificate checks for this one prompt.

Next test needed: review this pilot's proof, artifacts, and code before selecting
or executing another prompt.
