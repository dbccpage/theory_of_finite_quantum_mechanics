# Prompt 05 campaign: claims checked in Rust

**AuthorityEffect:** None.

**Firewall line:** NOT MUB(6)=3, NOT MUB(6)<=3; stated region only; mints no
authority.

Prompt 05 (`prompt_05_mub6_triadic_adversarial_operad_n6_equals_3`) ran for four
rounds on 2026-10-16, on the owner's machine. A local agent then wrote a
checkpoint at commit `fbeae2882` with a dirty working tree. In that
normalization two statuses were raised: `VERIFIED_LOCAL_RESULT` became `PROVED`
and `SOURCE_REPORTED_UNREPLAYED` became `CONDITIONAL`. The model's own text
does not support either change.

This note records each claim at the status the code in this repository
supports. It does not use the checkpoint's statuses. The campaign's verdict
stands: N(6) >= 3 is exact, and N(6) = 3 is open.

## Code and rerun

- `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_balanced_table_replay.rs`
  parses the pinned table
  `artifacts/balanced_quadratic_coefficients_20261011.jsonl` (SHA-256
  `cb552359…c217d`). It regenerates all 648 rows from the definitions in
  `MubBalancedQuadraticPolynomials.lean` and `MubQuadraticLiftPolynomials.lean`
  and compares them with the table term by term over Q. Points are evaluated
  in Q(ζ24).
- `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_prompt05_campaign_checks.rs`
  holds the negative controls, the Jacobian at the centre of the box, and the
  local lemmas D1, D2, D3, D9, E.1, F.2 and G.
- The tests are in
  `omega_engine/crates_rs/tests/omega_mub/test_mub6_prompt05_campaign_checks.rs`
  (8 tests). The receipt is
  `artifacts/mub6_prompt05_campaign_receipt.json`, and one test
  compares it with a fresh run.

```text
cd omega_engine/crates_rs
cargo test -j 1 -p omega_mub --test test_mub6_prompt05_campaign_checks
cargo run -j 1 -p omega_mub --bin mub6_prompt05_campaign_checks -- \
  ../../omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts/balanced_quadratic_coefficients_20261011.jsonl \
  <fresh output path>
```

The checkpoint suggested `omega_mub_verify_all` as the negative control. That
binary does not evaluate the balanced table, so the controls below come from
the new binary.

## Next step B-0.1 and B-0.2

- **Scope of `Quartet`.** The predicate is global, not tied to a family. It is
  defined at `lean4/research_programs/mub6/SzollosiQuartetSystem.lean:33` as
  `def Quartet (B : Fin 4 → Candidate) : Prop :=`. The chain to the table is
  written in Lean source:
  - `exists_quartet_iff_balanced_polynomials` (`MubBalancedQuadraticPolynomials.lean:84`);
  - `exists_quartet_iff_coded` (`MubBalancedCodedSystem.lean:64`);
  - `exists_quartet_iff_table` (`MubBalancedTable.lean:915`).

  None of these was elaborated here, because Mathlib cannot be reached from
  this environment. D5 stays **CONDITIONAL** until `lake build` and
  `#print axioms` run on the owner's machine.
- **Table against its definitions.** The 648 rows equal their regeneration.
  The table has 8313 terms, at most 676 in one row. It has 42 empty rows:
  23 gauge modulus rows and 19 Gram rows. The blocks are:
  - moduli: rows 0 to 107;
  - Gram: rows 108 to 323. Of these, 90 are upper entries and 90 are
    Hermitian duplicates. There are 18 zero imaginary diagonals, and 18 real
    diagonals that equal sums of modulus rows;
  - graph: rows 324 to 539;
  - transition moduli: rows 540 to 647.

  A changed coefficient is reported by its row number, and changed or
  truncated bytes are refused. This check compares the table with an
  independent Rust transcription of the definitions. It does not replay the
  Lean equivalence.
- **Comparison with the campaign's blocks E1 to E4.** The table has 108
  modulus rows, not 85. Its Gram block has 216 rows, not 90 unitarity rows. It
  has 216 graph rows and 108 transition modulus rows. The campaign's inventory
  came from the prompt, not from the table.
- **OBL-3, the box.** The box is not [-1, 1]^320. It is [-1, 1] on the 170
  slot and D-block coordinates, and ±10035/4096 on the 150 core coordinates.
  This matches `MubBalancedTable.lean`, `def bounds`. The cores store the
  transitions without the 1/6 scaling: their entries have modulus √6, and
  10035/4096 > √6.
