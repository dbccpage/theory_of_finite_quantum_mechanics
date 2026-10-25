"""Independent exact audit; imports no repository code."""
for m in range(2,101):
 roots=[k for k in range(2*m) if (2*k)%(2*m)==2]
 assert roots==[1,m+1],(m,roots)
 # Angles are represented exactly as rational multiples of pi.
 from fractions import Fraction
 assert Fraction(m+1,m)-Fraction(1,m)==1
assert [k for k in range(6) if (2*k)%6==2]==[1,4]
print('99 denominators: exactly two exchange residues for each specified monodromy; m=3 roots 1 and 4 differ by pi. No Berry phase calculated.')
