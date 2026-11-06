# The Symbol Game Architecture Operationalization & Protocol Specification

**AuthorityEffect:** None  
**Firewall Line:** `stated region only; mints no authority`  
**Authors:** Executive Steering Team (Team 0: 5 Experts)  
- Lead Rust Systems & Solvers Architect
- Symbol Game Core Developer & Protocol Master
- Quantum Information & Non-Commutative Operator Theorist
- Simplicial Cohomology & Čech Holonomy Topologist
- Abstract Algebra & Real Algebraic Geometry (Positivstellensatz) Specialist

---

## 1. Executive Summary & Protocol Spine

The Symbol Game represents the finite-packet boundary between continuous, untrusted heuristic proposals (e.g. LLMs, heuristic solvers, random algebraic restart engines) and discrete, trusted verification authority (the Host Governor $\mathcal{P}_S$, exact rational solvers, and the Lean 4 proof assistant).

\[
\boxed{
\mathsf{Finite\ packet\ grammar} + \mathsf{total\ verifier} + \mathsf{packet\ fidelity} + \mathsf{family\ soundness} \implies \mathsf{failure\ is\ mechanically\ enumerable,\ repairable,\ and\ terminalizable.}
}
\]

### 1.1 Dual-Space Sovereignty Model
- **Untrusted Proposer**: Emits candidate structured moves conforming to `$TAU_SG_V1`. It possesses **zero verification authority**. Claims of `"verified": true` in proposal payloads are treated strictly as untrusted testimony.
- **Trusted Host Governor ($\mathcal{P}_S$)**: Owns the carrier $\mathcal{C}$, active relations $\mathcal{R}_{\mathrm{active}}$, defect register $\mathcal{D}_{\mathrm{register}}$ (representing cochain $\Phi_1$), append-only cryptographic trace $\mathcal{H}_{\mathrm{trace}}$, and global invariants $\mathcal{I}_{\mathrm{invariants}}$. The host independently re-derives every admitted step fail-closed with 100% exact rational arithmetic.

### 1.2 The Prevention of Cancellation Laundering
In high-dimensional polynomial and operator spaces, continuous heuristics frequently suffer from *cancellation laundering*: blending opposing vectors or averaging local contradictions into a deceptively low loss. The host enforces:
1. Exact rational representation (`Fraction`, `BigRational`, `Cyc24`) over $\mathbb{Q}$ and $\mathbb{Q}(\zeta_{24})$. Binary floating-point arithmetic is strictly prohibited at AST and runtime levels.
2. Coordinate-wise $L_1$ defect descent where progress on one relation cannot cancel a violation on another:
   $$\|\Phi_1\|_{L_1} = \sum_{e \in E} w_e |r_e|$$

---

## 2. Pinned 5-Tuple Board State & Grammar

A playable state is formally represented as:
$$S = (\mathcal{C},\; \mathcal{R}_{\mathrm{active}},\; \mathcal{D}_{\mathrm{register}},\; \mathcal{H}_{\mathrm{trace}},\; \mathcal{I}_{\mathrm{invariants}})$$

1. **Context $\mathcal{C}$**: Pinned finite carrier. Each symbol is mapped to a unique Unicode codepoint (ASCII 32..126, Greek uppercase 0x0391..0x03A9, Greek lowercase 0x03B1..0x03C9, and relation symbols $\to, \vdash, \bot, \equiv, \delta, \Phi$). Pinned by SHA-256 digest.
2. **Active Relations $\mathcal{R}_{\mathrm{active}}$**: Ground tuples admitted by the host.
3. **Defect Register $\mathcal{D}_{\mathrm{register}}$**: Each declared obligation is evaluated as `Pass`, `Fail(w)`, or `Unknown(r)`. This cochain *is* the obstruction $\Phi_1$.
4. **Cryptographic Trace $\mathcal{H}_{\mathrm{trace}}$**: Append-only chain of verified events linked by SHA-256 parent state digests.
5. **Global Invariants $\mathcal{I}_{\mathrm{invariants}}$**: Invariants (e.g. irreflexivity, unimodularity, positive semidefiniteness, projector completeness) that no legal move may violate.

