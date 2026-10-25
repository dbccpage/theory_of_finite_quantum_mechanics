"""Independent exact audit; imports no repository code."""
from itertools import product
from fractions import Fraction
import sympy as sp
z=sp.Symbol('z')
cases=0
zero_mode_cases=0
for b,f in product(range(4),repeat=2):
 for spectrum in ((),(1,),(1,2),(1,1,3),(2,3,4)):
  bosons=[0]*b+list(spectrum);fermions=[0]*f+list(spectrum)
  # Construct each trace from its own spectral list.
  poly=sum(z**e for e in bosons)-sum(z**e for e in fermions)
  assert sp.expand(poly)==b-f
  if b==f and b>0:
   assert bosons.count(0)>0 and fermions.count(0)>0
   assert sp.expand(poly)==0
   zero_mode_cases+=1
  for t in (Fraction(0),Fraction(1,2),Fraction(1),Fraction(2)):
   assert sum(t**e for e in bosons)-sum(t**e for e in fermions)==b-f
  cases+=1
assert zero_mode_cases==15
print(f'{cases} independently constructed spectral pairs: symbolic polynomial and four exact weights pass; {zero_mode_cases} zero-index pairs have explicitly counted ground modes')
