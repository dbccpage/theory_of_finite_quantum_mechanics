import L02TerminalNonBypass

/-!
# CODA-MUR: Soundness is the L02 non-bypass kernel

Publication wrapper. The load-bearing statements are in
`L02TerminalNonBypass.lean`: target authority unfolds to a
terminal plus `IsAuth`, and a descent certificate χ alone does not imply
target standing. There is no vacuous `True` soundness theorem here.
-/

#check CODA_MUR.targetAuthority_unfolds
#print axioms CODA_MUR.targetAuthority_unfolds
#check CODA_MUR.targetAuthority_implies_terminalized
#print axioms CODA_MUR.targetAuthority_implies_terminalized
#check CODA_MUR.chi_alone_does_not_imply_target_authority
#print axioms CODA_MUR.chi_alone_does_not_imply_target_authority
