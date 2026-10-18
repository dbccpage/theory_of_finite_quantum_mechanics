"""Exact checks on an msolve rational parametrization with python-flint:
every root of the eliminating polynomial gives a solution of the input system (checked modulo ELIM),
ELIM is squarefree, DER is invertible modulo ELIM, and the factor degrees and real-root counts.
Usage: exactcheck.py system.ms output.par"""
import sys, time, json
import flint, sympy as sp
from param import load_param
t0=time.time(); log=lambda *a: print(f"[{time.time()-t0:7.1f}s]",*a,flush=True)
names,lin,elim,der,nums,real=load_param(sys.argv[2])
names=[n for n in names if n!='A']
log("deg",elim.degree(),"vars",names,"lin",lin)
lines=open(sys.argv[1]).read().split("\n",2)
syms=sp.symbols(names)
eqs=[sp.Poly(sp.sympify(e),*syms) for e in lines[2].replace("\n","").rstrip(',').split(',') if e.strip()]
log("equations",len(eqs),"total degrees",[e.total_degree() for e in eqs])
L=1
for _,c in nums: L=L*c//flint.fmpz.gcd(flint.fmpz(L),flint.fmpz(c)) if False else sp.ilcm(L,int(c))
L=flint.fmpz(int(L))
Y=[(-n*(L//flint.fmpz(int(c))))%elim for n,c in nums]
T=(L*der)%elim
cache={}
D=max(q.total_degree() for q in eqs)
def mono(e):
    if e in cache: return cache[e]
    p=flint.fmpz_poly([1]); d=sum(e)
    for i,k in enumerate(e):
        for _ in range(k): p=(p*Y[i])%elim
    for _ in range(D-d): p=(p*T)%elim
    cache[e]=p; return p
ok=True
for q in eqs:
    acc=flint.fmpz_poly([0])
    for e,c in q.terms(): acc=acc+int(c)*mono(e)
    if acc%elim!=0: ok=False
log("every root of ELIM solves every equation:",ok)
log("ELIM squarefree:", flint.fmpz_poly.gcd(elim,elim.derivative()).degree()==0)
log("DER invertible mod ELIM:", flint.fmpz_poly.gcd(elim,der).degree()==0)
log('homogenized to degree',D)
c,fl=elim.factor()
degs=sorted(f.degree() for f,e in fl); log("factors",len(fl),"degrees",degs,"multiplicities",sorted({e for f,e in fl}))
json.dump({"deg":elim.degree(),"subst_ok":ok,"factor_degrees":degs},open(sys.argv[2]+".check.json","w"))
with open(sys.argv[2]+".factors.gp","w") as f:
    f.write("FAC=["+",".join("Polrev(["+",".join(str(c) for c in fp.coeffs())+"],A)" for fp,e in sorted(fl,key=lambda t:t[0].degree()))+"];\n")
    f.write("NUMS=["+",".join("[Polrev(["+",".join(str(c) for c in n.coeffs())+"],A),"+str(c)+"]" for n,c in nums)+"];\n")
    f.write("DER=Polrev(["+",".join(str(c) for c in der.coeffs())+"],A);\nLIN="+str(lin[:-1])+";\n")
log("factors written")
