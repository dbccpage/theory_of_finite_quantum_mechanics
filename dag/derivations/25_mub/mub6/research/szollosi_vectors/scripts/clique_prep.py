"""For the candidate cliques of certgraph.py, write a small GP file: the factors holding their rays,
the coordinates reduced exactly to Q[A]/f (x_i = -NUM_i/(c_i DER) mod f), and each ray's (factor, root index).
Usage: clique_prep.py output.par cert.json certgraph.json out.gp"""
import sys, json
import flint
from flint import fmpq_poly, fmpz_poly
from param import load_param
names,lin,elim,der,nums,_=load_param(sys.argv[1])
c,fl=elim.factor(); fl=sorted(fl,key=lambda t:t[0].degree())
cert=json.load(open(sys.argv[2])); g=json.load(open(sys.argv[3]))
sols=cert["sols"]; ridx=[]; seen={}
for s in sols: k=s["factor"]; ridx.append(seen.get(k,0)); seen[k]=seen.get(k,0)+1
cl=[c for grp in g["groups"].values() for c in grp["six_cliques"]]
need=sorted({sols[r]["factor"] for c in cl for r in c})
def gp(p): return "Polrev([%s],A)" % ",".join(str(x) for x in p.coeffs())
with open(sys.argv[4],"w") as f:
    f.write("KS=%s;\nFAC=[%s];\n" % ([k for k in need], ",".join(gp(fl[k][0]) for k in need)))
    Xs=[]
    for k in need:
        F=fmpq_poly(fl[k][0].coeffs()); D=fmpq_poly(der.coeffs())%F
        G,S,T=D.xgcd(F); assert G.degree()==0; Dinv=S/G[0]
        Xs.append("[%s]" % ",".join("Polrev([%s],A)" % ",".join(str(x) for x in ((-fmpq_poly(n.coeffs())*Dinv/int(cc))%F).coeffs()) for n,cc in nums))
    f.write("X=[%s];\n" % ",".join(Xs))
    f.write("CL=%s;\n" % [[[need.index(sols[r]["factor"])+1, ridx[r]+1] for r in c] for c in cl])
print("factors needed",need,"degrees",[fl[k][0].degree() for k in need],"cliques",len(cl))
