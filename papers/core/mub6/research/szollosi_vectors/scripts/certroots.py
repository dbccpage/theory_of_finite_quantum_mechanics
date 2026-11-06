"""Certified real solutions from an msolve rational parametrization, independent of msolve's own boxes.
Real roots of each exact factor of ELIM: isolated by FLINT (arb_fmpz_poly_complex_roots), refined by Newton
in ball arithmetic, then certified by an exact rational sign change of the factor on [lo, hi].
Coordinates x_i = -NUM_i(A)/(c_i DER(A)) are enclosed in balls by evaluating on [lo, hi].
Real-root approximations and Sturm counts come from PARI (approx file: [k, sturm_count, [roots]] per factor);
the number of certified disjoint intervals must equal the Sturm count.
Usage: certroots.py output.par approx.txt out.json"""
import sys, json, time
import flint
from flint import arb, fmpq, fmpz_poly, arb_poly, ctx
from param import load_param
t0=time.time(); log=lambda *a: print(f"[{time.time()-t0:7.1f}s]",*a,flush=True)
names,lin,elim,der,nums,_=load_param(sys.argv[1])
import ast
APX=[ast.literal_eval(l.replace("~","").replace(" E","e").replace("E","e")) for l in open(sys.argv[2]) if l.strip()]
c,fl=elim.factor(); fl=sorted(fl,key=lambda t:t[0].degree())
log("factors",len(fl))
WP=24000; EPS_BITS=3000
def q_of(a):  # exact rational of an arb midpoint
    m,e=a.mid().man_exp(); m=int(m); e=int(e)
    return fmpq(m*2**e) if e>=0 else fmpq(m,2**(-e))
sols=[]; nreal=[]
for k,(f,_) in enumerate(fl):
    kk,nst,rs=APX[k]
    assert kk==k
    ctx.prec=WP
    rr=[arb(x) for x in rs]
    if len(rr)!=nst: raise SystemExit("count mismatch")
    nreal.append(nst); ivs=[]
    F=arb_poly([arb(x) for x in f.coeffs()]); dF=F.derivative()
    NUM=[(arb_poly([arb(x) for x in n.coeffs()]),int(cc)) for n,cc in nums]; DER=arb_poly([arb(x) for x in der.coeffs()])
    for r in rr:
        x=arb(q_of(r))
        for _ in range(8): x=arb(q_of(x-F(x)/dF(x)))
        xr=q_of(x); xr=fmpq(int(xr.p*2**(EPS_BITS+64)//xr.q),2**(EPS_BITS+64))  # round to EPS_BITS+64 bits
        eps=fmpq(1,2**EPS_BITS); lo=xr-eps; hi=xr+eps
        if not (f(lo)*f(hi)<0): raise SystemExit(f"no certified sign change in factor {k}")
        ivs.append((lo,hi))
        if len(ivs)%10==0: log("factor",k,"certified",len(ivs))
        X=arb(lo).union(arb(hi))
        coords=[-(N(X))/(cc*DER(X)) for N,cc in NUM]
        ctx.prec=300
        sols.append({"factor":k,"deg":f.degree(),"coords":[[a.mid().str(90,radius=False),a.rad().str(5,radius=False)] for a in (+(c) for c in coords)],
                     "rad_max":max(float(a.rad()) for a in coords)})
        ctx.prec=WP
    ivs.sort()
    if any(ivs[i][1]>=ivs[i+1][0] for i in range(len(ivs)-1)): raise SystemExit("intervals overlap")
    if len(rr): log("factor",k,"deg",f.degree(),"Sturm count",nst,"certified disjoint intervals",len(ivs))
ctx.prec=300
# disjointness: the isolating intervals came from FLINT's isolation of distinct roots; check distinct coordinates too
log("real solutions",len(sols),"max coordinate radius %.2e" % max(s["rad_max"] for s in sols))
json.dump({"nreal_per_factor":nreal,"factor_degrees":[f.degree() for f,_ in fl],"sols":sols},open(sys.argv[3],"w"))
