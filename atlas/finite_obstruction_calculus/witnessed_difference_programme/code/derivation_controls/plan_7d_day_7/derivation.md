# Derivation Control: PLAN-7D-DAY-7 (Linked Delivery Report & Independent Audit)

**AuthorityEffect:** None.

## 1. Scope and Claim

This finite control and linked delivery report (`PLAN-7D-DAY-7`) audits the 7-day execution campaign across Lanes A–E, the built Rust executables, the actual cost ledger, and all 50 Symbol Game (`SG-01`..`SG-50`) episode dispositions.

## 2. Five-Lane Endpoint Inventory (Lanes A–E)

| Lane | Written Anchor | Lean 4 Scope | Python / Certificate Scope | Native Rust Scope | Open / Out-of-Scope Obligations |
|---|---|---|---|---|---|
| **Lane A** | `docs/guarded_history_coherence.md` | `lean4/WitnessedDifference/GuardedHistoryCoherence.lean` (`guarded_history_coherence_axioms.txt`: `propext`, `Quot.sound`, `Classical.choice`, 0 `sorry`) | `code/causal_certificates/guarded_{compatible,p18,three_pairs}_{problem,certificate}.json` (`24, 30, 90` linear extensions) | `omega_wdp::genesis_guarded_history`, `src/bin/wdp_guarded_history.rs` | Arbitrary unbounded poset widths beyond the certified finite causal problem instances |
| **Lane B** | `docs/realizable_observation_calculus.md` | `code/realizable_observation/RelationLaws.lean` (`lean_check.txt`: 5 relation algebra laws, 0 custom axioms) | `code/realizable_observation/{core.py,replay.py,checker.py,finite_replay_v3.json}` (`15/4, 4, 6, 7/2`, 12 hostile controls) | `tests/omega_wdp/derivation_controls/{plan_7d_next_2.rs,plan_7d_day_4.rs}` | Continuous-state sensor models beyond finite transition/report tables |
| **Lane C** | `docs/rejection_reuse_calculus.md` | `code/rejection_reuse/rejection_reuse.lean` (`propext`, `Quot.sound`, `Classical.choice`, 0 `sorry`) | `code/rejection_reuse/trace_checker.py` (9-state image carriers $X_0, X_1, X_2$, 15-step trace cost $17 \le 18$) | `tests/omega_wdp/derivation_controls/{plan_7d_next_2.rs,plan_7d_day_4.rs}` | Reuse across non-bijective or uncertified coordinate transforms |
| **Lane D** | `docs/native_future_compression.md` | `lean4/WitnessedDifference/NativeFutureCompression.lean` (`native_future_compression_axioms.txt`: standard axioms, 0 `sorry`) | `code/derivation_controls/plan_7d_day_4/witness.py` (`1 + 15 + 495 + 29260 = 29771` classes at `(3, 4, 2)`) | `omega_wdp::genesis_future_compression`, `tests/omega_wdp/derivation_controls/plan_7d_day_4.rs` | Horizon/term/count parameters outside the declared `(max_terms=3, max_count=4, horizon=2)` envelope |
| **Lane E** | `docs/lane_e_character_duality_completion.md`, `docs/protected_subgroup_character_quotients.md` | Finite abelian group & quotient character separation (`LE-1`..`LE-4`, `PQ-1`..`PQ-6`) | `code/derivation_controls/{plan_7d_day_3,plan_7d_day_5}/witness.py` (cyclic orthogonality, $\mathbb{F}_p^n$ rank, CRT $\mathbb{Z}/6^n\mathbb{Z}$, dyadic $x_n$) | `tests/omega_wdp/derivation_controls/{plan_7d_day_3.rs,plan_7d_day_5.rs}` | Full locally compact infinite-group Pontryagin-van Kampen duality (`MATH-100`) remains open |

## 3. Binary Responsibilities and Campaign Spend Ledger

- **Declared Rust Executables**:
  - `omega_engine/crates_rs/omega_wdp/src/bin/genesis_extension.rs`: evaluates finite boolean graphs, machine prefixes, incidence chain complexes, metric/sheaf reports, and signed transport packets.
  - `omega_engine/crates_rs/omega_wdp/src/bin/wdp_guarded_history.rs`: emits canonical `wdp-guarded-coherence-v1` certificates and exits with status `2` (`REFUSE`) on malformed or cyclic inputs.
  - Native build receipt: `code/causal_certificates/native_build_receipt_guarded_2026_10_06.json` (`binary_sha256 = b37105dc9c58603b239bf1678af641c4f23bf5f23738642a97fd420853e27dcf`).
- **Actual Cost Ledger**:
  - Offline verification spend: `\$0.00` (`paid_dispatch_enabled = false`).
  - Configured caps preserved: `\$0.20` single-pilot cap, `\$20.00` campaign ceiling.

## 4. Complete 50-Episode Disposition Table (`SG-01`..`SG-50`)

- **Local Staged Controls Passed (`2 / 50`)**:
  - `SG-40`: `LOCAL_STAGED_CONTROL_PASS` (`code/derivation_controls/sg_40/witness.py`, `sg_40.rs`)
  - `SG-48`: `LOCAL_STAGED_CONTROL_PASS` (`code/derivation_controls/sg_48/witness.py`, `sg_48.rs`)
- **Live Paid Provider Episodes Not Run (`48 / 50`, Explicitly `NOT_RUN`)**:
  - `SG-01`, `SG-02`, `SG-03`, `SG-04`, `SG-05`, `SG-06`, `SG-07`, `SG-08`, `SG-09`, `SG-10`,
  - `SG-11`, `SG-12`, `SG-13`, `SG-14`, `SG-15`, `SG-16`, `SG-17`, `SG-18`, `SG-19`, `SG-20`,
  - `SG-21`, `SG-22`, `SG-23`, `SG-24`, `SG-25`, `SG-26`, `SG-27`, `SG-28`, `SG-29`, `SG-30`,
  - `SG-31`, `SG-32`, `SG-33`, `SG-34`, `SG-35`, `SG-36`, `SG-37`, `SG-38`, `SG-39`, `SG-41`,
  - `SG-42`, `SG-43`, `SG-44`, `SG-45`, `SG-46`, `SG-47`, `SG-49`, `SG-50`: `NOT_RUN` (open live provider benchmark obligations `SG-01..39`, `SG-41..47`, `SG-49..50` remain open and are not promoted).

## 5. Non-Claims

- This audit report does not promote any `NOT_RUN` live episode to `PASS` and does not claim empirical LLM capability from offline deterministic controls.
