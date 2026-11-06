# Draft v1 — from difference to Hamilton and Noether

Purpose: two printable sheets. Sheet 1 contains only straight line segments, triangular arrowheads, moves and short captions. No axes, grids, ambient boxes, circles or formula labels. Sheet 2 supplies all mathematical meanings, assumptions and limits. This is a construction of a small mathematical mechanics, not a derivation of physical laws from arbitrary marks. No claims about Born probabilities, Everett, Bell, or quantum mechanics are made in this installment.

## Sheet 1: eight horizontal strips, three panels each

Horizontal grey arrows between panels indicate reading/operation order, not an extra physical vector. Ghosted lines indicate a previous configuration. Black and green distinguish the two marks; orange is a constructed result or an incremental change. Text outside the captions is confined to unobtrusive strip numbers.

1. Compare: (a) two identical arrows placed apart, caption “Bring them together.” (b) the matching arrows overlaid, caption “They match.” (c) common tail, different tips, caption “Now there is a difference.” Congruence under translation is the chosen comparison, not a universal criterion of physical identity.

2. Compose: (a) one black arrow, “Take this step.” (b) green arrow placed head-to-tail after black, “Then take this step.” (c) both steps plus orange start-to-end arrow, “One step reaches the same end.” This is vector composition in a supplied affine plane.

3. Refine: (a) a two-segment path between fixed endpoints, “A few steps.” (b) a four-segment approximation to the same prescribed curved path, “More, smaller steps.” (c) a twelve-segment approximation, “Follow the change more closely.” The path is drawn only with line segments; no smooth curve. This suggests refinement; it does not prove a limit, differentiability or identity of approximate trajectories.

4. Cycle: (a) two matching directions at a common tail, “Start together.” (b) green makes a quarter-turn while black stays fixed, “Turn just one.” (c) green again matches black, with four ghosted intermediate directions, “A full turn brings it back.” This introduces cyclic relative position, not a quantum amplitude. Rotation is a supplied operation.

5. Preserve: (a) a rectangular cell divided into two triangles, “Two pieces make this patch.” (b) its top edge shifted sideways with base fixed, “Slide the top sideways.” (c) a more strongly sheared cell with same base and height, “Same area. Different shape.” The outline is the changing object, not an ambient container. Shearing preserves oriented area; ordinary area equality alone would also admit orientation reversal.

6. Couple: draw paired changes in a dimensionless state plane, black horizontal coordinate segment and green vertical momentum segment. (a) show a green segment and an orange horizontal increment in its corresponding direction, “Green sets black’s next change.” (b) show a black segment and an orange vertical increment in its opposite direction, “Black sets green’s opposite change.” (c) show three successive exact rotations of the endpoint of the paired segments, “Together, the pair turns.” Panels a/b describe instantaneous rates, not a finite Euler update; c uses the exact flow. This distinction is stated on the math sheet.

7. Symmetry: NEW rule, explicitly indicated by caption. (a) two stacked paired states with different black extents and equal green extents, “New rule: slide at green’s pace.” (b) shift both black extents equally, “Start farther along.” (c) advance the shifted and unshifted pairs through the same time interval, “The same shift survives the move.” Precise claim: translation of q commutes with the free-particle flow. This is not the previous oscillator rule.

8. Conservation: under the sliding rule of strip 7, (a) a paired state, “Black advances.” (b) later paired state with same green extent, “Green stays the same.” (c) another later state with same green extent, “Every step keeps that amount.” This visibly illustrates momentum conservation. The reason it follows from a symmetry is supplied on sheet 2, not inferred merely from repeated equal marks.

## Sheet 2: mathematical contract and derivation

### Given, not recovered from the marks

An oriented real affine plane and a choice of comparison/translation/addition are supplied in strips 1–2. Refinements in strip 3 concern a prescribed differentiable path; pictures alone do not guarantee its existence or differentiability. Strip 4 supplies a reversible periodic rotation and a fixed comparison direction. Its cyclic coordinate is a geometric phase only; no complex amplitudes or quantum phase interpretation follows.

For strips 5–8 we choose a two-dimensional state space with dimensionless conjugate coordinates q,p and the nondegenerate oriented area form omega=dq wedge dp. The pairing, its units/scaling, and the interpretation as conjugate variables are assumptions. In physical units p dq has units of action. Drawing a right angle does not establish this pairing, and p is not in general velocity. The arrows here display coordinate increments/components, not arbitrary physical-space directions.

Assume a C1 autonomous vector field X=(u,v), a differentiable local flow Phi_t, and preservation of omega by that flow for every sufficiently small cell. The finite shear in strip 5 illustrates this condition; one preserved patch does not prove it for a general evolution. In two dimensions area preservation gives u_q+v_p=0. With alpha=i_X omega=u dp-v dq, d alpha=(u_q+v_p)dq wedge dp=0. On a simply connected local patch alpha=dH. Thus H_p=u and H_q=-v: qdot=H_p, pdot=-H_q. H is determined only up to an additive constant. The inference is local; topology can obstruct a global single-valued H. This constructs a Hamiltonian generator from specified smooth area-preserving dynamics, not a universal physical energy law.

### Exact turning example (strip 6)

Take H=(q²+p²)/2. Then qdot=p and pdot=-q. The exact step through time h is q'=q cos h+p sin h, p'=p cos h-q sin h. This flow preserves omega and H. The two rate panels are not successive finite kicks. In particular the simultaneous Euler assignment q'=q+h p, p'=p-h q multiplies q²+p² and area by 1+h²; it is not the pictured exact rotation. Cyclic phase here is a property of this example, not a consequence of arbitrary Hamiltonian dynamics.

### Translation example and Noether (strips 7–8)

Switch explicitly to H=p²/2. Its exact flow is Phi_t(q,p)=(q+t p,p). The translation T_a(q,p)=(q+a,p) is canonical and leaves H unchanged, so Phi_t T_a=T_a Phi_t. Its generator Y=partial_q satisfies i_Y omega=dp: its Noether charge is J=p. Along the Hamiltonian motion dJ/dt=pdot=-H_q=0. Equivalently, the action S=integral(p qdot-H)dt is invariant under constant q translations; its Euler–Lagrange equations give the same conservation law. Noether's theorem relates a continuous symmetry of the action to a conserved charge, under its variational hypotheses. Equality of some drawn gap alone is not this theorem. This example has one degree of freedom and no boundary/topological complications.

### Scope

Supplied: geometry, oriented pairing, smoothness, evolution rules, and (for the Noether statement) the variational framework. Derived: the local Hamiltonian form under those hypotheses; exact turning dynamics for one H; translation symmetry and its conserved momentum for another H. Not derived: the origin of these structures in nature, the user's earlier L1/Genesis result, any general identification of holonomy with Noether, quantization, Born weights, Everett branching, or Bell correlations. This is an introductory classical construction, not yet the promised many-worlds explanation.

### Reviewer instructions

Try to falsify this construction. Identify mathematical mistakes, circular reasoning, hidden assumptions, changes in glyph meaning, misleading continuity between panels, missing orientation, conflation of finite/infinite moves, and any suggestion that Hamilton/Noether/quantum mechanics follow from combinatorics alone. Judge the actual visual design as well as this text. Give discrete findings with severity and an actionable remedy; distinguish scientific errors from pedagogy. Do not edit any deliverables. Return your full remarks. They will be retained verbatim, including objections the author disputes or cannot resolve.
