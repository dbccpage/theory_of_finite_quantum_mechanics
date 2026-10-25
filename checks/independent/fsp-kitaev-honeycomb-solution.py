"""Independent exact audit; imports no repository code."""
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
W=s.kronecker_product(Z,I);H=s.kronecker_product(Z,X)
P0=s.diag(1,1,0,0);P1=s.diag(0,0,1,1)
assert W*W==s.eye(4) and H*H==s.eye(4)
assert W*H==H*W
assert P0+P1==s.eye(4) and P0*P1==s.zeros(4)
assert P0*H==H*P0 and P1*H==H*P1
assert H[:2,:2]==X and H[2:,2:]==-X
# Independent complex Majorana realization of each matter block.
Y=s.Matrix([[0,-s.I],[s.I,0]])
assert Z*Z==I and Y*Y==I and Z*Y==-Y*Z and s.I*Z*Y==X
print('Exact 4x4 flux/hopping matrices: involutions, commutator, complementary projectors and both sector blocks pass; i*Z*Y=X')
