# FRONTIER — fable_hilbert_walk_20260819

**AuthorityEffect:** None.

## Strongest proved theorem

`FableHilbertWalk20260819.H017.finite_hilbert_boundary`
(axioms: `{propext, Quot.sound}`), whose conjunction contains,
verbatim as conjuncts:

1. the permutation-*isometry* envelope for every coefficient pack,
   enumeration, and reversible map (the general
   `H006.permutation_isometry` statement itself — obligation 1;
   invertibility separate as `H006.permU_left_inverse` /
   `permU_right_inverse`; the isometric-automorphism reading of
   "unitary" over the Int positive-definite host is
   `permU_isometric_automorphism_over_posdef`);
2. the phase fiber holds distinct states with equal L1 data
   (`H009.relative_phase_in_fiber` — obligation 2 content via
   `H008.equal_weights`);
3. a supplied mixing presentation separates that fiber and does
   not factor through it (`H010.mix_separates`,
   `H010.no_descent_through_fiber` — obligations 3–4);
4. the obstruction runs over ℤ on the sign group alone
   (`H010.int_no_descent`) — complex phase NOT selected;
5. a positive quartic rival readout, not a rescaling of the
   quadratic one, disagrees pointwise (`H013.quartic_rival`
   conjuncts; `H013.quartic_not_proportional`) — but at a
   *different* total (17 vs 5), so this is NOT a
   same-normalization-contract Born non-uniqueness (open O-6); it
   shows only that the quadratic rule is not the unique positive
   scale-distinct readout;
6. an entanglement witness — the tensor host carries a non-product
   vector while the direct-sum host is exhausted by its component
   embedding (`H014.bell_not_product`,
   `H014.sum_component_embedding_surjective`), structurally
   inequivalent rules; tensor "not forced" is NOT proved (open
   O-5 / R6c);
7. no isometric collapse on the declared basis, and two distinct
   reversible dilations share one reduction
   (`H015.collapse_no_isometry`, `H015.same_reduction`,
   `H015.dilations_distinct` — obligation 8);
8. no report-level half-step, amplitude interpolants exist at
   declared scale 4, and they are not unique
   (`H016.no_report_half_step`,
   `H016.sqrtSwap_squares_to_scaled_swap`,
   `H016.interpolant_not_unique` — obligation 10).

The mechanical route reached exactly the work order's anticipated
ceiling — a permutation-*isometry* envelope (not a Hilbert
unitary; see H006) plus a phase non-descent obstruction — and
made concrete a direction the order left generic: the anticipated
rival-carrier countermodel is realized over ℤ at the interference
rung itself. A smaller host artifact, honestly bounded: the
off-the-shelf ℚ route in this Lean core is `Classical.choice`-
tainted (the `ratPack` receipts), so a clean ℚ is an explicit
cost — NOT an impossibility (a choice-free ℚ is reprovable, R5).

## Hard-obligation status (honest, corrected review round 3)

The ten work-order obligations are NOT all discharged as direct
theorems. Precise status:

- **Discharged as theorems (7):** #1 bijection→isometry
  (`permutation_isometry`, + posdef automorphism; "unitary" only in
  the host-weakened sense, see H006), #2 phase-blind identifies
  equal-modulus (`equal_weights`), #3 mixing separates
  (`mix_separates`), #4 non-factorization (`no_descent_through_fiber`),
  #5 global vs relative phase (`global_phase_in_fiber`,
  `relative_phase_in_fiber`), #7 determinism≠reversibility
  (`collapse_not_reversible`), #8 non-bijective has no same-basis
  isometry (`collapse_no_isometry`).
- **Discharged in a host-WEAKENED form (1):** #6 asks for H000–H006
  over ℝ; ℝ is unavailable in this host, so it is carried over
  **Int** (`real_pipeline_complete`). The spirit (a real-like
  carrier without i shows ℂ is not selected below H007) holds; the
  letter (over ℝ) does not.
- **Discharged as "hypotheses named/imported", not a Born theorem
  (1):** #9 asks to identify Born-uniqueness hypotheses and bind or
  mark imported; `GleasonPack` marks them imported. The rival-readout
  side is only a positive non-proportional readout, NOT a
  same-contract non-uniqueness (open O-6).
- **Discharged as "assumptions named", not a continuum theorem (1):**
  #10 names the exact continuum imports (topology, one-parameter
  group, Stone) via H016; the passage itself is not taken (R8).

