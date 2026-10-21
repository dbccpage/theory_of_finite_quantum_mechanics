# Does the obstruction a quantum computation generates limit its own ability to finish reliably?

**AuthorityEffect: None.** Branch `comp-qc-viability` (from `lean-v4-35`, PR #137). Source ids `QCV-Q0` to `QCV-Q6`, DAG stage `COMPUTATION`.
This note records a derivation, not a verdict on physical hardware. Nothing here says that a quantum computer is, or is not, physically viable.

## 0. Answer in one paragraph

Inside the finite, exactly declared model of this note the answer is: **it is a threshold condition with four named resource requirements, not a self-referential no-go.** Every step of a noisy computation, repair included, adds residual; repair removes residual and, being a noisy circuit, adds some of its own. The derivation shows (all Lean statements are kernel-checked, axioms limited to `propext`, `Classical.choice`, `Quot.sound`):

1. The repair backlog stays bounded exactly when the *net* repair rate `(1-g)*mu` covers the generation rate `lam` (Q1). If every unit of repair generates at least one unit of new residual (`g >= 1`) no repair rate bounds the backlog: that is the one place where the obstruction does limit its own repair.
2. For the concatenation recurrence `p_{k+1} = c p_k^2` the threshold is exactly `1/c`, with the closed form `c p_k = (c p_0)^(2^k)`, doubly exponential decay below it, a fixed point at it, and divergence above it (Q2).
3. With a level-dependent overhead `c_k` a positive physical error rate below threshold exists **if and only if** the weighted geometric means `amp_k^(1/2^k) = prod_{j<k} c_j^(1/2^(j+1))` stay bounded (Q3). Bounded, geometric (`A B^(k+1)`, any `B >= 1`) and polynomial overhead pass. An overhead exponential in a block size passes exactly when the block size grows by a factor below the squaring ratio 2 per level and fails when the block size at least doubles; an overhead of at least `a b^(2^k)` (`b > 1`) fails for every `p_0 > 0`.
4. Without a supply of fresh (low-entropy) resources a noisy unitary computation forgets its input: the trace distance of two histories is multiplied by exactly `prod (1-p_i)` (Q4). This is a finite exact analogue of the cited 1996 result of Aharonov, Ben-Or, Impagliazzo and Nisan; it is not imported as proof.
5. The conditional theorem (Q5): fresh supply `r >= lam/((1-g) kappa)`, net-efficient repair `g < 1`, level-bounded overhead `c_k <= C`, physical error `p_0 < 1/max(C,1)`, and noise that obeys the recurrence whenever the backlog is bounded, give failure probability at most `L * (D p_0)^(2^k)/D` for a circuit of `L` locations at level `k`, made at most any `epsilon` by an explicit level. The negative half is exact inside the model: viability holds iff the supply reaches `lam/((1-g)kappa)` **and** the overhead means are bounded.

Whether any physical system meets the four requirements (independent or local noise, fresh ancillas, classical control, bounded overhead) is **not** derived and stays OPEN (`QCV-Q5C`). The Majorana record `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` is the same open question seen from locality.

## 1. The question made precise

Let a computation have `L` locations. Each noisy location adds residual; syndrome extraction and repair are circuits of the same kind, so they add residual too. Does the residual the machinery generates exceed what the machinery can remove, for every choice of the machinery's size?

Formally the note asks four sub-questions, one per way the answer could be "yes":

* **A (rate).** Is there a repair rate `mu` with `lam + g mu <= mu` (Q1)?
* **B (threshold).** Is there a physical error rate with `p_k -> 0` for the recurrence with the overhead the repair itself creates (Q2, Q3)?
* **C (memory).** Does a noisy computation with no fresh resources keep any information about its input (Q4)?
* **D (assembly).** Do A to C have a joint solution, and which hypotheses is it conditional on (Q5)?

## 2. DAG material this builds on (read first)

| Item | What it provides | Source (line range) |
| --- | --- | --- |
| `DS-QM061-BUILDABILITY-SET-S` | `UsefulQC` is defined as the conjunction S (race, floor, reachability, H1 advantage); the iff is definitional; S1 is `lambda_gen - mu_rep - eps_mix <= 0` | `dag/derivation_dag.json:4336-4363`, `lean4/BuildabilitySetS.lean:18-24`, `code/rust/src/qm/campaigns/buildability.rs:11-35` |
| `DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE` | threshold theorems as conditional repair certificates; queue `q' = max(0, q + lambda - mu)`; the rate inequality `mu_repair >= lambda_proj` at scale stays open | `dag/derivation_dag.json:5016-5044`, `dag/results/DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE/reviews/20261019_boundaries_audit/README.md:1-8` |
| `DS-QM102-SYNDROME-CAPACITY-BOUND` | syndrome as coboundary defect, `t = floor((d-1)/2)`, lower-bound direction only | `dag/derivation_dag.json:5046-5072`, `code/rust/src/majorana/repair_capacity.rs`, `code/python/src/majorana/repair_capacity.py:1-40` |
| `TFQ-0269`, `TFQ-0270`, `TFQ-0271` | threshold theorems read as repair-capacity certificates; the show-the-packet protocol leaves the device claim open | `dag/derivations/13_finite_qm_information/tfq_0269_threshold_theorems_read_as_repair_capacity_certificates.md:9-16`, `tfq_0270_syndrome_distance_and_repair_capacity.md:9-16`, `tfq_0271_show_the_packet_protocol_for_a_finite_computation.md:9-16` |
| `TFQ-0048`, `TFQ-0152` | toric code, Shor and stabilizer code witnesses | `dag/theory_of_finite_qm.jsonl` rows `TFQ-0048`, `TFQ-0152` |
| `MAJ-SURFACE-SHADOW-FENCE` | surface-code shadows are diagnostic schedules, not threshold proofs | `dag/derivation_dag.json:15534-15561` |
| `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` | OPEN: no Lieb-Robinson bound supports a viability verdict | `dag/derivation_dag.json:15513-15531` |
| `MAJ-PHI1-SYNDROME-DECODING` | `Phi_1` of a residual is a coset-leader weight; exact decoding is NP-hard for general codes (imported) | `dag/derivation_dag.json:15744-15768` |
| `L1-WDP-WINDOW-PHI1-GAMMA2`, `PG-WDP-GROWTH-NO-REPAIR` | `Phi_1([w]) = inf ||w - d0 a||_1` is the repair cost; growing the complex does not repair a residual | `dag/derivation_dag.json:1002-1030`, `dag/derivation_dag.json:918-938` |

## 3. The derivation, step by step

Status labels use the DAG vocabulary. "In the model" means: for the exactly defined objects in the Lean files, for all values of the stated hypotheses.

### Q0 The question node (OPEN)

Is a reliable finite quantum computation, whose repair is itself a noisy computation, possible, or does the residual that repair generates limit the repair's own ability to finish? The note answers it inside a declared finite model as a threshold condition (sections 0 and 4). It leaves the physical question open.

### Q1 Self-obstruction model (DEFINITION, with PROVED_LEAN consequences)

**Declared inputs.** `lam >= 0`, residual generated per round by the computation's own noisy locations, in units of the `Phi_1` repair cost of the packet; `g >= 0`, residual generated per unit of repair performed (the repair circuit's own faults); `kappa > 0`, units repaired per fresh ancilla; `r >= 0`, fresh ancillas per round; `mu = kappa r`; `q0 >= 0`. Backlog: `q_{t+1} = max(0, q_t + lam + g mu - mu)` (`backlog`, `drift` in `QcRepairQueue.lean:27-32`). With `g = 0` this is the DS-QM101 queue; with the substitution `eps_mix := -g mu` the step `lam - mu - eps_mix` of `DS-QM061` S1 is `drift`. That correspondence is algebraic and is not formalized between the two Lean files.

