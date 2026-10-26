# PR 186 adversarial audit of the synthesized PO-000 proof packet

**Audit date:** 2026-09-01
**Candidate commit:** `c6ce47da3a656728f8008165445f594767c2ae87`
**Canonical manuscript:** `projection_obstruction.md`, v6.3
**Canonical claim ledger:** `projection_obstruction_claim_ledger.md`
**Verdict:** `RepairRequired`
**Proof sign-off:** `BLOCKED`
**Release status:** not Zenodo-ready

## Executive result

The candidate `final_proof.tex` and rendered `final_proof.pdf` are not an
admissible replacement, proof supplement, or release artifact for PO-000.
They duplicate part of the canonical manuscript while changing claim status,
omitting the canonical scope fences, and citing receipts that are absent from
the repository. They are removed by the repair commit. Their original bytes
remain recoverable from the candidate commit above.

This audit does not weaken the claims already proved in PO-000. It prevents a
second, inconsistent manuscript from silently promoting open obligations.

## Claim-status conflicts

The canonical manuscript and ledger remain authoritative for PO-000. The
candidate packet conflicts with them in the following load-bearing places.

### S7: global trace norm versus overlapping edge tally

- Canonical status: `OPEN / POSSIBLY FALSE`; no equivalence claimed.
- Candidate promotion: “Two-Sided Structural Separation,” marked proved.
- Result: reject the promotion. The finite inequalities and XOR witness may be
  useful, but they do not close the canonical equivalence obligation.

### S11: residual-to-coboundary adapter

- Canonical status: `OPEN PER APPLICATION`.
- Candidate promotion: “Dynamical Independence” plus an asserted quotient
  identity.
- Result: reject. The candidate supplies no typed
  physical-residual-to-cochain adapter and no exactness witness.

### S12: detector adequacy

- Canonical status: `OPEN FOR DECISION USE`.
- Candidate promotion: “Detector Adequacy and Polynomial Measurement
  Complexity,” marked proved.
- Result: reject. Counting local tomography settings does not establish
  adequacy for a protected decision problem.

### G2: higher differential

- Canonical status: `REFUSED / OPEN`.
- Candidate promotion: “Higher Differential Non-Annihilation and Dominance,”
  marked proved.
- Result: reject the status change. A Taylor remainder estimate is not the
  missing higher-cell differential or a proof of its laws.

### C4 / S1: ambient-to-chart bridge

- Canonical status: `OPEN / QUALIFIED`.
- Candidate promotion: a universal non-commuting-bond nonlinearity clause.
- Result: reject. Nonzero projected generator-immersion coupling must be a
  hypothesis or separately proved witness.

## Mathematical blockers in the candidate

1. The affine-chart theorem asserts that any non-commuting bond and chosen
   site variations force a nonzero projected mixed derivative. That does not
   follow from non-commutation alone. The canonical paper correctly requires
   a projected-motion witness.
2. The cochain section concludes
   `Phi1([omega]) = sum_e nu_e` merely because one term is in the image of an
   oblique projection and the other is in its kernel. Trace norm does not make
   those subspaces orthogonal, and no best-approximation theorem is supplied.
3. The product-state set is called a smooth embedded manifold without a rank
   stratum or interior restriction. Density-matrix boundaries require an
   explicit stratified or affine-domain treatment.
4. The pure-state discussion identifies zero normal rate with being an
   eigenstate of the full bond Hamiltonian. The proved condition is the
   vanishing of the normal fluctuation commutator; tangent local motion can
   remain.
5. The candidate uses `Theta(Nt)` where the displayed argument supplies the
   lower-growth direction. Any two-sided asymptotic statement needs its own
   quantified upper bound and uniformity statement.
6. Two generated source locations contain a broken `nu_e` token split across
   lines. A PDF can compile while still rendering the wrong symbol.

## Receipt audit

### Python

The candidate says “59 passed.” Re-execution at the exact candidate commit
collected 59 tests, passed 58, and skipped one optional matplotlib test:

```text
collected 59 items
............................................s..............
```

The existing suite remains green at that scope. It contains no test for the
new three-body witness, the general p-local commutator bound, or the p-local
second-derivative constant. The candidate's claim that
`test_po000_unit.py` verifies those additions is false.

### Lean 4

The twelve files labelled `green_standalone` in `lean4/manifest.json` were
replayed with Lean 4.34.0-rc1 through the repository's `mathlib_lab` host;
all twelve exited zero, and the reported axiom sets stayed within
`{propext, Classical.choice, Quot.sound}`.

That successful replay supports only the declarations named in the manifest.
The package README and canonical claim ledger explicitly state that the
short-time quantum theorem remains prose-proved and that the affine and rate
files are toy or arithmetic cores. No Lean declaration proves the candidate's
new S7, S11, S12, G2, or curved-chart claims.

### Missing artifacts

The candidate audit cites all of the following as if they were present, but
none is tracked at the candidate commit:

- `final_proof.log`
- `final_proof.aux`
- `final_proof.out`
- `.agents/final_proof.tex`

The PDF metadata confirms a 15-page MiKTeX artifact, but a rendered file and a
self-authored “FULL PASS” report do not provide independent mathematical
review.

## Disposition

- Remove `final_proof.tex` and `final_proof.pdf` from the proposed tree.
- Retain this audit as the review receipt explaining the removal.
- Keep PO-000 v6.3 and its ledgers unchanged.
- Admit PO-031 only as a draft boundary note with corrected derivations and
  explicit evidence ceilings.
- Do not claim proof sign-off, publication readiness, or closure of S1, S7,
  S11, S12, G2, or C4 from this packet.

