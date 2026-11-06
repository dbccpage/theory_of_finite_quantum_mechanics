# Practical Evidence Checklist for Scalable Quantum Computation

**Document ID:** `QM_103_CHECKLIST`  
**Status:** Implementation Documentation (Operational Review Checklist)  
**AuthorityEffect:** None

---

## 1. Practical Review Checklist

Before treating any physical quantum scalability or fault-tolerance claim as settled, the claim must publish an explicit, replayable evidence packet covering the following six dimensions:

| Dimension | Declared Items | Required Specification |
|---|---|---|
| **1. Architecture** | Hardware platform, physical carrier | Physical qubit technology, device topology, coupling geometry, and duration of the active syndrome extraction / correction window. |
| **2. Workload** | Logical distinction, computational task | Target logical observable, preserved code-space sector, or logical circuit workload executed. |
| **3. Noise Assumptions** | Defect mechanisms, error model | Physical noise channels, measurement leakage, crosstalk, and defect-history space $C^1$. |
| **4. Logical Error Target** | Desired suppression, target metric | Target logical error probability per cycle or per gate, with explicit error-detection criteria. |
| **5. Resources & Overhead** | Physical overhead budget | Total physical qubits, time latency, control bandwidth, decoder compute capacity, and cryostat/control hardware requirements. |
| **6. Evidence Pipeline** | Hash-verified machine receipt | Replayable software test suite or machine-generated execution receipt verifying the data end-to-end. |

---

## 2. Mathematical Corrections to Repair Quotient Formulations

### 2.1 Feasible Repair Sets versus Algebraic Quotients
Budget-constrained repairs do not generally form an algebraic vector space or submodule.
If a repair action is constrained by locality, weight, latency, or energy, the set of admissible repairs $B \subset C^1$ is typically not closed under addition.

**Counterexample to Transitivity:**  
Suppose bit-flip repairs on two bits are limited to weight $\le 1$:
$$B = \{00, 10, 01\} \subset \mathbb{F}_2^2.$$
If one defines a relation $x \sim y \iff x - y \in B$, then:
- $00 \sim 10$ (since $00 - 10 = 10 \in B$),
- $10 \sim 11$ (since $10 - 11 = 01 \in B$),
- but $00 \not\sim 11$ (since $00 - 11 = 11 \notin B$).

Because transitivity fails, the relation does not define an equivalence relation, and no algebraic quotient space $C^1/B$ exists. Taking the linear span $\operatorname{span}(B)$ generates all of $\mathbb{F}_2^2$, which improperly admits the unbudgeted repair $11$.

**Resolution:**  
The framework distinguishes two mathematically distinct objects:
1. **Stabilizer / Gauge Subgroup (Algebraic Quotient):** A linear subspace or subgroup defining true quotient equivalence classes $[x] \in C^1/B^1$.
2. **Resource-Constrained Feasible Set (Optimization / Reachability):** A bounded subset of executable operations defining a constrained reachability or minimum-weight decoding problem.

### 2.2 Minimum Residual Weight versus Logical Error Probability
Identifying the minimum residual weight of a homology class directly with logical error probability is mathematically invalid:
1. A metric weight $\min_{\alpha} \operatorname{wt}(\omega - d_0 \alpha)$ computes a discrete combinatorial distance on a cell complex.
2. Logical error probability is a measure-theoretic quantity that requires an explicit noise probability distribution, an explicit decoder algorithm, and a specified failure event.
3. The empirical Fowler formula $P_L \approx C (p / p_{\text{th}})^{(d+1)/2}$ is an asymptotic numerical approximation under independent phenomenological noise models; it is not a quotient-norm identity.
4. Universal positive repair margin conditions (such as $\mu_{\text{repair}} - \lambda_{\text{proj}} - \epsilon_{\text{mix}} \ge \delta > 0$) lack general necessity proofs and must be treated as architecture-specific throughput bounds.