Per-level shape: a distance-three level whose extended gadget has `a` fault locations (the repair circuit's locations among them) fails when two of them fail, so `c = pairCount a = a(a-1)/2` (`QcConcatenation.lean:198`), and the certified threshold `1/c` falls as repair locations are added.

**Kernel-checked in the model** (`QcRepairQueue.lean`, `QcConcatenation.lean`):

| Lean | States |
| --- | --- |
| `backlog_bounded_iff` (68) | for `q0 >= 0`: backlog bounded iff `lam <= (1-g) mu` |
| `backlog_le_initial` (40), `backlog_linear` (51) | drift `<= 0`: never above `q0`; drift `> 0`: exactly `q0 + t*drift` |
| `no_bounded_backlog_if_unit_gain` (87) | `g >= 1`, `lam > 0`: no `mu >= 0` bounds the backlog |
| `capacity_threshold` (93), `fresh_supply_threshold` (100) | `g < 1`: bounded iff `mu >= lam/(1-g)`; with `mu = kappa r`: iff `r >= lam/((1-g) kappa)` |
| `no_supply_linear_growth` (106) | `r = 0`, `lam > 0`: backlog `= q0 + t*lam` |
| `lin_not_goesToZero` (185) | without a squaring repair step (`p_{k+1} = a p_k`, `a >= 1`) the error never tends to zero |
| `threshold_decreases_with_repair` (212) | more fault locations in the gadget, lower certified threshold |

**Status of the record.** The model is DEFINITION; the consequences are PROVED_LEAN inside it. `lam`, `g`, `kappa`, `r` are inputs the note does not measure or derive for any code; deriving `g` for a code is open.

### Q2 Threshold dichotomy (PROVED_LEAN over ℚ)

`conc c p k` is `p_k` of `p_{k+1} = c p_k^2`. In `QcConcatenation.lean`:

* `conc_closed` (39): `c * conc c p k = (c p)^(2^k)` with no hypothesis, hence `p_k = (c p_0)^(2^k)/c` for `c != 0` (`conc_eq_div`, 47).
* `threshold_trichotomy` (143) for `c > 0`, `p >= 0`: (i) `c p < 1`: `p_k -> 0` and the closed form; (ii) `c p = 1`: `p_k = 1/c` for all `k`, not tending to zero; (iii) `c p > 1`: `p_k` diverges (leaves every bound, so also leaves `[0,1]`).
* Explicit bounds: `sub_bound` (65) `c p_k <= (c p)^(k+1)` (doubly exponential in the exact form, at least geometric in this corollary); `sub_half_bound` (71) for `c p <= 1/2`: `p_k <= (1/2)^(2^k)/c`; `sub_strictAnti_step` (92); `super_bound` (119) Bernoulli: `c p_k >= 1 + 2^k (c p - 1)`.
* `goesToZero_iff_below_threshold` (163): `p_k -> 0` iff `c p_0 < 1`. The threshold of the recurrence is exactly `1/c`.

Worked values (checked also by Python and Rust): `c = 4`, `p_0 = 1/10`: `p_k = 1/10, 1/25, 4/625, 64/390625`; `c = 4`, `p_0 = 3/10` exceeds 1 at level 3.

**Not claimed.** That any noise model obeys the recurrence; any value of `c` for any code; the concatenated-code threshold theorem itself (cited, section 5).

### Q3 Self-limitation: the exact condition on the overhead (PROVED_LEAN)

With `p_{k+1} = c_k p_k^2`: `concv_eq_amp` (230) `p_k = p_0^(2^k) * amp c k`, `amp 0 = 1`, `amp (k+1) = c_k amp_k^2`, i.e. `amp k = prod_{j<k} c_j^(2^(k-1-j))`.

**Criterion** (`threshold_region_iff` 320, `region_empty_iff` 332). For `c_k >= 0`: some `p_0 > 0` has `p_k -> 0` iff some `p_0 > 0` has `p_k < 1` eventually iff `AmpBounded c`: `exists M > 0, forall k, amp c k <= M^(2^k)`. In real-number terms `M` bounds the weighted geometric means `exp(sum_{j<k} 2^(-(j+1)) ln c_j)`. The threshold region is empty exactly when this fails. The proof is rootless over ℚ.

**Cases** (all kernel-checked):

| Overhead | Lean | Result |
| --- | --- | --- |
| `c_k <= C` (level-bounded) | `ampBounded_of_bounded` (358), `bounded_overhead_goesToZero` (377) | region nonempty; every `p_0 < 1/max(C,1)` works |
| `c_k <= A B^(k+1)`, `A, B >= 1` | `amp_le_of_geom` (393), `ampBounded_of_geom` (412) | region nonempty, `M = A B^2` |
| `c_k = (k+1)^2` | `ampBounded_poly` (437) | region nonempty |
| `c_k <= a b^(N_k)`, `N_{k+1} <= s N_k`, `s < 2` | `blockExp_le` (515), `ampBounded_of_sizes` (533) | region nonempty |
| `c_k >= a b^(N_k)`, `2^k <= N_k`, `b > 1` | `sizes_not_ampBounded` (586) | region **empty** |
| `c_k >= a b^(2^k)`, `a > 0`, `b > 1` | `dexp_not_ampBounded` (474), `dexp_region_empty` (500) | region **empty**: no positive `p_0` tends to zero |

The sharp feature is the ratio 2. If the overhead is exponential in a block size (a correlated-noise style bound `exp(gamma N)`), the region survives exactly while the block size grows by less than the squaring ratio 2 per level (`s < 2`), and dies when the block size at least doubles, for every `b > 1` however close to one. This is the exact place where an obstruction that the repair machinery creates limits that machinery. For pure geometric or polynomial overhead (for example swap or communication overhead from planar locality growing like a power of `2^k`) it does not.

**Fences.** The families are exact illustrations of the criterion; they are not claims that any physical overhead has such a form. The doubly exponential case is far outside the polynomial block growth of the usual constructions; it is recorded because the criterion is exact.

### Q4 No fresh resources means decay (PROVED_LEAN, general dimension and exact qubit)

**Model.** Global depolarizing channel `Delta_p rho = (1-p) rho + p (tr rho / d) 1` after each unitary `V_i`, `p_i in [0,1]` (`depol`, `noisyStep`, `QcEntropySink.lean:122-126`). **Trace norm.** `tn X = sup_U |tr(U X)|` over unitaries `U` (`tn`, line 44), a variational definition for complex `d x d` matrices of any size `d`; it is bounded (`pairingSet_bddAbove`, 46), homogeneous (`tn_smul`, 78) and unitarily invariant (`tn_conj`, 94). Its equality with the sum of singular values is the standard cited fact (Ky Fan), not re-derived.

| Lean | States |
| --- | --- |
| `depol_dist` (151) | equal-trace inputs: `tn(Delta_p rho - Delta_p sigma) = (1-p) tn(rho - sigma)` |
| `noisyStep_dist` (161) | the same after an arbitrary unitary |
| `run_dist` (193) | along a history: `tn(run L rho - run L sigma) = (prod (1-p_i)) tn(rho - sigma)` |
| `run_dist_le` (209) | every `p_i >= p`: `<= (1-p)^t tn(rho - sigma)` |
| `decay_le_inv` (238), `decay_below` (253) | `(1-p)^t <= 1/(1+p t)`; `t >= (1/delta - 1)/p` gives `<= delta` |

Exact qubit (rational Bloch vectors): `sqDist_runB` (310) `sqDist(run r, run s) = prod (1-p_i)^2 sqDist(r,s)` with unitaries acting as rational rotations `R^T R = 1`; `sqDist_runB_le` (322); `blochMat_sq` (351): `(v . sigma)^2 = |v|^2 * 1` over ℂ, so a difference of two qubit states has both singular values `|r-s|/2` and trace norm `|r-s|` (the last step is the cited eigenvalue fact). Python and Rust check the matrix-level evolution (`rho -> Delta_p(U rho U†)` over Gaussian rationals, `U = c 1 - i s sigma`, `(c,s) = (3/5,4/5)`) against the Bloch-level map exactly.

**Reading.** After `t >= (1/delta - 1)/p` noisy steps the distinguishability of any two input states is at most `delta` of its initial value, whatever unitaries are applied (Helstrom: optimal success probability `1/2 + tn/4`, cited). Reliable computation of depth much beyond `1/p` therefore **requires** an external entropy sink or fresh supply: resets, fresh ancillas, or cold refrigerant (the Landauer cost of the reset is cited, not derived).

**Fences.** The channel is global depolarizing with a per-step rate; independent per-qubit noise on `n` qubits gives the cited `n`-dependent ABIN statement, which is not proved here. The statement is about computation *without* fresh resources; it does not say anything about computations with them.

### Q5 Conditional viability (CONDITIONAL, PROVED_LEAN inside the model for the negative half)

Positive half, `QcSelfObstruction.lean`: `conditional_viability` (78) with hypotheses

* `g < 1`, `kappa > 0`, `r >= lam/((1-g) kappa)` (fresh supply, efficient repair);
* `c_k <= C` (level-bounded overhead), and `max(C,1) p_0 < 1` (below threshold);
* the actual level errors `p_k >= 0` obey `p_{k+1} <= c_k p_k^2` **whenever the backlog is bounded** (the noise-model hypothesis: independent or sufficiently local noise, classical control fast enough for the syndrome, fresh ancillas).

Conclusion: the backlog is bounded and for every `epsilon > 0`, circuit size `L >= 0` there is a level `k` with `L p_k <= epsilon` (union bound over `L` locations). `conditional_viability_explicit` (102): with `max(C,1) p_0 <= 1/2`, any `k` with `L <= epsilon max(C,1) 2^(2^k)` works, so the level grows like `log log (L/epsilon)`. `level_error_le` (31) is the comparison `p_k <= conc (max C 1) p_0 k`. `conditional_viability_instance` (154) shows the hypotheses are jointly satisfiable (`lam=1, g=1/2, kappa=1, r=2, c=4, p_0=1/10`, declared toy numbers).

Negative half (exact inside the model): `model_viable_iff` (114): for `g < 1`, `kappa > 0`, `c_k >= 0`: backlog bounded *and* positive threshold region nonempty iff `r >= lam/((1-g) kappa)` *and* `AmpBounded c`. `not_viable_without_supply` (121), `not_viable_unit_gain` (129), and `not_viable_dexp_profile` (136): a tight lower-bound noise profile `p_{k+1} >= c_k p_k^2` with `c_k >= a b^(2^k)` cannot tend to zero from any `p_0 > 0`; with Q4, a computation with no resets also loses its input.

**What the verdict is.** CONDITIONAL on named assumptions: (a) noise independent or local enough that the recurrence holds when repair keeps up; (b) fresh ancillas at rate `r`; (c) classical control; (d) level-bounded overhead. The note does not decide any of them for any device. The super-threshold and unbounded-overhead cases show that the *certificate* is empty there; in the exact (equality) recurrence the failure bound itself diverges. A tight-model failure is a statement about the model, not about a machine.

### Q5C Physical satisfiability (OPEN)

Whether the hypotheses of Q5 hold for a physical system is not derived, not measured and not claimed either way. It is the same open question as `MAJ-OPEN-LIEB-ROBINSON-LOCALITY` and the unproved rate comparison `mu_repair >= lambda_proj` of `DS-QM101`.

### Q6 Bridge to the Turing-universality branch (DEFINITION)

**Definition (fresh-mark supply).** A *fresh-mark supply* is a stream of distinguished marks, each usable once; a process *needs* `u_t` marks in round `t`. The arithmetic facts are in `QcRepairQueue.lean`: `rounds_le_budget` (116) a total budget `B` with at least `rmin > 0` per round bounds the number of completed rounds by `B/rmin`; `budget_exhausted` (127) a fixed positive consumption exhausts every finite budget.

**Shared structure.** (1) Reliable quantum computation of unbounded length needs an unbounded supply of fresh low-entropy resources: with supply rate `r >= r*` the backlog is bounded, with total supply finite the number of rounds is finite (Q1, Q4, Q6). (2) The parallel branch `comp-utm` derives that Turing universality from `<>` needs an unbounded supply of fresh blank marks, and that bounded regimes are finite automata (that branch is not part of this checkout; no node of it is cited here). Both statements are instances of the same bookkeeping: a bounded supply of fresh marks bounds the length of a process that consumes some of them each round. This note records the shared notion as a **definition**. It proves no common theorem: the two consumption notions (entropy sink, blank tape) are different objects, and no map between them is defined.

## 4. Assembly: the four requirements and what each failure gives

| Requirement | If it fails | Exact statement |
| --- | --- | --- |
| N1 fresh supply `r >= lam/((1-g) kappa)` | backlog grows linearly; with no resets history distance decays as `prod(1-p_i)` | Q1 `fresh_supply_threshold`, `no_supply_linear_growth`; Q4 `run_dist` |
| N2 net-efficient repair `g < 1` | no repair rate bounds the backlog | Q1 `no_bounded_backlog_if_unit_gain` |
| N3 bounded weighted means of `c_k` | no positive `p_0` tends to zero | Q3 `threshold_region_iff`, `dexp_not_ampBounded`, `sizes_not_ampBounded` |
| N4 `max(C,1) p_0 < 1` | the recurrence is at or above its fixed point | Q2 `threshold_trichotomy` |

Together with the noise hypothesis they give the explicit bound of Q5. N1 and N2 are conditions on the *resources*, N3 on the *architecture*, N4 on the *physics*. Only N2 and N3 are conditions that the repair machinery imposes on itself; they are the "obstruction limits its own repair" part of the answer. They are satisfiable in the model.

## 5. Literature context (cited, not proved or imported here)

* Threshold theorems: P. Shor, "Fault-tolerant quantum computation" (FOCS 1996); D. Aharonov and M. Ben-Or, "Fault-tolerant quantum computation with constant error rate" (STOC 1997; SIAM J. Comput. 2008); A. Kitaev, "Quantum computations: algorithms and error correction" (Russian Math. Surveys 1997); E. Knill, R. Laflamme and W. Zurek, "Resilient quantum computation" (Science 1998); J. Preskill, "Reliable quantum computers" (Proc. R. Soc. A 1998); P. Aliferis, D. Gottesman and J. Preskill, "Quantum accuracy threshold for concatenated distance-3 codes" (Quantum Inf. Comput. 2006). The recurrence `p_{k+1} = c p_k^2` and `p_th = 1/c` is the textbook form of the concatenation argument; the constants and noise hypotheses of those theorems are not reproduced.
* Limitations without fresh resources: D. Aharonov, M. Ben-Or, R. Impagliazzo and N. Nisan, "Limitations of noisy reversible computation" (1996, arXiv quant-ph/9611028). The cited result says, in substance, that noisy reversible or quantum computation with no supply of fresh low-entropy bits cannot preserve its input beyond a short depth. Consult the paper for its exact statement; `QcEntropySink.lean` proves a finite exact analogue for the global depolarizing model only.
* Entropy and resets: R. Landauer (1961) on the cost of erasure; D. DiVincenzo (2000) for the fresh-ancilla requirement among the criteria for a quantum computer; D. Gottesman, "Fault-tolerant quantum computation with local gates" (J. Mod. Opt. 2000), on threshold with geometrically local gates.
* Trace distance and contraction: C. Helstrom (1976) on optimal discrimination; M. B. Ruskai (1994) on contractivity of trace-preserving positive maps; the variational form of the trace norm is standard (Ky Fan).
* Skeptical views on correlated noise (G. Kalai and others) motivate the Q3 question of overhead growth; the Q3 families are illustrations, not endorsements.

## 6. Fences

* No claim about physical hardware, no claim that any device beats or fails a threshold, no claim that quantum computation is or is not viable.
* Finite instances (Python, Rust, the worked values) are not general theorems; the general statements are the Lean theorems, each with the hypotheses written in its statement.
* Literature results are cited, not re-proved. The only imported statements are the equality of the variational trace norm with the Schatten-1 norm and the Helstrom formula.
* The decoder is assumed classical and instantaneous in the model. Exact `Phi_1` decoding is NP-hard for general codes (`MAJ-PHI1-SYNDROME-DECODING`, imported); the classical cost of repair is not modelled.
* The global depolarizing model is a coarse stand-in; per-qubit noise, leakage and correlated noise are outside the Lean statements except through the declared `c_k`.
* The `Phi_1` units in Q1 are a unit choice for the backlog; no statement computes `Phi_1` of any residual.

## 7. Native code and reproduction

* Lean (`lean4/lakefile.lean`, library `QcSelfObstruction`, roots `QcConcatenation`, `QcRepairQueue`, `QcEntropySink`, `QcSelfObstruction`): `lake build QcSelfObstruction` in `lean4/`. No `sorry`, `admit`, `native_decide` or new axiom. `#print axioms` for the 62 declarations cited by the DAG records: `dag/research/quantum_computation_self_obstruction_axioms.txt` (every line `[propext, Classical.choice, Quot.sound]`).
* Rust: `code/rust/src/qm/campaigns/qc_self_obstruction.rs` (registered in `code/rust/src/qm/campaigns/mod.rs`); exact `BigRational`; inline tests (23).
* Python: `code/python/src/qm/qc_self_obstruction.py`, tests `code/python/tests/test_qc_self_obstruction.py` (27): `python -I -X utf8 -m pytest code/python/tests/test_qc_self_obstruction.py`.
* Companions: written through `scripts/contract_scores.py`; `python -I -X utf8 scripts/contract_scores.py check` passes.

## 8. Open items

1. Derive `g` and `kappa` for a declared stabilizer packet (exact `Phi_1` on the repair cochain complex of a declared code) and connect `lam` to the cochain residual rate.
2. Replace the global depolarizing model by independent per-qubit noise and prove the `n`-dependent decay (the finite analogue of the full ABIN statement).
3. A Lean statement of the concatenated-code threshold theorem with an explicit `c` for a named code (currently cited).
4. A genuine common theorem for Q6, if a map between fresh-mark supplies of the two branches can be defined.
5. A Lieb-Robinson-type locality bound to discharge hypothesis (a) for a declared local Hamiltonian (`MAJ-OPEN-LIEB-ROBINSON-LOCALITY`).