### 2.1 The 4-Move Grammar ($TAU\_SG\_V1$)

```json
{
  "schema": "TAU_SG_V1",
  "move_type": "ASSERT | CUT | VERIFY | RETRACT",
  "redex_key": {"position": "string", "rule_id": "string"},
  "payload": {},
  "claimed_post_state_digest": "hex64",
  "expected_delta_phi": "exact_rational_string",
  "rationale": "carrier_validated_text"
}
```

| Move | Proposer Request | Host Governor Action & Refusal Condition |
|---|---|---|
| `ASSERT` | Propose candidate ground atom over pinned carrier. | Pinned equations are immutable. Unlicensed claim mutations are refused fail-closed (`FW-MUTATION`). |
| `CUT` | Apply licensed projection / gauge transformation $P_S$ targeting defect $\Phi_1$. | Refused unless $\|\Phi_1\|$ is non-increasing ($\Delta \|\Phi_1\| \le 0$) and all coordinates are exact rationals. |
| `VERIFY` | Recompute target property (`ZERO_OBSTRUCTION` or `DUAL_WITNESS`). | Host recomputes from its internal store. For `DUAL_WITNESS`, host validates: (1) $B^T z = 0$, (2) $\|z_e\| \le w_e$, (3) $\langle z, r \rangle = \|r\|_{1,w}$. |
| `RETRACT` | Roll back to prior snapshot before `step_id`. | Refused unless `step_id` exists in history. The failed branch is logged, incrementing the structural exhaustion counter. |

---

## 3. Network Simplex Duality & Weak Duality Verification

The discrete host solves or verifies $L_1$ projection problems via Network Simplex exact duality.
For a constraint complex $(V, E, w)$ with cochain $c \in \mathbb{Q}^E$:

1. **Primal Problem**:
   $$\min_{s \in \mathbb{Q}^V} D(s) = \sum_{e=(u,v) \in E} w_e |c_e - (s_v - s_u)|$$
2. **Dual Problem**:
   $$\max_{z \in \mathbb{Q}^E} \langle z, c \rangle = \sum_{e \in E} z_e c_e \quad \text{s.t.} \quad B^T z = 0, \quad |z_e| \le w_e \; \forall e \in E$$
3. **Soundness Invariant**:
   For any feasible dual witness $z$ and section $s$:
   $$\langle z, c \rangle = \langle z, r \rangle \le \sum_{e \in E} |z_e| |r_e| \le \sum_{e \in E} w_e |r_e| = D(s)$$
   Equality $\langle z, r \rangle = D(s)$ certifies that $s$ achieves the global minimum defect $\Phi_1$, and $z$ is an optimal dual certificate.

---

## 4. Priority Law (R1 before R2) and Structural Exhaustion

- **R1 (Same-Context Descent)**: Monotonic defect descent must be pursued within the declared carrier and constraint graph.
- **R2 (Context Enlargement / Lift)**: Adding new carrier generators, higher-degree moments, or new variety charts is prohibited until the host certifies **R1 structural exhaustion** (all forward paths in the local state space terminate in strictly positive defect lower bounds).
- **Refutation Semantics**: When a candidate configuration achieves a certified strictly positive dual witness lower bound ($\Phi_1 \ge \varepsilon > 0$), it is permanently culled from the admissible solution space.

---

## 5. Epistemic Firewall Integration

Every proposal, session trace, and certified receipt generated in this campaign MUST embed:
```text
AuthorityEffect: None.
Firewall Line: stated region only; mints no authority
```
Under no circumstances may any agent claim or imply that $\mathrm{MUB}(6) = 3$ or $\mathrm{MUB}(6) \le 3$.
All theorems and certificates apply strictly to declared parameter domains, rational boxes, and verified algebraic variety charts.
