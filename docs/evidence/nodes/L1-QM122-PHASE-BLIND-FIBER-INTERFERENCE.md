# L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over Z\[i\] with the unnormalized two-sector Hadamard readout (|a+b|^2, |a-b|^2): for any nonzero Gaussian amplitudes a, b no function of the phase-blind weights (|a|^2, |b|^2) determines the readout on the product of the weight fibers (rotation by i or by -1 suffices); mixing doubles the total weight and the readout difference is 4 Re(a conj b); a zero first or zero second sector makes the readout descend. The source witnesses (1,1)/(1,-1) are instances. Complex Hilbert amplitudes, normalized or projective states, more than two sectors, other mixes and the link to the Vec GaussInt Bool declarations (H008/H010) are not covered.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- distinct cited Lean declarations covered by a current replay receipt: 13
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- unit phases: assumption

## Bottleneck

Z\[i\] -\> C embedding and the identification with the source H008/H010 declarations are not formalised; normalized/projective readout with n\>=3 sectors and non-Hadamard unitary mixes are open.

## Source status

QM_122 ledger LEAN4_PROOF; file headers: 'Candidate only. Not PROVEN' (H013 headers); build not rerun by me

## Review

- PFP review: [dag/results/L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Over Z\[i\] with the unnormalized two-sector Hadamard readout: both sector amplitudes nonzero implies the weight pair does not determine the readout; a zero first or zero second sector implies it does.
  - does not support: Complex-Hilbert amplitudes beyond Z\[i\]; normalized or projective states; more than two sectors; mixes other than the unnormalized 2x2 Hadamard; the embedding of Z\[i\] into C (non-descent on the Gaussian-lattice fibers gives non-descent on the full complex phase fibers only after that embedding is formalised); the identification of the module readout with the source declarations phaseBlind/mix/readout over Vec GaussInt Bool (H008/H010), which is a modelling identification, not a checked one; any measurement, branch or physical interpretation of the phase fiber.
  - next test: Decide non-descent of the normalized projective readout w(a+b)/(2(w(a)+w(b))) for n\>=3 complex sectors under a unitary mix other than the 2x2 Hadamard, by exhibiting a fiber pair with different readouts or a descending fiber.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/HilbertWalkPhaseBlindPresentation.lean`

- file: [lean4/HilbertWalkPhaseBlindPresentation.lean](../../../lean4/HilbertWalkPhaseBlindPresentation.lean)
- sha256 (`bytes`): `e7ca49b4ca6cd26239b024ee0f171bba8b978d4d0b3eebb8ab99f9068b8cee04`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkPhaseBlindPresentation`): recorded sha256 `e7ca49b4ca6cd26239b024ee0f171bba8b978d4d0b3eebb8ab99f9068b8cee04` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkPhaseBlindPresentation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `phase_blind_presentation` | yes | yes | yes | propext | `#print axioms phase_blind_presentation` |

- counts toward the grade: yes

### Lean: `lean4/InterferenceNonDescent.lean`

- file: [lean4/InterferenceNonDescent.lean](../../../lean4/InterferenceNonDescent.lean)
- sha256 (`bytes`): `a7247e052643452607f54ef0efa5ea98df3dc763e0620558ca81080fa73eca94`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `InterferenceNonDescent`): recorded sha256 `a7247e052643452607f54ef0efa5ea98df3dc763e0620558ca81080fa73eca94` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound; only standard axioms: yes
- check: `cd lean4 && lake build InterferenceNonDescent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mix_separates` | yes | yes | yes | none | `#print axioms mix_separates` |
| `no_descent_through_fiber` | yes | yes | yes | Quot.sound | `#print axioms no_descent_through_fiber` |

- counts toward the grade: yes

### Lean: `lean4/PhaseBlindFiber.lean`

- file: [lean4/PhaseBlindFiber.lean](../../../lean4/PhaseBlindFiber.lean)
- sha256 (`bytes`): `302e3a2da088ad7de12570522d30a4bbd1f5c03099a22d4b7ff6be6baa75ad6d`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (PhaseBlindFiber)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `PhaseBlindFiber`): recorded sha256 `302e3a2da088ad7de12570522d30a4bbd1f5c03099a22d4b7ff6be6baa75ad6d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PhaseBlindFiber`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PhaseBlindFiber.descends_when_second_zero` | yes | yes | yes | propext | `#print axioms PhaseBlindFiber.descends_when_second_zero` |
| `PhaseBlindFiber.descends_when_zero_sector` | yes | yes | yes | propext | `#print axioms PhaseBlindFiber.descends_when_zero_sector` |
| `PhaseBlindFiber.fiber_changes_readout` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.fiber_changes_readout` |
| `PhaseBlindFiber.no_descent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.no_descent` |
| `PhaseBlindFiber.phase_blind_fiber_interference` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.phase_blind_fiber_interference` |
| `PhaseBlindFiber.readout_interference` | yes | yes | yes | Quot.sound, propext | `#print axioms PhaseBlindFiber.readout_interference` |
| `PhaseBlindFiber.readout_total` | yes | yes | yes | Quot.sound, propext | `#print axioms PhaseBlindFiber.readout_total` |
| `PhaseBlindFiber.w_I_mul` | yes | yes | yes | Quot.sound, propext | `#print axioms PhaseBlindFiber.w_I_mul` |
| `PhaseBlindFiber.w_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PhaseBlindFiber.w_eq_zero` |
| `PhaseBlindFiber.witness_readouts` | yes | yes | yes | none | `#print axioms PhaseBlindFiber.witness_readouts` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0310_finite_hilbert_boundary_from_a_presented_carrier.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0310_finite_hilbert_boundary_from_a_presented_carrier.md](../../../dag/derivations/09_finite_hilbert/tfq_0310_finite_hilbert_boundary_from_a_presented_carrier.md)
- sha256 (`lf-normalised`): `67fd961bf04a6879f486db996d6a2e24b6db5a2ff2f2cd33a7669cc387dc22d7`
- generated view: listed, not counted
- cited in: record TFQ-0310
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:86710ba8ef7db719a42a2165e71d3bc72ac5db63d0b2a51e57f48f14e137754e`
- `external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6::discrete_fiber`
- `external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6::phase_blind_projection`

## Absences recorded by the TFQ records

- TFQ-0310 python: no local python twin located for sources/atlas/papers/quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py
- TFQ-0310 rust: no local rust twin located for external:sha256:904a09d9ca4b18f97838457416046361842e537e895afce0374f8b6c670a1ef1
- TFQ-0310 rust: no local rust twin located for external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6

## Routes

Incoming (1):

- `L1-R-PHASE-BLIND-INTERFERENCE` `DERIVED_LEAN`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE), [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `L1-R-MNC-LEFTOVER` `GAP_NO_DERIVATION`: [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) (OPEN)
- `X-R-PHASE-BLIND-TO-FQ-FIBER` `DERIVED_LEAN`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)
