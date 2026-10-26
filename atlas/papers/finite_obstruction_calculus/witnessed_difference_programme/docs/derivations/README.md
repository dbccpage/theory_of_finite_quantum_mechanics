# Active derivation supplements

The [literal Genesis construction](genesis_construction.md) is a development
increment connecting the existing Rust primitives to WDP: literal `<>`,
checked replay, typed histories, explicit cell admissions, and computed
homology. Its provisional choices and remaining proof obligations are listed
there; it is not yet part of a rebuilt manuscript release.

These seven documents are the full proof supplements for the finite-dimensional
algebraic constructions summarized in §17.7–§17.11 and Chapter 19A of
[`witnessed_difference_programme.md`](../../witnessed_difference_programme.md).
They have been moved from the paper root to keep the release layout readable.
They remain active evidence-bearing documents, rather than historical source
material that can be deleted.

| Supplement | Main-text integration | Additional material retained here |
|---|---|---|
| [Generative histories and contextual compression](generative_histories_contextual_compression_derivation.md) | §17.7, first paragraph; theorem map R7 | Typed-history construction, universal property, current-answer counterexample, cochain-shadow limits, and replay scope |
| [Additive and tensor completion](additive_tensor_completion_derivation.md) | §17.7; `GEN-WDP-58` and `GEN-WDP-59` | Full universal-property proofs, information-loss boundaries, non-pure tensor witness, and evidence contract |
| [Dagger and observer pairing](dagger_observer_pairing_derivation.md) | §17.8; `GEN-WDP-60` and `GEN-WDP-61` | Descent hypotheses, nonselection theorems, rank-one obstruction, and bounded replay scope |
| [Finite Hermitianization](finite_hermitianization_derivation.md) | §17.9; `GEN-WDP-62` and `GEN-WDP-63` | Complete scalar and pairing proof, refusal examples, certificate format, and completion boundary |
| [Finite states, effects, and readout](finite_state_effect_readout_derivation.md) | §17.10; `GEN-WDP-64` and `GEN-WDP-65` | Gram-factor certificate language, full trace proof, readout nonselection, and adversarial controls |
| [Finite process composition](finite_process_composition_derivation.md) | §17.11; `GEN-WDP-66` through `GEN-WDP-68` | Composition proofs, instrument countermodel, exact-gate boundary, and Bell/computation dependency map |
| [Certified preservers and algebraic generators](certified_preserver_derivation.md) | Chapter 19A; theorem map R12–R13 | Global coordinate proof, corrected phase group, norm-class reachability, postselection, qubit boundary, Galois/bicommutant/count laws, and inner generators |

The manuscript states the central results and scope fences. These supplements
retain the longer proofs and the exact relationship among prose, Lean, Python,
and retained receipts. Moving a supplement does not promote executable evidence
to a general proof or expand any physical claim.
