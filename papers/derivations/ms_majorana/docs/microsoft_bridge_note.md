# Majorana Parity Obstruction Calculus: Exact Algebraic Classification
## Technical Bridge Note for Microsoft Azure Quantum & Topological Computing Group

This technical note documents the exact polynomial-time classification algorithm for finite boundary complex readout schedules over $\mathbb{G}\mathbb{F}(2)$, and outlines the formal verification of Ising braid and fusion algebraic identities using exact cyclotomic field arithmetic.

---

### 1. Theorem (Topological Parity Obstruction under Bounded GF(2) Assumptions)

Let $(C_*, D_*)$ be a finite chain complex of vector spaces over the field $\mathbb{G}\mathbb{F}(2)$:

$$C_0 \dots \xrightarrow{D_0} C_1 \xrightarrow{D_1} C_2$$

where $C_0$ represents the vertex (0-cell) space, $C_1$ represents the edge (1-cell) space, and $C_2$ represents the face (2-cycle) space. The boundary operators satisfy the standard algebraic chain condition:

$$D_1 \cdot D_0 = 0 \dots \pmod 2$$

For a given readout mismatch vector $r \in C_1$, the system is classified into three mutually exclusive algebraic categories:

1. **Exact (Locally Generated):**
   The mismatch $r$ lies in the image of $D_0$. There exists a vertex carrier state $\alpha \in C_0$ such that:
   $$D_0 \cdot \alpha = r \pmod 2$$
   This state suggests that the mismatch is locally resolvable.

2. **Closed Residual (Coherent Obstruction):**
   The mismatch $r$ is closed ($D_1 \cdot r = 0 \pmod 2$) but does not lie in the image of $D_0$. The quotient state $[r]$ represents a non-trivial class in the first homology group:
   $$[r] \in H_1(C_*) = \ker(D_1) / \text{im}(D_0)$$
   Its non-zero normal form under row-reduction represents the topological obstruction.

3. **Open Obstruction (Higher Coherence Contradiction):**
   The mismatch $r$ is not closed:
   $$D_1 \cdot r \neq 0 \pmod 2$$
   The non-zero boundary $w = D_1 \cdot r$ acts as a coherence witness demonstrating contradiction at the face level.

---

### 2. Corrected Finite GF(2) Parity Complex Example

To illustrate the mechanics in a concrete setting, consider a triangular cell complex with:
* $C_0$ (vertices): $\{v_0\}$ (dimension 1)
* $C_1$ (edges): $\{e_0, e_1, e_2\}$ (dimension 3)
* $C_2$ (faces): $\{f_0\}$ (dimension 1)

The boundary operators are configured as:

$$D_0 = \begin{pmatrix} 1 \\ 1 \\ 0 \end{pmatrix}, \quad D_1 = \begin{pmatrix} 1 & 1 & 0 \end{pmatrix}$$

#### Chain Condition Validation
$$D_1 \cdot D_0 = \begin{pmatrix} 1 & 1 & 0 \end{pmatrix} \cdot \begin{pmatrix} 1 \\ 1 \\ 0 \end{pmatrix} = 1 + 1 + 0 = 0 \pmod 2$$
This supports the algebraic consistency of the chain complex.

#### Mismatch Scenarios and Classification
* **Exact Scenario ($r = [1, 1, 0]^T$):**
  Solving $D_0 \cdot \alpha = r$ yields the unique solution $\alpha = [1]$, classifying it as **Exact**.
* **Closed Residual Scenario ($r = [0, 0, 1]^T$):**
  Here, $D_1 \cdot r = [0] \pmod 2$ (closed), but $D_0 \cdot \alpha = r$ has no solution over $\mathbb{G}\mathbb{F}(2)$. The quotient normal form is $[0, 0, 1]^T$ with obstruction norm $1$, classifying it as **ClosedResidual**.
* **Open Obstruction Scenario ($r = [1, 0, 0]^T$):**
  Computing $D_1 \cdot r$ yields the non-zero witness $w = [1] \pmod 2$, classifying it as **OpenObstruction**.

---

### 3. Exact Polynomial-Time Algorithm

The classification of any readout schedule $r$ is executed using exact Gaussian elimination (Reduced Row Echelon Form) over $\mathbb{G}\mathbb{F}(2)$ without floating-point arithmetic.

```
Algorithm: Parity Obstruction Terminalizer
Input: Boundary matrices D0, D1, Readout mismatch r
Output: Terminal status, Certificate, Class ID

1. Validate complex structure:
   Confirm D1 * D0 == 0 mod 2.
   If invalid, return Status: RepresentationInvalid.

2. Attempt to solve D0 * alpha = r mod 2:
   Construct augmented matrix [D0 | r].
   Reduce to RREF using bitwise XOR row operations.
   If consistent:
       Extract solution alpha.
       Return Status: Exact, Certificate: alpha, Class ID: "exact".

3. Compute face-level coherence:
   w = D1 * r mod 2.
   If w != 0:
       Compute normal form n = r mod im(D0) via RREF on D0^T.
       Return Status: OpenObstruction, Witness: w, Class ID: "open-obstruction:" + string(w).

4. Mismatch is closed but not exact:
   Compute normal form n = r mod im(D0) via RREF on D0^T.
   Return Status: ClosedResidual, NormalForm: n, Class ID: "closed-residual:" + string(n).
```

---

### 4. Sample Replayable Certificate Ledger Entry

Every terminalization outcome is logged in a standardized JSON schema designed for replayability. Below is an example of a recorded **ClosedResidual** certificate:

```json
{
  "certificate_id": "cert_a94f89c0f938c222a7f5a04f2105151e33d4e68e4a8f9c1b72e5c8e9d0a1b2c3",
  "carrier_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "terminal_status": "ClosedResidual",
  "q1_norm": "1",
  "certificate_alpha": null,
  "normal_form": [0, 0, 1],
  "coherence_witness": null,
  "replay_hash": "8f3c1a9d0e2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d"
}
```

---

### 5. Strict Non-Claims and Bounded Interpretation

Consistent with scientific discipline and rigorous engineering practice, we declare the following narrow claims:

* **Scope of Validation:** The exact algorithms and algebraic classifications described herein have been tested and verified in finite, simulated, discrete chain complex models (such as Triangle, Plaquette, and Prism complexes).
* **Physical Hardware Interpretation:** These results do not guarantee performance, error rates, or noise resilience on physical topological quantum processors or noisy intermediate-scale quantum (NISQ) hardware.
* **Algebraic Representation:** The verifications of the Yang-Baxter relation, fusion rules, and Hexagon equations are conducted within the formal algebraic field $\mathbb{Q}(\zeta_{16})$ and represent algebraic consistency of these structures. They do not constitute empirical evidence of anyon dynamics in real physical substrates.
* **Next Tests Needed:** The next step of research requires integrating these exact parity check matrices with realistic topological noise models to evaluate decoding thresholds under simulated phenomenological noise.
