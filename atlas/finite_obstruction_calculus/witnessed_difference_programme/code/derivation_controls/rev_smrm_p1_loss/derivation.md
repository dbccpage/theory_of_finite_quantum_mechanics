# REV-SMRM-P1-LOSS

Goal id: REV-SMRM-P1-LOSS

Selected scope for REV-SMRM-P1-LOSS is recorded in this note.

## Selected scope

Verification (`REV-SMRM-P1-LOSS`) for P1 `WdpAbstentionGovernor` (`omega_engine_applications/wdp_products/p1_abstention_governor/adapter.py` and `omega_engine_applications/tests/test_p1_p2_adapters.py`):
1. The governor refuses `LOSS` certificates whose trap set $T$ omits the initial belief $b_0$ (`b_0 in T` check fails in `verify_certificate`, returning `AbstentionLabel.REFUSED_CERTIFICATE`).
2. `Stalled`, `Exhausted`, and `Impossible` are distinct, non-interchangeable labels (`WDP-CHS-N07`).

## Hypotheses

H1. A valid `LOSS` certificate in Appendix G.4 requires a trap set $T \subseteq B$ such that (i) $b_0 \in T$, (ii) $T \cap B_{\mathrm{goal}} = \emptyset$, and (iii) $T$ is closed under every admissible action from every $b \in T$.

H2. If $b_0 \notin T$, the certificate does not trap the initial state of the arena and must be refused (`RefusedCertificate`).

H3. Operational stagnation (`Stalled`), budget exhaustion (`Exhausted`), and certified arena impossibility (`Impossible` under a task policy) are mutually distinct states (`WDP-CHS-N07`).

## Derivation

1. **Refusal of `LOSS` certificate lacking $b_0$**:
   - Starting from a verified `LOSS` certificate on `example_arenas()["loss"]`, removing `loss_arena["initial"]` ($b_0$) from `cert["trap_set"]` causes `verify_certificate(loss_arena, bad_cert)` to fail the `"b_0 in T"` check.
   - `WdpAbstentionGovernor.verify(loss_arena, bad_cert)` emits `GovernorReport` with `label == AbstentionLabel.REFUSED_CERTIFICATE` and `verified is False`.

2. **Distinctness of `Stalled`, `Exhausted`, and `Impossible`**:
   - On `example_arenas()["stagnation"]`, `evaluate` emits `AbstentionLabel.STALLED`.
   - On `example_arenas()["exhausted"]`, `evaluate` emits `AbstentionLabel.EXHAUSTED`.
   - On `example_arenas()["loss"]` with `task_admits_impossibility=True`, `evaluate` emits `AbstentionLabel.IMPOSSIBLE`.
   - All three labels are pairwise distinct in `AbstentionLabel`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not treat `Stalled` or `Exhausted` as evidence of `Impossible`.
