"""Independent exact audit; imports no repository code."""
from itertools import product,permutations
states=list(product(range(2),repeat=2))
def controlled(p):return (p[0]^p[1],p[1])
assert all(controlled(controlled(p))==p for p in states)
assert len(set(map(controlled,states)))==4
local=[]
for f,g in product(permutations(range(2)),repeat=2):
 local.append(tuple((f[a],g[b]) for a,b in states))
assert len(set(local))==4
assert tuple(map(controlled,states)) not in local
assert len(list(permutations(states)))==24
for a,b in product(range(4),range(3)):
 # The independent functional model admits assignment cloning on blanks.
 clone_a=lambda x:(x[0],x[0]);clone_b=lambda x:(x[0],x[0])
 ca=clone_a((a,0));cb=clone_b((b,0))
 assert ((ca[0],cb[0]),(ca[1],cb[1]))==((a,b),(a,b))
print('12 product-cloning inputs; controlled flip is an involutive permutation outside the 4 local products among 24 composite permutations')
