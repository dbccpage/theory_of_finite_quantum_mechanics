# TFQ-0123: `GAP-F002-S000-002` Carrier Mismatch and `GAP-F002-S000-001` Supergravity Triangulation Stay Open

- **Node ID**: `TFQ-0123`
- **Stage**: `CONTINUUM_INTERFACE`
- **Status**: `OPEN`
- **Claim Class**: `L4D`
- **Lean 4 Module**: `lean4/CampaignTfq0123ContinuumInterface.lean`
- **Independent Checker**: `checks/independent/tfq-0123.py`
- **AuthorityEffect**: `None`

## 1. Statement & Scope

> `TransportCell.lean` adds loss ledgers valued in the natural numbers and checks associativity of that addition. The atlas Python twin uses floating values and tests one exactly representable triple. `GAP-F002-S000-002` says the two arms are different carriers and that neither witnesses the other. `GAP-F002-S000-001` leaves an 11-dimensional supergravity triangulation unbuilt. What is finite is either the natural-number sum or the float instance, not both as one object. What is not discharged is transport into a smooth frame and the continuum limit. The ledger is not the Einstein equation.

## 2. Formalized Finite Surface & Scope Fences (`lean4/CampaignTfq0123ContinuumInterface.lean`)

1. **Natural-Number Transport Loss Ledger Monoid (`NatTransportCell`, `TransportCell.lean` Replay)**:
   - `nat_transport_cell_assoc`: proves `composeNatCell (composeNatCell c1 c2) c3 = composeNatCell c1 (composeNatCell c2 c3)`.
   - `nat_transport_cell_unit_laws`: proves `composeNatCell (idNatCell c.source) c = c` and `composeNatCell c (idNatCell c.target) = c`.
   - `nat_transport_loss_monotonicity_and_zero_iff`: proves loss monotonicity and `(c1.loss + c2.loss = 0) ↔ (c1.loss = 0 ∧ c2.loss = 0)`.
2. **Carrier Mismatch Between $\mathbb{N}$ Addition and Floating/Dyadic Absorption (`GAP-F002-S000-002`)**:
   - `dyadic_triple_exact_coincidence`: proves that on the representable sub-unit dyadic triple $(1/2, 1/4, 1/8)$ at $\varepsilon = 1/16$, `ulpAbsorbedAdd` associates to $7/8$ in both parenthesizations.
   - `gap_f002_s000_002_float_absorption_breaks_associativity`: proves that at $\varepsilon = 1/8$, the triple $(1, 1/16, 1/16)$ associates to $1$ on the left and $9/8 \ne 1$ on the right under `ulpAbsorbedAdd`, whereas scaled natural numbers associate to $16 + 1 + 1 = 18$.
   - `gap_f002_s000_002_nat_not_divisible_carrier_mismatch`: proves that $1 \in \mathbb{N}$ has no half ($n + n \ne 1$) whereas $1/2 + 1/2 = 1$ in $\mathbb{Q}$, obstructing any unit-preserving additive homomorphism $\mathbb{Q} \to \mathbb{N}$.
3. **11D Supergravity Triangulation & Smooth-Frame Fences (`GAP-F002-S000-001`)**:
   - `simplex_11d_combinatorial_skeleton_counts`: proves the $k$-face counts $\binom{12}{k+1}$ of $\Delta^{11}$ (`12` vertices, `66` edges, `220` 2-faces, `495` 3-faces for $C_3$, `792` 4-faces for $G_4 = dC_3$, `66` 9-faces for codimension-2 Regge hinges, and `4095` total non-empty faces).
   - `simplex_11d_hinge_codimension_and_euler_characteristic`: proves `reggeHingeDim 11 = 9 ≠ 2` and the alternating boundary face sum $\chi(\partial \Delta^{11}) = 2$.
   - `transport_loss_ledger_discards_frame_rotation_fence`: proves that 2D identity and $90^\circ$ rotated $SO(2)$ frames have `det = 1` but distinct traces `2 ≠ 0`.
   - `scalar_loss_ledger_underdetermines_11d_ricci_fence`: proves `symmetricTensorComponents 11 = 66` and exhibits traceless mode pairs $(r, -r)$ with $r + (-r) = 0$ and $r^2 + (-r)^2 = 2r^2 > 0$.

## 3. Independent Verification & Mutation Receipts

- **Independent Checker (`checks/independent/tfq-0123.py`)**: `checks=820 nat_cell=512 carrier_fence=215 sugra_fence=93 failures=0`.
- **Lean Mutation Gate (`dag/research/campaign_tfq-0123_lean_mutation.json`)**: 6/6 semantic mutations killed (`all_killed=true`).

## 4. Claim Hygiene Summary

1. **What it supports**: Supports exact verification of `NatTransportCell` monoid laws and the explicit `GAP-F002-S000-002` and `GAP-F002-S000-001` non-equivalence fences.
2. **What it does not support**: Does not support carrier equivalence between $\mathbb{N}$ and floats, an 11D supergravity triangulation, smooth-frame bundle transport, a continuum limit, or the Einstein field equations.
3. **Narrowest defensible claim**: Natural-number loss addition forms an associative monoid, while floating-point absorption and $\mathbb{N}$ are distinct carriers (`GAP-F002-S000-002`) and a scalar loss ledger does not build an 11D supergravity triangulation or smooth Einstein dynamics (`GAP-F002-S000-001`).
4. **Next test needed**: Return to the highest-ranked unclaimed finite nodes in `dag/pfp/campaign/derivation_queue.json`.
