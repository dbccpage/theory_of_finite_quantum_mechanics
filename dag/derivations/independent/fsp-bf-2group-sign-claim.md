Status: AI-drafted, awaiting human review.

# FSP-BF-2GROUP-SIGN-CLAIM: a normalized Z2 cocycle with an unavoidable generator sign

For the additive group Z2 with trivial Z2 coefficient action, the Boolean 3-cochain omega(a,b,c)=a*b*c is normalized and satisfies the cocycle identity. Every normalized 2-cochain beta has coboundary zero at (1,1,1), whereas omega is one there. Thus omega is not a normalized coboundary, and normalized 2-cochain rephasing leaves a negative sign at that triple.

AuthorityEffect: None.

## Derivation

Write group addition and coefficient addition modulo two. Define omega(a,b,c)=abc, and define the coboundary of beta as beta(b,c)+beta(a+b,c)+beta(a,b+c)+beta(a,b). The coefficient action is trivial. Normalization requires beta(0,x)=beta(x,0)=0.

The cocycle identity is checked for every quadruple of group elements. Normalization of omega follows when any argument is zero. These finite statements have kernel proofs, and the independent checker uses multiplicative signs instead of Boolean XOR.

At the generator triple, the coboundary is beta(1,1)+beta(0,1)+beta(1,0)+beta(1,1)=0. In contrast, omega(1,1,1)=1. This rules out equality with every normalized coboundary, including either possible value of beta(1,1).

Rephasing adds the coboundary to omega. Consequently the sign at the generator triple remains -1. An all-positive representative cannot be reached within this explicitly defined normalized-cochain class. This is a finite algebraic obstruction; interpreting it as a BF amplitude requires a separate construction.

## What is proved

For the additive group Z2 with trivial Z2 coefficient action, the Boolean 3-cochain omega(a,b,c)=a*b*c is normalized and satisfies the cocycle identity. Every normalized 2-cochain beta has coboundary zero at (1,1,1), whereas omega is one there. Thus omega is not a normalized coboundary, and normalized 2-cochain rephasing leaves a negative sign at that triple.

## What is assumed

The mathematical structures and operations are exactly those declared in `lean4/CampaignBfCocycleObstruction.lean`. The result concerns the explicitly defined Z2 cochain model and normalized rephasings. It constructs no BF state sum, 2-group gauge dynamics, knotted-worldsheet amplitude or three-loop braiding observable. No general cancellation or sign-free theorem follows.

## What is open

Claimed: in BF theory on finite cell complexes, the Postnikov class in H^3(G, A) governs cancellation of higher 2-group sign anomalies on knotted worldsheets; no BF model, linking computation or cancellation identity exists in this checkout.

Define the finite BF or 2-group gauge model, compute the 3-loop braiding phases and state exactly which weights become nonnegative; ledger GIN-C19 to GIN-C21 withdraw the fixture readings.
