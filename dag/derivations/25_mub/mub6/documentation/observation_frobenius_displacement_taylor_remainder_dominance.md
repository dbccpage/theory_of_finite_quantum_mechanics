# Frobenius Displacement Inflation and Taylor Remainder Dominance in Stage B Dual Separation

Type: observation
Confidence: high
Source: Falser reports strategy_L03_N00, strategy_L03_N01, strategy_L03_N02 (Level 3)
Relevant to: Stage B dual hyperplane separation, U(2) cell pruning, and interval-certified complex Hadamard completion enclosures.

## Statement
In Stage B $U(2)$ kernel compression, the Frobenius displacement between a candidate completion $D'$ and the midpoint comparison block $D$ over a $U(2)$ box of half-width $h = \pi / N_u$ is bounded by:
$$z = \sqrt{m_C^{-2} R_s^2 (\sqrt{6} + A_*)^2 + (6h + p)^2}.$$
Across nominal seed parameters ($R_s = 0.201063$, $A_* = 2.0$, $h = \pi/32$, $p \le 0.0926$):
1. On exact Hadamards where $m_C = \sqrt{2}$, $z \approx 0.8992$ to $0.9300$.
2. On accepted seed boundaries where $m_C = 1.0$, $z \approx 1.1247$.
Because the phase ball radius is $r \le 0.016$, the cell displacement $z$ is $56\times$ to $70\times$ larger than the target phase ball radius.
Consequently, the second-order Taylor remainder in the dual separation criterion:
$$\frac{1}{2} z^2 \max\left(0, \max_{i,j}(-y_{D,ij})\right)$$
evaluates to at least $0.4043$ to $0.6325$, which exceeds typical linear separation slacks ($< 0.1$) by a factor of 4 to 6. Under verified outward-rounded interval arithmetic, dual separating hyperplanes fail to refute coarse $U(2)$ cells unless subdivision is refined to astronomical depths.

## Evidence
1. **Analytical Formula Evaluation**:
   Substituting $R_s = 0.201063$, $A_* = 2.0$, $h = \pi/32 \approx 0.09817$, $m_C = \sqrt{2}$, and $p = 0.050022$:
   $$m_C^{-2} R_s^2 (\sqrt{6} + A_*)^2 = \frac{1}{2} (0.040426) (2.44949 + 2.0)^2 = 0.500 \times 0.040426 \times 19.798 = 0.40017.$$
   $$(6h + p)^2 = (6 \times 0.098175 + 0.050022)^2 = (0.58905 + 0.050022)^2 = (0.63907)^2 = 0.40841.$$
   $$z = \sqrt{0.40017 + 0.40841} = \sqrt{0.80858} \approx 0.8992.$$
   The quadratic remainder evaluates to $\frac{1}{2} z^2 \approx 0.4043$.
2. **Boundary Seed Evaluation**:
   At $m_C = 1.0$ and $p = 0.092519$:
   $$z = \sqrt{1.0 \times 0.040426 \times 19.798 + (0.58905 + 0.09252)^2} = \sqrt{0.80034 + 0.46454} = \sqrt{1.26488} \approx 1.1247.$$
   The quadratic remainder evaluates to $\frac{1}{2} z^2 \approx 0.6325$.
3. **Falser Execution Probes**:
   Falser reports across L03_N00, L03_N01, and L03_N02 confirmed that linear dual separation margins in historical runs succeeded only by omitting or under-bounding the quadratic remainder term in floating-point evaluation. Under outward interval rounding, the remainder dominates the linear Taylor expansion.

## Implications
1. Coarse box partitioning of $U(2)$ with $N_u = 32$ (yielding $32^4 = 1,048,576$ boxes per seed) does not achieve certified separation under outward interval arithmetic without further subdivision.
2. Refuting cells to the point where remainder $\frac{1}{2} z^2 < 0.05$ requires $z < 0.316$, demanding $h \ll \pi/32$ and $R_s \ll 0.07$, which increases the required seed count and $U(2)$ subdivision count by orders of magnitude ($\gg 10^{11}$ total evaluations).
3. The claim that dual separating hyperplanes rigorously isolate all completions into 22,379 phase balls remains conditional on outward-rounded re-verification of the remainder terms.

## Caveats
1. This observation applies specifically to the second-order Taylor linearization model used in Theorem 5.1 / Stage B of the polar kernel pipeline.
2. It does not imply that completions exist in infeasible cells; it shows that dual hyperplanes cannot certify their absence without much finer subdivision or higher-order bounds.

## Claim Hygiene Summary
- **What it supports**: Supports that displacement $z \ge 0.899$ is $56\times$ larger than phase ball radius $r = 0.016$, and that the second-order remainder $(1/2)z^2 \ge 0.404$ dominates typical linear separation slacks.
- **What it does not support**: Does not support the existence of complex Hadamard completions in refuted cells.
- **Narrowest defensible claim**: For seed radius $R_s = 0.201063$ and $U(2)$ box half-width $h = \pi/32$, the Frobenius displacement bound satisfies $z \ge 0.8992$, yielding a quadratic remainder bound $(1/2)z^2 \ge 0.4043$.
- **Next test needed**: Evaluate outward-rounded interval enclosures of dual separation slacks on a representative shard of Stage B cells to determine empirical contraction thresholds.
