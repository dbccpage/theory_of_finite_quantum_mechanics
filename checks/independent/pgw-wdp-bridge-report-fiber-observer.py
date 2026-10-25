"""Independent exact audit; imports no repository code."""
from itertools import product
cases=0
for n in range(5):
 for report in product(range(3),repeat=n):
  image=sorted(set(report))
  for decision in product(range(2),repeat=n):
   constant=all(report[i]!=report[j] or decision[i]==decision[j] for i in range(n) for j in range(n))
   decoders=[]
   for values in product(range(2),repeat=len(image)):
    decoder=dict(zip(image,values))
    if all(decoder[report[i]]==decision[i] for i in range(n)):decoders.append(decoder)
   assert (len(decoders)==1)==constant
   for post in product(range(2),repeat=3):
    if not constant:
     transformed=[post[r] for r in report]
     assert any(transformed[i]==transformed[j] and decision[i]!=decision[j] for i in range(n) for j in range(n))
   cases+=1
print(f'{cases} report/decision maps including empty domain and unused reports: unique-image-decoder equivalence and postprocessing obstruction pass')
