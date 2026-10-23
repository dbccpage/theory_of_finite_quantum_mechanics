# PROD-P4-NEXT-2

Goal id: PROD-P4-NEXT-2

Selected scope for PROD-P4-NEXT-2 is recorded in this note.

## Selected scope

Distinct-image target mapper (`map_completion_target_to_distinct_image` and `plan_distinct_image_shelf`) in `omega_engine_applications/wdp_products/p4_observation_budget/adapter.py` and verification in `omega_engine_applications/tests/test_p4_adapter.py`.

## Hypotheses

H1. Under `WDP-DIM-1` (`observer_completion.distinct_image`), given source realizable defect space $R = \operatorname{im} D_s$, algebraic repair space $B = \operatorname{im} D_r$, and existing observer kernel $K = \ker Q$:
- $m_{\mathrm{raw}} = \dim(R \cap K)$,
- $m_{\mathrm{quo}} = \dim(K / (K \cap B))$,
- $m_{\mathrm{both}} = m_{\mathrm{quo}} + \dim(R \cap K \cap B) \le m_{\mathrm{raw}} + m_{\mathrm{quo}}$.

H2. Mapping `CompletionTarget.kind` (`"raw"`, `"quotient"`, `"both"`) onto `produce_completion` and `check_completion` yields a verified completion witness whose row count equals the sharp minimum for each target and satisfies strict subadditivity ($m_{\mathrm{both}} = 2 < 3 = m_{\mathrm{raw}} + m_{\mathrm{quo}}$) when $R \cap K \not\subseteq B$.

## Derivation

1. On the 4D `neither_inclusion` fixture ($R = \operatorname{span}(e_2, e_3)$, $B = \operatorname{span}(e_1, e_2)$, $Q = [0, 0, 0, 1]$), `map_completion_target_to_distinct_image` produces and verifies:
   - `raw`: minimum $2$,
   - `quotient`: minimum $1$,
   - `both`: minimum $2 < 3 = m_{\mathrm{raw}} + m_{\mathrm{quo}}$.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not conflate $R$ and $B$ (`assumes_equal_images = False`).
