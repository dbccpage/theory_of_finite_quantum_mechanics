# Review of first submitted rational-homogeneity proof

Written proof accepted on mathematical review, with these corrections kept separate from the submitted source:

- Read the multiplication commas as multiplication, e.g. k p(B), not an ordered pair.
- In the integer-multiple lemma, explicitly split n=0. Only k=0 occurs and p(0)=0 handles it. In the induction step k<n ensures n>0 before any division, so this is clarification rather than a counterexample.
- Real scalar multiplication is not defined on an arbitrary rational vector space. In a real ordered vector space with real-valued p, positivity and effect-additivity already yield monotonicity; rational squeezing then yields real homogeneity on admissible segments. No independent monotonicity assumption is required.
- Rational effect homogeneity alone is not Born uniqueness. Matrix representation and the operational justification of the input assumptions remain separate.

Status: reviewed written proof; no Lean certificate, executable proof replay, or full Born claim.