So: 7 direct theorems, #6 host-weakened, #9/#10 as named imports.
The `ImportLedger` in H017 is hand-set METADATA (rfl over Bool
flags), not a theorem-bound gate; the binding is the named theorems.

## Exact open residues, classified and ordered by estimated cost

| id | residue | class | estimated cost / next step |
|----|---------|-------|---------------------------|
| R0 | **Connected end-to-end threading**: thread one `PresentedCarrier`/report object from H000 through the scaled-integer simplex shadow, dynamics, linearization, inner product, isometry, complexification, phase-blind, and interference rungs, so the capstone is a derivation over one object rather than a conjunction of fixtures. `HWThread.phaseBlind_intertwines` is the first genuine thread (dynamics/isometry/pushforward over one τ), but its Bool specialization reuses only H000's `enumQ`. | theorem work (re-architecture) | HIGH — the primary structural gap; most rungs are already parametric over the report set Q, so the work is re-instantiating them at one shared carrier and proving the connecting squares |
| R1 | Parseval-type scale law for the mixing map in general (only witness-level total-doubling proved) | theorem work | LOW — one list-algebra lemma over the pack; extend `rsum_map_add` |
| R2 | O-2: does the quartic rival survive a dimension-2 noncontextuality axiom? | finite search | LOW-MED — enumerate frame functions on the 2-dim host; a finite check either kills the rival under the axiom or exhibits it surviving |
| R3 | O-1: a selector theorem excluding the sign carrier under a strict subset of QM_062's assumptions | theorem work | MED — formalize the composition law on the phase carrier and test the 4-unit group Z[i]* vs {±1}; the walk predicts {±1} survives holonomy-free transport and dies only under a connectedness-type import |
| R4 | Sub-envelope classification: which isometries of the ℤ[i] host ARE permutation lifts (a finite classification at n = 2) | finite search | MED — enumerate the finite isometry group of the scale-preserving maps on (ℤ[i])²; classify by basis action |
| R5 | O-3: a choice-free dense coefficient carrier (rebuild ℚ inside the campaign with clean lemmas) | theorem work | MED-HIGH — mechanical but large; would upgrade H001 from scaled-integer to genuine rational masses under policy |
| R6a | Count the reversible dilations of the identity on Bool×Bool (the literal sharpening of `H015.dilations_distinct` into a count) | finite search | LOW — finite enumeration |
| R6b | Formalize an ancilla-preparation convention and classify (or refute) reversible dilations of the collapse map under it (open obligation O-4) | finite search + author choice | LOW-MED — convention first, then enumeration |
| R6c | Tensor "not forced": define the composition interface precisely and either exhibit a same-interface rival (direct sum) or show tensor is forced (open O-5) | theorem work | MED — interface definition first |
| R6d | Same-contract Born non-uniqueness (open O-6): formalize a division-free fixed-scale normalization contract and exhibit two effect-bearing readouts meeting it that differ (expected achievable at dimension 2, where Gleason fails) | theorem work | MED — contract definition first |
| R7 | Born uniqueness under the full Gleason package | literature import | HIGH — dimension ≥ 3 host plus σ-additivity machinery; out of scope for the self-contained host |
| R8 | Continuum passage (topology, one-parameter group, Stone) | literature import / author choice | HIGH — requires an analytic host; the finite walk can only price it, which H016 does |

## Next cheapest separating experiment

**R2** (quartic rival vs dimension-2 noncontextuality): a fully
finite computation on the existing host. If the rival survives, it
gives a sharp local statement — "at dimension 2, positivity +
normalization + noncontextuality still do not pin the quadratic
rule" — matching Gleason's own dimension restriction with a
constructive witness. If it dies, the walk gains a genuine
dimension-2 uniqueness theorem under a named axiom. Either outcome
is a result.

## Negative results that count as results

- Determinism ≠ reversibility (`H003.collapse_not_reversible`).
- Selected-representative descent checks are refuted by the trunk
  model (`E018` replay).
- The permutation-isometry envelope is strictly smaller than the
  isometry group (`H006.swapI_not_permutation`); "unitary" holds
  only up to the Int positive-definite specialization
  (`permU_isometric_automorphism_over_posdef`), and not as a
  Hilbert-space unitary.
- The interference witness cannot select the complex carrier
  (`H010.int_no_descent`).
- The off-the-shelf ℚ route in this Lean core is
  Classical.choice-tainted (`ratPack` receipts) — a priced import
  cost, not an impossibility (a choice-free ℚ is reprovable, R5).

**AuthorityEffect:** None.
