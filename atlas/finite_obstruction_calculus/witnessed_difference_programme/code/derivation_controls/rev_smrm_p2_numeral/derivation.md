# REV-SMRM-P2-NUMERAL

## Target
Implement the **Numeral-Bearing Measurement & Replay Calculus** (`REV-SMRM-P2-NUMERAL`, unblocking 3 downstream nodes in `goal_dag.jsonl`). Using `witnessed_difference.measurement` and `witnessed_difference.measurement_replay`, every numerical claim is backed by an explicit finite measurement quotient, calibration table, and replayable composition trace (`replay_composed_measurement`, `verify_measurement_replay`), mapped onto `omega_engine_cognitive_operations` and `omega_engine_pfp`.

## Mathematical Formulation

Let $M = (S, O, Q, c, T)$ be a finite relational model and let $m : S \to \mathcal{Y}$ be a measurement procedure with calibration map $\kappa : \mathcal{Y} \to \mathbb{Z}_{\ge 0}$.
1. **Numeral Provenance (`measure`)**: A numeral $n \in \mathbb{Z}_{\ge 0}$ is admissible only as the calibrated outcome of a witnessed measurement record $R = (s, \text{obs}, \text{class}, \text{numeral}, \text{receipt})$.
2. **Composed Measurement Replay (`replay_composed_measurement`)**: Given a sequence of measurements along a transition trace, the composed numeral and intermediate class transitions are deterministically replayed from the initial state and action sequence.
3. **Replay Verification (`verify_measurement_replay`)**: Any mutation to the claimed numeral, intermediate observation class, or step receipt fails `verify_measurement_replay`.

## Verification Summary
- Valid measurement traces produce deterministic numerals and pass `verify_measurement_replay`.
- Tampered numerals or observation records fail `verify_measurement_replay`.
