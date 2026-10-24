# Independent Derivation Note: `PGW-SN-PROTECTED-ANSWER-TRANSPORT` (`TFQ-0519`)

- **AuthorityEffect**: `None`
- **Target**: `PGW-SN-PROTECTED-ANSWER-TRANSPORT` (`TFQ-0519`, stage `MSSN_SN`, group `S(n)`)
- **Outcome**: `Narrowed` (`record_status: "OPEN_OBLIGATION"`, `dag.status: "OPEN"` retained for the external `S6Descent` Python code in `002_oesn/code/sn_core.py`, case-by-case user-supplied target transitions, and the exercise obligation $s_6 = 1$)
- **Lean 4 Module**: `lean4/CampaignSnProtectedAnswerTransport.lean`
- **Independent Check**: `checks/independent/pgw-sn-protected-answer-transport.py`

## 1. Mathematical Summary

Given a lift $u : A \to B$ and a typed recovery map $r : B \to A \oplus E$ satisfying `OldImageLaw u r` ($\forall a \in A,\; r(u(a)) = \mathrm{inl}(a)$):

1. **Retraction-induced answer transport and image uniqueness**:
   - Every protected answer $F : A \to Q$ and off-image fallback $d : E \to Q$ define a canonical target counterpart `retractionTransport r F d` $= \mathrm{Sum.elim}\;F\;d \circ r : B \to Q$ satisfying `AnswerTransport u F (retractionTransport r F d)`, i.e., $\forall a \in A,\; F'(u(a)) = F(a)$ (`retraction_transport_law`).
   - Without choosing an off-image fallback $d$, `typedRetractionTransport r F` $= \mathrm{Sum.map}\;F\;\mathrm{id} \circ r : B \to Q \oplus E$ sends $u(a) \mapsto \mathrm{inl}(F(a))$ and preserves the refusal tag $\mathrm{inr}(e)$ on off-image points (`typed_retraction_transport_law`, `typed_retraction_transport_refuses`).
   - Any two target counterparts $F'_1, F'_2 : B \to Q$ satisfying `AnswerTransport u F` agree at every point of $\mathrm{im}(u)$ (`transport_unique_on_image`).
