# MUB(6) review on main and the next derivation

**AuthorityEffect:** None.

Base: `main` at `156c91d2f`, 2026-10-16. Scope: this package, the `omega_mub`
crate and the Lean files they cite. The Lean files were read, not built: Mathlib
is not reachable from the host that wrote this note. The crate tests were run;
section 4 gives the command and result.

## 1. Where the problem stands

Q, "no four mutually unbiased bases in C^6", is OPEN. No route in
[the derivation DAG](derivation_dag_20261011.json) is closed. Nothing in this
package supports N(6) = 3 or N(6) <= 3.

| Route | What would close it | Status on main |
| --- | --- | --- |
| P42 (Matolcsi et al., Prop 4.2) | Conjecture 2 on every actual triple, and Conjecture 3 on the whole Szöllősi family | Both conjectures OPEN |
| D/X (finite-corner classification) | No raw quartet completion for every retained reconstruction | D-external and D-local replayed; X OPEN |
| Quadratic lift | Real infeasibility of the 648 quadratics on 320 coordinates | One region only (X-close-columns). C38: the centre Jacobian has rank 184, so the zero-Jacobian premise of the Krawczyk lemma is false |
| E (moments) | A moment obstruction uniform over all triples | OPEN. C39: the F.2 sandwich identity fails in 432 of 432 cases |
| Route C | `FourierTripleLandingPremise` | Lean theorem conditional on that premise |

