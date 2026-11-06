# Candidate Basis Dimension Scaling and Coordinate Misidentification

Type: observation
Confidence: high
Source: Aggregator Nodes strategy_L02_N00, strategy_L02_N02, strategy_L02_N05 (Level 2 Falser Reports)
Relevant to: Algebraic geometry, polynomial optimization, semidefinite programming (SDP/SOS), and Gröbner basis formulations for MUB extensions in dimension 6

## Statement
In dimension $d=6$, dephasing a single unitary candidate basis against the standard basis leaves $6 \times 5 = 30$ complex variables, corresponding to $n = 60$ real variables. A search for a 4-MUB system requires finding two mutually unbiased candidate bases $B_1, B_2$ simultaneously unbiased to $\{I, F_6\}$, which requires $2 \times 30 = 60$ complex variables ($n = 120$ real variables). Formulations that analyze a 60-real-variable polynomial system parameterize only a single candidate basis (a 3-MUB system), which is already known to exist across the entire Szöllősi family $B_6(\theta)$. At $n=120$, degree-4 sum-of-squares (SOS) relaxations scale to a Gram matrix size of $\binom{122}{2} = 7381$ (over $5.45 \times 10^7$ matrix entries) and $\binom{124}{4} = 9,379,505$ affine constraints, exceeding standard SDP solver capabilities.

## Evidence
1. **Coordinate Counting**:
   Each candidate basis $B = [v_1, \dots, v_6] \in U(6)$ has 36 complex entries. Dephasing the first row and column leaves 25 entries; column normalization and global phases fix 6 real phases, leaving 30 complex parameters = 60 real parameters for one basis. For two bases $(B_1, B_2)$, mutual unbiasedness requires parameterizing both simultaneously, yielding $60$ complex = $120$ real variables.
2. **Triplets vs. Quadruplets**:
   A single candidate basis $B_1$ mutually unbiased to $I$ and $F_6$ forms a 3-MUB system $\{I, F_6, B_1\}$. Szöllősi (2010) explicitly proved that MUB triplets exist on the entire two-circulant family $B_6(\theta)$ for all $\theta \in [0, \pi/2]$. Thus, checking or certifying feasibility for a 60-variable system merely tests known triplets and does not probe $N(6) \ge 4$.
3. **SOS Dimension Scaling**:
   For degree-4 pseudo-moments with $n$ variables, the positive semidefinite block size is $\binom{n+2}{2}$. For $n=60$, $\binom{62}{2} = 1891$ ($1891 \times 1891 \approx 3.58 \times 10^6$ entries). For $n=120$, $\binom{122}{2} = 7381$ ($7381 \times 7381 = 54,479,161$ entries), and the dual constraint count is $\binom{124}{4} = 9,379,505$, rendering dense SDP interior-point algorithms intractable without symmetry reductions.

## Implications
- Any polynomial optimization or SOS certification targeting $N(6) \ge 4$ must explicitly account for the full $120$-variable system (or provide a decoupling reduction).
- Claims of certifying infeasibility or feasibility on a 60-variable system must be audited for whether they only test 3-MUB existence.
- Reformulations using symmetry reductions (such as commutant or group-theoretic block diagonalization) are necessary before SDP hierarchies can be made tractable for 4-MUB searches.

## Caveats
- If one basis $B_1$ can be fixed without loss of generality (up to equivalence), the variable count might be reduced, but in dimension 6 the stabilizer group of $\{I, F_6\}$ is discrete (order 216), leaving no continuous gauge freedom to fix $B_1$ continuously.
- Exploiting polynomial symmetries (such as $S_6$ permutations and circulant automorphisms) can block-diagonalize the SDP, but the block sizes must still be shown tractable.
