"""Exact graph analysis from the GP status file: 0 orthogonal, 1 unbiased, 2 neither."""
import sys, itertools, json
import networkx as nx
rows=eval([l for l in open(sys.argv[1]).read().split('\n') if l.strip()][-1])
st={}
for k1,i1,k2,i2,s in rows:
    a=(k1,i1); b=(k2,i2)
    if a==b: continue
    key=frozenset((a,b))
    if key in st and st[key]!=s: raise SystemExit("inconsistent status")
    st[key]=s
nodes=sorted({n for k in st for n in k})
n=len(nodes); full=n*(n-1)//2
print("rays",n,"pairs with status",len(st),"of",full)
G=nx.Graph(); G.add_nodes_from(nodes)
G.add_edges_from(tuple(k) for k,s in st.items() if s==0)
print("orthogonal pairs",G.number_of_edges(),"unbiased pairs",sum(1 for s in st.values() if s==1))
bases=[c for c in nx.enumerate_all_cliques(G) if len(c)==6]
print("orthonormal bases (6-cliques)",len(bases),"; largest clique",max(len(c) for c in nx.find_cliques(G)))
mub=[(i,j) for (i,b1),(j,b2) in itertools.combinations(enumerate(bases),2)
     if all(st[frozenset((p,q))]==1 for p in b1 for q in b2)]
print("mutually unbiased pairs of bases",len(mub))
json.dump({"rays":n,"orth":G.number_of_edges(),"bases":[sorted(map(list,b)) for b in bases],"mub_pairs":mub},open(sys.argv[2],'w'))
