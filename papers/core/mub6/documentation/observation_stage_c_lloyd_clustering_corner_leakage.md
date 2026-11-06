# Stage C Multi-Bin Lloyd Clustering Corner Leakage

Type: observation
Confidence: high
Source: Falser reports strategy_L02_N00, strategy_L02_N01, strategy_L02_N03, strategy_L02_N07 (Level 2); Candidate strategy_L03_N00 and Falser reports strategy_L03_N00, strategy_L03_N01, strategy_L03_N02, strategy_L03_N03, strategy_L03_N04 (Level 3); Candidate strategy_L04_N00 and Falser report strategy_L04_N00 (Level 4)
Relevant to: Stage C graph clique search, vector discretization, and bin set covering in MUB(6) refutations.

## Statement
In Stage C candidate vector discretization on the 5-torus $\mathbb{T}^5$, Lloyd $k$-means clustering minimizes total variance (sum of squared Euclidean distances) rather than solving a metric set covering problem. While an isolated single bin at fine resolution $M \ge 48$ has center-to-corner distance $d_{\text{corner}} = \frac{\sqrt{5}}{2M} \le \frac{\sqrt{5}}{96} \approx 0.0233 < s = 0.042$, clustering multiple surviving bins into balls of radius $s = 0.042$ causes bin corners to leak outside the cluster balls:
- Diagonal neighbor bins (offset $(1/M, 1/M, 0, 0, 0)$ from the cluster center) have furthest corners at Euclidean distance $\frac{\sqrt{21}}{2M} \approx 0.0477 > s = 0.042$ (ratio $1.137\times$).
- 2-step axis neighbor bins (offset $(2/M, 0, 0, 0, 0)$) have furthest corners at $\frac{\sqrt{29}}{2M} \approx 0.0561 > s = 0.042$ (ratio $1.336\times$).
- Multi-bin clusters spanning $k \ge 4$ bins along an axis have corner distances exceeding $0.0466 > 0.042$.

## Evidence
1. **Analytical Geometry**:
A hypercube bin in $\mathbb{T}^5$ has side length $1/M$. If a cluster centroid coincides with the midpoint of a bin, any adjacent neighbor bin has center offset by $1/M$. The distance to the furthest corner of the neighbor bin is $\sqrt{(3/(2M))^2 + (3/(2M))^2 + 3(1/(2M))^2} = \frac{\sqrt{21}}{2M}$. At $M = 48$, $\frac{\sqrt{21}}{96} \approx 0.047735 > 0.042$.
2. **Numerical Simulation**:
In synthetic 5D $k$-means clustering on 1,000 candidate bins into 50 cluster balls of nominal radius $s = 0.042$ at $M = 48$, 83.1% of assigned bins have corners that leak outside radius $s$ (with worst-case corner distance reaching $0.1253$, nearly triple the cluster radius).
3. **Historical Execution Record Audit**:
The 23,506 historical execution records in Stage C were executed at coarse resolutions $M \in \{12, 24\}$, where single-bin corners alone reached $d_{\text{corner}} \approx 0.0932$ ($M=12$, $2.22\times$ radius) and $0.0466$ ($M=24$, $1.11\times$ radius), strictly leaking even without multi-bin clustering.
4. **Level 3 and Level 4 Falsification of Proposed Repairs**:
   In Level 3 and Level 4 syntheses, candidates proposed replacing Lloyd $k$-means with certified greedy or minimax metric set covering at $M \ge 48$ (with $r_{\text{allow}} = s - d_{\text{corner}} = 0.01871$) or single-bin clustering. Falser audits proved both proposals introduce fatal failure modes:
   - For minimax set covering with $r_{\text{allow}} = 0.01871 < 1/M = 0.02083$, each cluster ball covers at most 1 to 8 grid points (average 1–2 bins). Covering realistic surviving bin counts ($N = 10,000$) requires $> 2,000$ to $5,000$ clusters, instantly exceeding the hardcoded 2048-vertex cap of the C++ graph search pipeline; covering even 1% of $[0, 1]^5$ requires $> 829,000$ cluster balls of radius $0.01871$ ($V_5 = 1.21 \times 10^{-8}$), rendering bipartite clique search computationally intractable.
   - For strict single-bin covers at $M = 48$ ($d_{\text{corner}} = 0.02329 < s = 0.042$), candidate bins number in the thousands ($N_{\text{bin}} \sim 2,000 - 10,000$), instantly exceeding the 2048-vertex limit.
   - For $M \ge 96$, a cluster ball of diameter $2s = 0.084$ spans up to 8 bins along an axis; any bin with center distance $d > s - d_{\text{corner}} = 0.042 - 0.01165 = 0.03035$ has corners exceeding radius $s = 0.042$ (for center distance 0.035, corner distance is $0.0466 > 0.042$).
   - Crucially, neither greedy nor minimax nor single-bin covering has ever been executed across the 23,506 historical records; asserting that historical branch-and-bound runs refuted cliques under certified clustering is a false attribution to buggy runs with >83% corner leakage.

## Implications
Candidate vector phases residing in the leaked bin corners are omitted from the vertex sets of the orthogonality graph $\mathcal{O}$ and unbiasedness graph $\mathcal{U}$. Omitting candidate basis vectors can falsely destroy valid 6-cliques, creating false-negative clique search outputs (erroneously declaring nonexistence of MUB quartets).
Efforts to force 100% vertex containment by shrinking cluster containment radii trigger severe cluster fragmentation and combinatorial explosion, exceeding graph search vertex limits.

## Claim Hygiene Summary
- **What it supports**: Supports that multi-bin Lloyd clustering at $M = 48$ leaks bin corners outside radius $s = 0.042$, and supports that minimax metric set covering with $r_{\text{allow}} = 0.01871$ restricts clusters to 1–8 bins, causing cluster counts to exceed graph search vertex caps.
- **What it does not support**: Does not support the existence of an MUB quartet in $\mathbb{C}^6$.
- **Narrowest defensible claim**: Lloyd $k$-means clustering at $M=48$ allows multi-bin corners to exceed radius $s=0.042$, while enforcing vertex enclosure via $r_{\text{allow}} = s - d_{\text{corner}}$ restricts clusters to at most 8 bins at $M=48$.
- **Next test needed**: Replay Stage C on benchmark phase balls using adaptive variable-radius covers or test graph searches with higher vertex caps.
