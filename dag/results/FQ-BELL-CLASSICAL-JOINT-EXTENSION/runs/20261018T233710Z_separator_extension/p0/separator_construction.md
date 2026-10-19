# Selected next Bell work unit: separator reduction

Pair order 00,01,10,11 and cells --,-+,+-,++. Admit exact Q-valued
nonnegative normalized pairs with matching one-party marginals. No supplied
four-variable law is assumed. For B_y=b let u=P(A0+,b), v=P(A1+,b),
w=P(b). The free ++b mass t_b obeys max(0,u+v-w)<=t_b<=min(u,v).
Thus the free separator r=P(A0+,A1+) lies in [sum lower_b,sum upper_b].
Choose r in both setting intervals. Split each triple using
t_-=max(lower_-,r-upper_+), t_+=r-t_-. Fill the other cells by
u-t_b, v-t_b, w-u-v+t_b. Glue the two triples by
p(s,b0,b1)=T0(s,b0)*T1(s,b1)/q(s) for q(s)>0; use zero for q(s)=0.
This zero branch is licensed by nonnegativity and equal separator marginals.

Prove at common integer scale D: the separator intervals overlap iff all
eight CHSH facets hold, assuming all 16 observed cells are nonnegative.
Prove existence of the two nonnegative triple cell systems with common r.
Retain the all-facet common-law necessity theorem. The general Q-valued
conditional-gluing and input-transport proofs remain explicit obligations;
native extension certificates are accepted only by actual projection checks.

Fine 1982 is source orientation, not an imported proof or accepted result:
https://doi.org/10.1103/PhysRevLett.48.291
Primary author-hosted paper: https://faculty.washington.edu/afine/PRL1982.pdf
The construction and forthcoming Lean proof in this run are new local work.