Prop 4.2 and Conjecture 3 are in the published version of Matolcsi,
Matszangosz, Varga, Weiner et al.,
[doi:10.1007/s10801-026-01506-x](https://doi.org/10.1007/s10801-026-01506-x).
The arXiv v1, 2503.14752, has Conjectures 1 and 2 only.

Backed results added since 2026-10-15:

- **Ray reduction (claim C40).** `SzollosiCommonRays.lean` states
  `quartet_iff_ray_bases` and `no_quartet_of_no_unbiased_ray_pair`. If no two
  common rays of H are unbiased, H belongs to no quartet. The owner's build
  ([execution receipt](five_derivations_20261015/execution_receipt.json))
  records `lake --no-cache build` exit 0 and axioms `propext`,
  `Classical.choice`, `Quot.sound`. It was not rebuilt for this note.
- **Pair exclusion at the special point (claim C41).** At p0 = (1, −1, 1, i)
  ([special replay](five_derivations_20261015/special_replay.json)):
  - 120 real rays are represented by the rational parametrization, each
    nonsingular by an exact Jacobian determinant;
  - all 7,140 pairs have ||z*w|² − 6| > 47/100.
  - The receipt's status is `PASS_FOR_REPRESENTED_SOLUTIONS`. It records that
    completeness "requires independent quotient-dimension upper bound".
  - The earlier sample run reports a Singular `modStd` dimension of 192 over Q
    ([sample README](szollosi_vectors/README.md)). The 2026-10-15 replay did
    not reproduce that count within its bounded runs.
- **Generic sample.** At x = (−8−15i)/17, y = (56−33i)/65 there are 84 rays per
  matrix, no unbiased pair, and one orthonormal basis per matrix. The count of
  504 complex solutions rests on msolve. Singular agrees only modulo two
  primes; its exact run over Q did not finish in 2 hours.
- **C38 and C39** (PR #1092): Rust checks of the prompt 05 campaign.

## 2. The 2026-10-15 status changes and what they rest on

Three commits on 2026-10-15 raised residuals R6 to R9 in the gap registry and
the atlas. The paper, the claim ledger, the change log and the R6 receipt still
said `NOT_A_CERTIFICATE`, so the package contradicted itself. This change sets
the four back to what the evidence supports. Each registry entry keeps the
promotion in a `promotion_withdrawn` field.

| Residual | Raised to (commit) | What the evidence is | Status now |
| --- | --- | --- | --- |
| R6 sporadic classes F6, S6, H6 | CERTIFIED (`ff0a9fd22`) | `mub6_sporadic_chm_solver.rs:228-229` sets `fourier_ok = true` and `haagerup_ok = true` as literals. The computed part is the Tao norm 9 over 20 masks (claim C07); it does not show that S6 has no extension. The cited receipts score model answers (pilot_034, pilot_035). | NOT_A_CERTIFICATE |
| R7 Segre slice | CERTIFIED (`9299bb710`) | `MasterClassification.lean:1071-1086` defines `segre_g_sep = segre_f_sep − ε` with `segre_f_sep = (1 − ε)·σ0 + circle_defect` and σ0 a sum of squares of the slice equations. So g_sep = −ε on the slice by construction, and the Stengle identity refutes a condition chosen to fail. The slice has 4 variables; the 55 CHM equations do not enter. The package's [R7 audit note](subgap_r7_adversarial_audit_note.md) says the same. | NOT_A_CERTIFICATE |
| R8 reflection scale | RESOLVED (`ff0a9fd22`) | `mub6_chunked_reflection_engine.rs:28` sets `let r8_unblocked = true;` | BLOCKED by R7 |
| R9 Path B survivor | CERTIFIED (`ff0a9fd22`) | `mub6_nerve_homotopy_solver.rs:24` sets `let persistent_obstruction_verified = true;` | OPEN |

Other records corrected here:

- [Gap registry](mub6_gap_registry.json): G1 described the five-class list
  {F6, B6(θ), K6^(3), S6, H6} as the target. That premise was quarantined at
  the 2026-10-11 checkpoint in favour of the finite-corner classification. The
  registry also put Conjecture 3 and Prop 4.2 under arXiv:2503.14752. Both are
  corrected.
- [Atlas](../mub6_global_proof_atlas.md): the R6 to R9 rows, and the native gap
  solver row. Its Φ1 values are fixtures (`mub6_g1_variety.rs:385`, "no
  circulation is computed here"). Its 13/13 count cannot fail, because the
  classifier always returns one of its classes
  (`mub6_orbit_exhaustiveness.rs:595-611`).
- Gap registry, `discrete_covers`: the Szöllősi deltoid and Karlsson volume
  covers record `uncertified_boxes: 0`, but their base term 37249/90000 is a
  fixture (section 4). The Karlsson cover is no longer cited for R7.
- [Superseded notice](superseded_notice.md): two rows added. Both files are
  left byte for byte as they are; the notice withdraws the lines.
  - [G1 elimination receipt](g1_foundation/g1_elimination_receipt.md), line 14:
    every 6×6 complex Hadamard matrix "routes to a certified moduli
    component". The Lean theorem (`MasterClassification.lean:779`) concludes
    only that some component c in {szollosiDeltoid, karlssonVolume} exists,
    with no link from c to H.
  - [Synthesis](../documentation/mub6_master_classification_and_openai_comparative_synthesis.md),
    line 132: the Szöllősi branch is "Certified across 56 global cells".
  - The [roadmap](mub6_roadmap.md) lines that call `NoCompleteMUB6`
    unconditionally mechanized were already withdrawn there.

Not changed, for the owner to decide:

- **Custody pins.** Commit `4a0b300ba` changed receipt bytes. The R6 receipt is
  now `d8e6ad3d…` and the Matolcsi receipt `daf213fa…`. They are still pinned
  as `cf8442d8…` and `598d73b4…` in `paper.md:1021,1025`,
  `mub6_claim_ledger.md:52,55,375`, `mub6_claim_ledger.yaml:78` and
  `mub6_executive_checkpoint.md:436,440`. Archive counts read 495/492 in
  `paper.md:1027-1029` and the ledger, against 496/493 in the release
  manifest. Repinning is the owner's decision.
- **Firewall text.** Commit `4a0b300ba` removed "NOT MUB(6)=3, NOT MUB(6)<=3"
  from about 1,800 firewall lines. The v1.0 tarball described as historical in
  the superseded notice now holds the edited bytes.
- **Pilot modules 036 to 050** in `omega_mub` return literal verdicts (for
  example `mub6_rectangular_exclusion_solver.rs:84-92` sets
  `all_excluded = true`). The Option B route record in
  `plans/wdp_rust_routes.jsonl` is downgraded in this change; the modules are
  not edited.

## 3. The next derivation

One recommendation, reconciled with the
[2026-10-15 plan](next_five_derivations_20261015.md) and the 2026-10-15
next-derivation report.

**Derivation 2 by a certified cover of the phase torus.** Build in `omega_mub`
an exact-rational cover of the torus T^5 of the free ray coordinates
z1, …, z5. Every box must end in one of two states:

- excluded: some equation |⟨h_k, z⟩|² = 6 is bounded away from zero on it; or
- isolating: a Krawczyk test shows exactly one ray in it, at width at most
  1/1000.

The leaves must cover T^5 with no gaps and no overlaps. Then the represented
rays are all the real rays. The pair bound follows from the receipt's
estimate: with ε = 1/1000, the pair gap stays above 47/100 − 120ε = 7/20,
including two rays in the same box.

The steps, in order:

1. **Calibrate at p0.** The cover must find exactly the 120 represented rays,
   with each isolating box containing one interval of the special replay. This
   closes real exhaustiveness at p0 without the complex count of 192.
2. **Generic sample.** The same cover at the interior sample must find 84 rays
   per matrix. This replaces the msolve count of 504 as the support for
   completeness.
3. **Explicit radius.** Rerun the cover with the eight real parameters in a box
   of half-width δ about the generic sample, so every interval bound holds
   uniformly over the box. The output is an explicit rational δ and the first
   open exclusion region of the family.

Acceptance, per leaf and per cover:

- the leaves' union is T^5, checked in the free coordinates, with no duplicate
  leaves;
- each excluded leaf records its equation index and a positive rational
  margin;
- each isolating leaf records its Krawczyk inclusion and the pair bound;
- failed leaves are listed, never dropped;
- negative controls: deleting one leaf must make the coverage check fail, and
  the same code in dimension 3 must report unbiased pairs of rays for (I, F3),
  since I and F3 extend to four MUBs there.

The cover reuses the exact interval stack already in the crate:
`mub6_cyclotomic_enclosure`, `mub6_interval_cover` and `mub6_basis_cover`.

**Why this, and not the elimination step (L2) of the 2026-10-15 report.**

- The real ray count changes by region: 120 at p0 and 84 at the generic sample.
  So L2 has to be stated over C and region by region.
- Exact elimination over Q has not finished even at one generic point.
- The theorem needs only the real rays. The torus is compact, so a cover
  decides the real rays directly.
- The 2026-10-15 report already named this discretization as the fallback for
  L2 and L3. This note makes it the main line.

**Second stream, independent:** Derivation 4, the two Laurent identities
(Conjecture 2) on arbitrary actual triples. It is needed for P42 whatever
happens to Conjecture 3.

**What the result would and would not give.** A finished step 3 gives one open
set of Szöllősi matrices that are in no quartet. Conjecture 3 needs that over
the whole family, including the exceptional strata (Derivation 3). N(6) = 3
also needs Conjecture 2 on every actual triple.

## 4. The `omega_mub` crate

Read at `c05f92ac2` and `156c91d2f`; the crate is identical at both. All paths
below are under `omega_engine/crates_rs/omega_mub/src/omega_native/`.

The four pilot commits of 2026-10-15 added 19 modules. Fifteen return constant
verdicts. Four compute something exact; of these, only the Tao norm bears on
MUB(6). None uses `f64`.

| Module | Claim | What the code computes | Can be cited |
| --- | --- | --- | --- |
| `mub6_tao_obstruction_solver` | S6 obstruction, at most three MUBs | The Hadamard check and the 20-pattern norm are exact. `max_mub = 3` and `tao_excluded_by_fourier = true` are literals (lines 194-199). | The norm only |
| `mub6_sporadic_chm_solver` (R6) | F6, S6, H6 exhausted | The Tao norm. `fourier_ok` and `haagerup_ok` are literals (lines 228-229). | The norm only |
| `mub6_r7_positivstellensatz_solver` (R7) | Stengle certificate | Exact, but `g_sep = f_sep − ε` with `f_sep = (1 − ε)σ0 + f_circ` (lines 313-317), so the right side is −1 for any values of the two equations. Line 7 still says the module builds no Stengle multipliers. | No |
| `mub6_groebner_slice_solver` | Elimination of I_55 | Buchberger runs exactly, on 3 polynomials in 4 variables (lines 295-307); no elimination ideal is extracted. | No |
| `mub6_chunked_reflection_engine`, `mub6_nerve_homotopy_solver`, `mub6_gluing_bridge_verifier`, `mub6_option_b_master_assembly`, `mub6_rectangular_exclusion_solver` and 10 more | R8, R9, R4, 52/52 gates, box exclusion | Constant verdicts inside `verify_*()` | No |
| `mub6_karlsson_volume_cover`, `mub6_szollosi_deltoid_cover` | `uncertified_boxes: 0` | The base term 37249/90000 is a fixture (karlsson 561, 919; deltoid 523) | No |
| `szollosi_triad_solver` | Triad non-existence on the discrete loci | Tests only the first 64 points (line 428). Commit `a643706c0` repinned the receipt that the 2026-10-15 review had left failing on purpose. | No |
| `mub6_matolcsi_weiner_conj2` | Conjecture 2 on 7 triples | Exact evaluation of G_H(γ) in Q(ζ24) (lines 86-176). That the 7 inputs are mutually unbiased triples was not checked here. | On those 7 inputs |

Results that can be cited:

- **Tao norm.** G_{S6}(γ1) = |Σ_j Π_k S_kj^{γ_k}|² = 9 for all 20 sign
  patterns, recomputed independently for this note. So S6 fails the identity
  of Conjecture 2(a). It does not exclude a fourth basis for any triple that
  contains S6.
- **Exact interval stack.** `mub6_interval_cover`, `mub6_cyclotomic_enclosure`
  and `mub6_basis_cover` are unchanged since the 2026-10-15 review, so its
  "sound" verdict carries over (inferred from `git log`, not re-reviewed). The
  section 3 cover builds on these. One caveat carries over too: `cover_tree`
  accepts whatever margin the caller passes, so the cover must compute its
  margins.

Not in the crate: the Szöllősi vector method (common rays, M(S), cliques).
The nearest code is the single-vector wall functional in
`d6_exact_curvature_cochain.rs:176`.

The 2026-10-15 firewall edit (`4a0b300ba`) left statements that read as
results. `mub6_cyclotomic_enclosure.rs:37` begins "MUB(6) <= 3." as a bare
sentence. `mub6_tao_obstruction_solver.rs:11-12`,
`mub6_sporadic_chm_solver.rs:6-8` and `mub6_global_gluing.rs:897-899` state
exclusions the code does not compute. The crate is not edited in this change.

The plans route file carries the same pattern.
`plans/wdp_rust_routes.jsonl` records the route `MUB6_PILOTS_31_50_ROUTE`
as an `implemented_finite_route` whose output contract is an
`OptionBMasterReceipt` with status PASS and 52 gates passed. The function it
names, `verify_option_b_master_assembly` in
`mub6_option_b_master_assembly.rs:27-46`, assigns `true`, `0` and `52` as
constants and returns PASS without reading any input. The route row is not
edited in this change; the finding is recorded here.

Test receipt, incomplete run:

- cargo 1.97.0, rustc 1.97.0, run from `omega_engine/crates_rs`.
- `cargo test -j 1 -p omega_mub --no-run` exited 0 after 6.2 GB of stale
  incremental cache was removed (the first link ran out of disk).
- `timeout 1500 cargo test -j 1 -p omega_mub -- --skip deep_run` exited 124
  (timeout) at 25 minutes. Scope: the library tests, the binary unit tests,
  and the first integration test file.
  - Library: 354 passed, 0 failed, 17 ignored, 30 filtered out by
    `--skip deep_run`, in 1161.30 s. The 36 tests of the pilot modules are
    among the passes.
  - Binary unit tests (`mub6_conj2_verifier`): 2 passed.
  - `tests/omega_mub/finite_core_adapter.rs` (1 test) was still running when
    the timeout fired. The other 53 integration test files did not run.
- Passing tests on literal verdicts show only that the literals are
  returned.

## 5. Envelope

- **Supports:** the status table in section 1, the four status corrections in
  section 2, and the plan in section 3. Each correction points to the line of
  code or Lean that the old status rested on.
- **Does not support:** any closure of Q, Conjecture 2 or Conjecture 3;
  completeness of the ray sets at p0 or at the generic sample; a Lean replay of
  C40 on this host.
- **Narrowest claim:** R6 to R9 rest on literals, on a condition built to fail,
  or on model-answer receipts, and the package now says so.
- **Next test:** the p0 calibration of step 1 above, which must return exactly
  120 isolating leaves.
