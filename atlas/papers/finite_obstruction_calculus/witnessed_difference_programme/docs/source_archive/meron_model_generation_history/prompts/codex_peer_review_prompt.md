# Codex Peer-Review Protocol: Meron Spacetime Field Theorems

**AuthorityEffect:** None.  
**Target Document:** [`meron_spacetime_field_theorems.md`](../meron_spacetime_field_theorems.md)  
**Verifier:** OpenAI Codex / Advanced Reasoning Engine.

---

## Instructions for Codex / OpenAI Reviewer

You are tasked with an adversarial mathematical audit of the treatise on the **Periodic $U=t$ Meron Chain Field Theorems** (covering G3, G4, Theorem A, Theorem B, Gate E refutation, and Gate D polymer closure).

Please review the monograph against the following four rigorous checkpoints:

### Checkpoint 1: Automorphism & Spectral Positivity (G4 & Theorem A)
- Verify Section 1.2: Does the CAR particle-hole automorphism $\mathscr{C}(c_x) = (-1)^x c_x^\dagger$ strictly satisfy $\mathscr{C}(G_L) = G_L$ on the periodic boundary bond $(L-1, 0)$ without missing minus signs?
- Verify Section 2.2: Is the proof of strictly positive Matsubara modes $\hat k_\theta(j) = \frac{\theta^2}{8\pi^2 j^2} + O(\theta^3) > 0$ via the commutator $[G_L, Q_L]$ and fourth spectral moments mathematically solid?

### Checkpoint 2: The Finite-$M$ Indefiniteness & Gate E Counterexample
- Inspect Section 4 and execute `py -3.12 ow/g3_g4_meron_field_theorems/code/gate_e_exact_counterexample.py`.
- Confirm whether the response matrix $G^{(2)}_{4,1}$ on the 16-dimensional CAR Fock space has an exact negative eigenvalue $\lambda_{\min} = -1/706440 < 0$ at $r=1/10$ with eigenvector $v = (-1, -1, -1, -1, +1, +1, +1, +1)^T$.
- Verify that this definitively refutes positive semidefiniteness for finite $M$.

### Checkpoint 3: Emergent Positivity & Mode Decoupling ($O(M^{-6})$)
- Verify Section 6: When tested against a $C^1$ profile $\Psi \in C^1(\mathbb{T}^2)$, does the projection onto the alternating temporal mode $j \mapsto (-1)^j$ scale as $O(M^{-1})$ via summation by parts?
- Confirm that the negative quadratic form contribution is bounded by $-C'\|\partial_\tau \Psi\|_\infty^2 / M^6$, ensuring emergent positivity for all $M \ge M_0(\Psi) = O(1)$.

### Checkpoint 4: 2D Spacetime Polymer Expansion & Lemma A (G3)
- Verify Section 5.2: In the bulk sector $X_{L,M,+}(z)$, does the Kotecký-Preiss criterion $e(d+1)\zeta \le 7e/75 \approx 0.254 < 1$ hold uniformly in $M$ on the polydisk $|z_{j,x}| \le 1/64$?
- Confirm the deduction of MIMO's Lemma A with constant $A \le C_0/1369 < \infty$.

---

## Required Deliverables from Codex

1. **Defects & Counterexamples:** Identify any logical gaps, unstated assumptions, or bounding errors in the monograph.
2. **Acceptance / Certification:** If mathematically sound, issue formal certification of Theorems A and B and G3/G4 closure.
3. **Next Strategic Target:** Propose the next high-impact mathematical target (e.g. Lean 4 Lake formalization, critical coupling boundary $r_c$, or non-Gaussian CFT crossover).