- **OBL-4, negative controls.** We set B3 := B1 and B3 := B2 at the product
  triple. In each case exactly the 36 transition modulus rows of the repeated
  pair are nonzero: rows 576 to 611, and rows 612 to 647. Their values lie in
  {-6, 30}. Every other block vanishes. Five core coordinates of each control
  lie outside the box.

## Statuses

| Claim | Checkpoint | Status here | What backs it |
|---|---|---|---|
| D1, N(6) >= 3 by `I, H/√6, U/√6` | PROVED | Exact computation | Entries unimodular in Q(ζ12), Gram 6I, all normalized cross overlaps 1/6 |
| D2, permutation decoys | PROVED | Exact computation | Overlap sets {0, 1}, {0, 1}; the six-dimensional σz seed gives {0, 1/3} |
| D3, Gram spectrum | PROVED | Exact computation | Multiplicities 4^1, 1^20, 0^3, read from exact ranks. The description of the nullspace and "excludes no quartet" are hand statements |
| D4, Krawczyk containment | PROVED | Hand lemma, unmechanized | Its stated premise is false for this table: the Jacobian at the centre of the box is not zero (see below) |
| D5, quartet iff coded box solution | CONDITIONAL | CONDITIONAL | Lean source chain above, not elaborated here; Rust checks the table against its definitions |
| D9, 180 residuals in 72 coordinates | CONDITIONAL | Exact computation; premise refuted | 180 = 108 overlap rows + the 72 real components of B3^H B3 - I. 42 are implied by the others, so 138 are not. No row of B3 B3^H - I is listed (OBL-5 answered: no) |
| E.1, no affine-multiplier certificate | PROVED | Moments checked; closing step by hand | Under a four-point design on each entry, all 252 × 73 = 18396 expectations are zero. The design matches the circle measure on every moment of degree at most three. A degree-two multiplier has nonzero expectation. Scope: the fixed triple, multipliers of degree at most one |
| F.2, trace-level hierarchies feasible | PROVED | Exact computation | The commutative model on {1..6}^4 is idempotent, orthogonal and complete, with traces 1/6 and 1/36. It violates `P_ai P_bj P_ai = P_ai / 6` in 432 of 432 cases |
| G, gauge and coordinate count | PROVED | Count and balance checked; rest by hand | 320 = 152 slot + 18 D-block + 150 core, and the product triple is balanced. The 1152-element symmetry group (OBL-6) and "no positive-dimensional symmetry" are not checked |
| X, N(6) = 3 | OPEN | OPEN | No exclusion cover, sum-of-squares or NPA certificate, or contraction exists |
| NB-9 | REFUTED | REFUTED, not used | Not an antecedent anywhere |
| arXiv:2608.18053 | cited | MISSING | Not pinned (OBL-10) |

## The walls

1. **Interval branch-and-bound over 320 coordinates (Route D).** The
   campaign wrote that J(0) = 0 at the centre of the box. The table has 1045
   terms of degree one: 100 Gram, 720 graph and 225 transition modulus. They
   lie in 269 rows. The exact rank of J(0) over Q is 184 of 320. So J(0) is
   not zero, but J(0)^T J(0) is singular, and the Moore–Penrose
   preconditioner the campaign named is still undefined at the centre. No leaf
   record, preconditioner or finite subdivision bound exists for a box of
   dimension 320.
2. **Moment and sum-of-squares relaxations (Routes E and F).** A level-two
   moment matrix in 320 variables is 51,681 × 51,681, since C(322, 2) = 51,681.
   No certificate exists at any level. E.1 blocks multipliers of degree at most
   one on the fixed triple only. It says nothing about degree two, or about the
   320-coordinate system. F.2 shows that relations at trace level alone admit a
   commutative model, so the operator identity must be included. Any
   certificate that uses it would hold in every dimension 6k.
3. **Family versus global scope.** `Quartet` is global, but the bridge from it
   to the table is Lean source that has not been replayed. Results covering one
   family of Hadamard matrices do not carry over to the global predicate
   without that bridge.

## What needs the owner's machine

- Run `lake build` on `MubBalancedQuadraticPolynomials`,
  `MubBalancedCodedSystem` and `MubBalancedTable` in
  `lean4/research_programs/mub6`.
- Run `#print axioms` for `exists_quartet_iff_coded` and
  `exists_quartet_iff_table`. The campaign reports `[propext,
  Classical.choice, Quot.sound]` without having seen the output.
- Then bind the Rust table identity to the kernel result. The goal is
  `MUB6-P05-KERNEL-REPLAY` in `plans/goal_dag.jsonl`.
