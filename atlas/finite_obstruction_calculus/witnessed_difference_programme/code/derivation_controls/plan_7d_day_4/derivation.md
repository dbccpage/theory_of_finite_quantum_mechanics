# Derivation Control: PLAN-7D-DAY-4

**AuthorityEffect:** None.

## Scope and Claim

This finite control (`PLAN-7D-DAY-4`) verifies the Day 4 native/reference correspondence across Lanes B and C alongside the scoped native reuse records for Lanes A and D:

1. **Lane B (`code/realizable_observation/`)**:
   - Exact rational correspondence between `finite_replay_v3.json` and the 4-state Appendix-S relation arena (`read_branch = 1`, `read_A = 3`, `read_B = 3`, `read_all = 6`, `flip_read = 1/2`, `restore = 1/4`), yielding disturbance+repair optimum $\frac{1}{2} + 3 + \frac{1}{4} = \frac{15}{4}$, adaptive non-disturbing optimum $1 + 3 = 4$, static `read_all` cost $6$, and original-class-only cost $\frac{1}{2} + 3 = \frac{7}{2}$.
   - Changed-input refusal controls: raising `restore` cost to $4$ shifts the disturbance+repair cost to $\frac{15}{2} > 4$ so the overall optimum becomes $4$; collapsing the paired transition relation to final states $(x, y) \mapsto y$ merges distinct original classes after `flip_read`; omitting `restore` leaves perturbed trajectories outside identity fiber restoration.
   - Lean 4 scope parity (`RelationLaws.lean`, `lean_check.txt`): 5 relation-update and decoding laws over `X \to X \to Prop` (`original_coordinate_retained`, `update_twice`, `decoded_original_and_current`, `decoder_unique_on_nonempty_relation`, `same_current_set_need_not_decode_original`) with zero custom axioms.
2. **Lane C (`code/rejection_reuse/`)**:
   - Exact correspondence between `trace_checker.py` and the 15-step compositional trace over the 9-element image carriers $X_0, X_1, X_2$ ($4 + 3 + 1 + \frac{9}{2} + \frac{9}{2} = 17 \le 18$), with scan formulas $T_0(v) = 31 - 3v$ and $T_R(v, s) = 36 - \frac{7}{2}v - 2s$.
   - Changed-input refusal controls: reusing a fixed $d=1$ residual table $R_1$ on changed task $d=2$ fails at least one state in $X_0$; stale parent digest mismatch is refused; repeating the child episode without reuse costs $4 + 3 + 1 + \frac{9}{2} + \frac{9}{2} + \frac{9}{2} = \frac{43}{2} > 18$.
   - Lean 4 scope parity (`rejection_reuse.lean`): standard axioms only (`propext`, `Quot.sound`, `Classical.choice`) and zero `sorry` tokens.
3. **Scoped Native Reuse for Lanes A and D**:
   - Lane A (`GuardedHistoryCoherence.lean`, `guarded_history_coherence_axioms.txt`, `code/causal_certificates/guarded_*`): linear extension counts $(24, 30, 90)$ for `compatible`, `p18`, and `three_pairs`.
   - Lane D (`NativeFutureCompression.lean`, `native_future_compression_axioms.txt`): bounded quotient class count $1 + 15 + 495 + 29260 = 29771$ for $(\text{max\_terms}, \text{max\_count}, \text{horizon}) = (3, 4, 2)$, refusing undeclared bound extensions.

## Non-Claims

- This finite control does not claim empirical LLM behavior or unbounded continuous-time extension beyond the declared finite carriers and certificates.
