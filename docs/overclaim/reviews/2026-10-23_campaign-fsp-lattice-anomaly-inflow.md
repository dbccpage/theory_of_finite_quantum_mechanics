# Review of campaign FSP-LATTICE-ANOMALY-INFLOW

AuthorityEffect: None. AI self-review by the PR author, awaiting human review.

Superseded by the independent review `docs/overclaim/reviews/2026-10-22_pr-203.md`,
which reclassifies the outcome from Narrowed to no result (failed candidate) and
corrects the "obstruction" framing. This file is kept as the author's record.

Scope: campaign/fsp-lattice-anomaly-inflow against origin/main
3924d378ff1de685948bf2b419dc63a5a9560881. Compiled source commit:
1f89c54283ae0c6b5ee7acd0dc3aebe01a1ec11c. The full node remains OPEN.

Method: read the target statement, source passages, every new Lean declaration,
the exact checker and the derivation note. Used the campaign's completed build
receipt; no Lean, Lake or Cargo build was performed as part of this review.
Checked source bytes against committed LF blobs and all printed axiom sets.
Normal and optimized independent outputs agree. The scanner cannot determine
whether a fixed chiral matrix is the physical determinant line.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM among the campaign target nodes.
No node status changed. This is a provisional failed-candidate result, subject
to a reviewer's classification. It neither discharges the original target nor
refutes the existence of other finite regulators.

## Corrections to the PR's own text

- The CS term is called a lifted cup-product candidate throughout. Its
  coefficient is specified rather than extracted from the Wilson determinant.
- K is a fixed-basis chiral truncation. The actual boundary Schur determinant
  and the interior determinant are separately gauge invariant.
- The width-three witness uses a gauge transformation vanishing on the lateral
  faces; that excludes missing side support as an explanation of this witness.
- The default library and the historical anomaly module were not rebuilt.
- The new proof/checker are assessed L4C/L4D. The declarative Lake registration
  is L1C, a disclosed exception to the per-file L4 floor (on main the same
  companion is L1 with no grade).

## Per-node statement-versus-theorem table

All Lean declarations below are in `lean4/CampaignFspLatticeAnomalyInflow.lean`.

| Atomic claim | Declaration or evidence | Verdict |
|---|---|---|
| Wilson hopping transforms covariantly in fixed spin bases | `hopping_covariant`, lines 100-110; explicit matrices independently assembled by `wilson`, checker line 130 | NARROWED: general algebra plus finite computational construction |
| Interior elimination preserves covariance when an inverse exists | `transport_inverse`, line 49; `schur_covariant`, line 90 | FULL for the stated algebraic identities; physical target still NARROWED |
| Boundary chiral determinant has the anomalous variation required by the node | not proved; `chiral_fixed_basis_det`, line 75, instead states invariance for site-matched fixed bases | NOT PROVED |
| Rational lifted CS variation is a boundary pairing | `curvature_gauge`, line 121; `bianchi`, line 125; `cs_cell_variation`, line 139; `cs_chain_variation`, line 144 | NARROWED to the defined lifted cochain action |
| Defined width-two CS actions change from zero to 1/32 | `slab_three_cs`, line 176; `slab_four_cs`, line 181 | NARROWED to the explicit boxes |
| Explicit Wilson determinants and width-three control values | independent checker lines 189-255 and committed computational receipt; no Lean determinant evaluation | NARROWED computational evidence |
| Combined candidate factor is unequal to its original value | `phase_times_det_ne`, line 193, with exact computational identification of the phase and nonzero determinant | NARROWED |
| This CS action is induced by the Wilson interior and defines compact U(1) inflow | not proved; same-link integer-lift failure is checked at checker lines 230-232 | NOT PROVED |
| Full finite-lattice anomalous cancellation or continuum Callan-Harvey theorem | not proved | NOT PROVED |

The node's statement retains the full target and says that the tested candidate
has obstruction witnesses. Its bottleneck requires a regulated chiral
determinant, compatible induced inflow and compact completion. OPEN is retained.

## Numbers recomputed

| Quantity | Recomputed evidence | Result |
|---|---|---|
| Width-two matrix sizes 24 and 32; width-three size 54 | geometry and Wilson assembly in the independent checker | match |
| All displayed rational determinants | exact domain elimination, before and after gauge change; det D = det C det S checked separately | match |
| CS change 1/32 and same-link integer-lift change 1/8 | tetrahedral sums and independently assembled boundary chain; first change also kernel checked for the width-two cases | match |
| Cyclotomic polynomial X^16+1 and residual X-1 | SymPy cyclotomic polynomial and exact polynomial remainder | match |
| Eight domain refusals and three killed mutations | explicit challenge calls in checker lines 266-294; no surviving, invalid, equivalent, inconclusive or unrun mutants | match |
| Eighteen theorem audits | eighteen terminal print commands, each matched to a parsed build-output axiom set | match |
| Twenty-four campaign regression tests | captured pytest output in the campaign checks receipt | match |
| Generated README inventory counts | `scripts/build_readme_facts.py --check` | current; inventory only |

No numerical mismatch was found in the campaign evidence. Toolchain versions,
dates and source IDs are metadata, not mathematical quantities.

## Scanner output and remaining failures

The changed-since strict scan returned HIGH=0, MEDIUM=0, LOW=3. The LOW findings
concern existing tensor receipt/module coverage and numbers in tensor notes;
they do not concern the anomaly target. No baseline entry was added.

The required sync, invariants, rendering, DAG validation, README, receipt,
evidence and regression checks pass. The all-missing prompt writer returns
success while refusing to rewrite the executed TFQ-0084 prompt. Its additional
`--check --all-missing` diagnostic returns failure for that manual-delta item;
the TFQ-0084 node is unchanged from the base.

The additional repository-wide contract check returns failure because
`lean4/HilbertLiftOperators.contract.score.yaml` has malformed JSON. Its bytes
are unchanged from origin/main. The three campaign companions pass the
history-integrity checker and bind their current sources. No full repository
contract success is claimed.

The all-missing generator required a syntax repair to the TFQ-0016 operad
statement. The statement string was preserved, and the generator then refreshed
its existing declaration pins. That module was not rebuilt in this campaign.

## What the scanner could not decide

The physical regulator/measure defining an anomalous determinant, matching an
induced bulk term, compact gauge invariance, continuum limits and the final
outcome class require human review. No proof of those obligations appears in
this PR. The continuum mechanism remains a literature import.