2. **Off-image freedom and exact counterpart cardinality**:
   - Whenever $u$ is injective and $b_0 \notin \mathrm{im}(u)$, any protected answer $F : A \to Q$ and any two distinct values $q_0 \neq q_1 \in Q$ yield two distinct target counterparts $F'_0 \neq F'_1 : B \to Q$ that both satisfy $F'_i \circ u = F$ while $F'_0(b_0) = q_0$ and $F'_1(b_0) = q_1$ (`transport_off_image_underdetermined`).
   - For finite types $A, B, Q$ and injective $u : A \to B$, the number of target counterparts $F' : B \to Q$ satisfying `AnswerTransport u F F'` is $|Q|^{|B| - |A|}$ (`transport_counterpart_card`).
3. **Commuting transition squares and multi-step preservation**:
   - If $(T : A \to A, T' : B \to B)$ satisfies `TransitionSquare u T T'` ($\forall a \in A,\; T'(u(a)) = u(T(a))$), then by induction on $k \in \mathbb{N}$ the $k$-fold iterates $(T^{[k]}, (T')^{[k]})$ satisfy `TransitionSquare u (T^[k]) (T'^[k])` (`commuting_square_iterated`), and every transported answer $F'$ satisfying $F' \circ u = F$ satisfies $F'((T')^{[k]}(u(a))) = F(T^{[k]}(a))$ (`commuting_square_preserves_transported_answer`).
   - Under `OldImageLaw u r`, any source transition $T : A \to A$ and fallback state $b_{\mathrm{ref}} \in B$ induce a canonical target transition `canonicalTransitionLift u r T b_ref` satisfying `TransitionSquare u T` (`canonical_transition_lift_commutes`).
   - Pointwise on $\mathrm{im}(u)$, when $T'(u(a)) \in \mathrm{im}(u)$ and `OldImageLaw u r` holds, $T'(u(a)) = u(T(a))$ holds if and only if every Boolean protected answer $F : A \to \mathrm{Bool}$ is preserved after one step via `retractionTransport r F d` (`commuting_square_iff_boolean_answers_preserved_on_image`).
   - `OldImageLaw u r` and `AnswerTransport u F F'` alone do not imply `TransitionSquare u T T'` or one-step preservation $F'(T'(u(a_0))) = F(T(a_0))$ (`transition_square_not_implied_general`).
4. **Concrete `SnCarrier` and `S6Descent` instantiations**:
   - For `SnCarrier` (`BasePresentation`, `sectionLift`, `retractionDownMap` in `lean4/Imported/OeSn/SnOffImage.lean`), `snRetract n : SnPresentation → BasePresentation ⊕ Unit` satisfies `OldImageLaw (sectionLift n) (snRetract n)` (`snRetract_old_image_law`) and refuses exactly when `retractionDownMap n p = .nonDescent` (`snRetract_nonDescent_iff`), yielding canonical answer transport (`snCarrier_answer_transport`) and canonical transition squares (`snCarrier_canonical_transition_square`), while `.lift ⟨6, .glyphs [.latin 0, .latin 1, .latin 2]⟩` witnesses stage-6 off-image non-uniqueness (`snCarrier_off_image_underdetermined`) and one-step transition failure without a commuting square (`snCarrier_transition_counterexample`).
   - For the integer slice model `s6Lift x = (x, 0)` and `s6Retract (x, y)`, `OldImageLaw s6Lift s6Retract` holds (`s6Descent_old_image_law`), yielding canonical answer transport (`s6Descent_answer_transport`) and canonical transition squares (`s6Descent_canonical_transition_square`), while the off-slice shift $T'(x, y) = (x + 1, 1)$ violates the commuting square and corrupts transported answers (`s6Descent_transition_counterexample`).
5. **Non-implication fences**:
   - Universal validity on $\mathrm{im}(u)$ does not conservatively extend to all of $B$ when off-image points exist (`not_conservative_extension_off_image`).
   - `OldImageLaw` does not make $u$ and a collapsed retraction a two-sided inverse off $\mathrm{im}(u)$ (`old_image_not_right_inverse`), nor does it induce a Galois adjunction $u(a) \le b \leftrightarrow a \le p(b)$ on the monotone lift `gapLift : Fin 2 → Fin 3` (`old_image_not_left_galois_adjunction`).
   - Transporting an active demand predicate $D : A \to \mathrm{Prop}$ across $u$ preserves the active demand at $u(a_0)$ (`unrelated_demand_not_resolved_by_lift`), and `activeObstructions 6 = 1` in `SnCarrier` records the stage-6 obligation table value alongside exact old-image recovery (`snCarrier_s6_demand_active`).

## 2. Claim Hygiene Summary

1. **What it supports**: Retraction-induced answer transport, off-image counterpart cardinality $|Q|^{|B|-|A|}$, $k$-step commuting transition square transport, canonical transition lifts, concrete `SnCarrier` and integer `S6Descent` transport and counterexamples, and the three non-implication fences (no conservative extension off-image, no two-sided inverse or Galois adjunction on `gapLift`, no resolution of an active demand) in Lean 4 and independent Python.
2. **What it does not support**: Automatic generation of commuting squares for arbitrary user-supplied target operations without checking `TransitionSquare`, cross-repository refinement of `omega_engine_education/documentation/002_oesn/code/sn_core.py::S6Descent`, or treating the table entry $s_6 = 1$ as a forced survivor count.
3. **Narrowest defensible claim**: Under `OldImageLaw u r`, canonical retraction transport `retractionTransport r F d` and `canonicalTransitionLift u r T b_ref` satisfy `AnswerTransport` and `TransitionSquare` (including for `SnCarrier` and the integer `S6Descent` model), whereas off-image values and unconstrained target transitions remain underdetermined ($|Q|^{|B|-|A|}$ counterparts) and can violate answer preservation unless a commuting square is supplied.
4. **Next test needed**: Proceed to the next available derivation in `dag/pfp/campaign/derivation_queue.json`.
