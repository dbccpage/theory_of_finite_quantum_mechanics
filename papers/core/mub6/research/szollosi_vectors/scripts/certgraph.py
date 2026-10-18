"""Ball-arithmetic orthogonality / unbiasedness graph from certroots.py output.
A pair is certified not orthogonal when Re or Im of <v,v'> excludes 0, and certified not unbiased
when |<v,v'>|^2 - 6 excludes 0. Pairs whose balls contain 0 are candidates (exact check needed).
Coordinates: a1..a5, b1..b5, then parameters (e.g. aw, bw) that label S; pairs are taken within one S."""
import sys, json, itertools
import networkx as nx
from flint import arb, ctx
ctx.prec=300
d=json.load(open(sys.argv[1])); sols=d["sols"]
B=[[arb(m,r) for m,r in s["coords"]] for s in sols]
def lab(s): return tuple(round(float(c.mid()),9) for c in s[10:])
groups={}
for k,s in enumerate(B): groups.setdefault(lab(s),[]).append(k)
out={"groups":{}}
for L,idx in sorted(groups.items()):
    oc=[];uc=[]
    for p,q in itertools.combinations(idx,2):
        P,Q=B[p],B[q]
        re=1+sum(P[j]*Q[j]+P[j+5]*Q[j+5] for j in range(5)); im=sum(P[j]*Q[j+5]-P[j+5]*Q[j] for j in range(5))
        if all(P[j].overlaps(Q[j]) for j in range(len(P))): raise SystemExit("two solutions not separated")
        if re.contains(0) and im.contains(0): oc.append((p,q))
        if (re*re+im*im-6).contains(0): uc.append((p,q))
    G=nx.Graph(); G.add_nodes_from(idx); G.add_edges_from(oc)
    cl=[sorted(c) for c in nx.enumerate_all_cliques(G) if len(c)==6]
    out["groups"][str(L)]={"rays":idx,"orth_candidates":oc,"unb_candidates":uc,"six_cliques":cl,
        "clique_factor_degrees":[[sols[k]["deg"] for k in c] for c in cl]}
    print("S",L,": rays",len(idx),"| orth candidates",len(oc),"| unbiased candidates",len(uc),
          "| 6-cliques",len(cl),"| largest clique",max((len(c) for c in nx.find_cliques(G)),default=0),
          "| clique factor degrees",out["groups"][str(L)]["clique_factor_degrees"][:3])
json.dump(out,open(sys.argv[2],"w"))
