Status: AI-drafted, awaiting human review.

# FSP-COBORDISM-INTRINSIC-SIGN: classification of vertex-sign switching on a triangle

For every assignment of Boolean edge signs to a triangle and every Boolean vertex switching, the XOR of the three edge signs is invariant. A switching makes all three edge signs positive exactly when their XOR is zero. An explicit switching gives the normal form (0,0,parity), and the product of integer edge signs equals the sign of that parity. A negative-parity triangle is obstructed within this switching class, whereas a balanced triangle with two negative edges can be made positive.

AuthorityEffect: None.

## Derivation

Encode a positive edge by zero and a negative edge by one. Switching vertex i by g_i replaces an edge sign s_ij by g_i+s_ij+g_j modulo two. In the three-edge cycle sum, each vertex label occurs twice and cancels. Thus cycle parity is invariant.

Choose g_0=0, g_1=s_01 and g_2=s_01+s_12. The first two transformed signs are zero and the last is the original cycle parity. This provides a constructive normal form, so an all-positive representative exists exactly for zero parity.

Mapping each Boolean sign to 1 or -1 identifies cycle parity with the product of the edge weights. A triangle with exactly one negative edge cannot be made positive by these switchings. A triangle with two negative edges is balanced and has an explicit positive switching. Negative entries alone therefore do not characterize the switching obstruction.

The independent check conjugates each integer adjacency matrix by each diagonal sign matrix and verifies the classification and constructive normal form. Its representation class is the same declared vertex-switching class, with an independent matrix implementation.

## What is proved

For every assignment of Boolean edge signs to a triangle and every Boolean vertex switching, the XOR of the three edge signs is invariant. A switching makes all three edge signs positive exactly when their XOR is zero. An explicit switching gives the normal form (0,0,parity), and the product of integer edge signs equals the sign of that parity. A negative-parity triangle is obstructed within this switching class, whereas a balanced triangle with two negative edges can be made positive.

## What is assumed

The mathematical structures and operations are exactly those declared in `lean4/CampaignSignedTriangleSwitching.lean`. Only diagonal vertex-sign switching on one three-cycle is classified. No spin bordism group, eta invariant, fermion representation, bulk cancellation or obstruction over all representations is computed. The original cobordism-based intrinsic-sign claim remains open.

## What is open

Claimed: a 4D boundary fermion theory with nontrivial invariant exp(2 pi i eta) in Omega_5^Spin(B Z2) has an unremovable sign problem curable only by a 5D bulk; no computation of the bordism group, eta invariant or sign obstruction exists in this checkout.

Relate the anomaly invariant to the sign of a declared finite representation and rule out every representation in a stated class; anomaly-based intrinsic sign results in the literature are class specific.
