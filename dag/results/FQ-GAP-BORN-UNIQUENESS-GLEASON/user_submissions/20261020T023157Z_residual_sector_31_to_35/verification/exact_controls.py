"""Bounded exact controls for the saved RS review, not a general LP solver/proof."""
import sys,json
from fractions import Fraction as F
from pathlib import Path
from dataclasses import replace
sys.dont_write_bytecode=True
ROOT=Path(sys.argv[1]);sys.path.insert(0,str(ROOT/'code/python/src'))
from functional.l1_seminorm import L1Seminorm,ExactPhi1Certificate,L1SeminormError
checks=[];certs=[];mutations=[]
def require(ok,label):
    if not ok: raise RuntimeError(label)
    checks.append(label)
def dot(a,b):return sum((F(x)*F(y) for x,y in zip(a,b)),F(0))
def cert(label,omega,boundary,weights,alpha,dual,value):
    w=list(map(F,weights));om=list(map(F,omega));aa=list(map(F,alpha));bb=[list(map(F,row)) for row in boundary]
    rr=[x-dot(row,aa) for x,row in zip(om,bb)]
    obj=ExactPhi1Certificate(om,bb,w,aa,rr,list(map(F,dual)),F(value))
    require(L1Seminorm(bb,w).verify_certificate(obj).value==value,label+' public verifier')
    require(sum(wi*abs(ri) for wi,ri in zip(w,rr))==dot(dual,om)==value,label+' independent primal/dual equality')
    require(all(dot([row[j] for row in bb],dual)==0 for j in range(len(aa))),label+' independent annihilator')
    require(all(abs(F(z))<=wi for z,wi in zip(dual,w)),label+' independent dual box')
    certs.append((label,obj));return rr
P=[[-1,1]]*4;omega=[0,0,1,2];dual=[-1,-1,1,1]
rs={}
for t in [F(0),F(1,2),F(2,3),F(3,4),F(1)]:rs[t]=cert('parallel4 t='+str(t),omega,P,[1]*4,[0,t],dual,3)
def masses(r,w):
    phi=sum(F(x)*abs(y) for x,y in zip(w,r));return [F(x)*abs(y)/phi for x,y in zip(w,r)]
for t in rs:
    mu=masses(rs[t],[1]*4);require(mu==[t/3,t/3,(1-t)/3,(2-t)/3],'parallel4 mass formula '+str(t))
for t,expected in [(F(1,2),F(1,3)),(F(3,4),F(1,2)),(F(2,3),F(4,9))]:
    require(sum(masses(rs[t],[1]*4)[:2])==expected,'selector sector '+str(t))
require(8*F(3,4)-6==0,'quadratic derivative root')
require(F(2,3)**2==(1-F(2,3))*(2-F(2,3)),'entropy stationary equation')
require(all(rs[a][j]*rs[b][j]>=0 for a in rs for b in rs for j in range(4)),'sampled minimizers share signs')
avg=[(a+b)/2 for a,b in zip(rs[F(0)],rs[F(1)])]
require(avg==rs[F(1,2)],'two-atom repair barycenter')
require([(a+b)/2 for a,b in zip(masses(rs[F(0)],[1]*4),masses(rs[F(1)],[1]*4))]==masses(avg,[1]*4),'mixture mass equals Dirac barycenter mass')
require(rs[F(0)]!=avg!=rs[F(1)],'ensemble support differs despite same mass outputs')
C=[[-1,1,0,0],[0,-1,1,0],[0,0,-1,1],[1,0,0,-1]]
for k,alpha in enumerate([[0,0,0,0],[0,1,0,0],[0,1,1,0],[0,1,1,1]]):
    r=cert('cycle4 vertex '+str(k),[1,0,0,0],C,[1]*4,alpha,[1]*4,1)
    require(r==[F(j==k) for j in range(4)],'cycle vertex residual '+str(k))
T=[[-1,1,0,0],[0,-1,1,0],[1,0,-1,0],[-1,0,0,1]]
for k,alpha in enumerate([[0,0,0,0],[0,1,0,0],[0,1,1,0]]):
    r=cert('triangle bridge vertex '+str(k),[1,0,0,0],T,[1]*4,alpha,[1,1,1,0],1)
    require(r[3]==0 and sum(masses(r,[1]*4)[:3])==1,'triangle bridge constant sector '+str(k))
for t in [F(0),F(1,2),F(1)]:
    cert('distinct weights t='+str(t),[0,0,1],[[-1,1]]*3,[1,2,3],[0,t],[-1,-2,3],3)
# Algebraic entropy countermodel. No floating entropy calculation or approximate root.
f=lambda t:2*t**3-6*t**2+11*t-6
require(f(F(4,5))<0<f(F(5,6)),'entropy cubic rational isolating interval')
require(f(F(1,2))!=0,'only possible rational root in (0,1) rejected')
for t in [F(0),F(1,2),F(1)]:
    require(t**3-(1-t)*(2-t)*(3-t)==f(t),'entropy cubic identity fixture '+str(t))
# Positive, singular positive, and rejected trace-one completions with same diagonal.
require(F(1,4)-F(0)**2>0,'zero coherence positive determinant')
require(F(1,4)-F(1,2)**2==0,'half coherence PSD boundary')
require(F(1,4)-F(1)**2==F(-3,4),'unit coherence negative determinant')
require(F(1,2)+F(1,2)-2<0,'unit coherence negative quadratic form')
# Actual public verifier mutations; guards remain active under python -O.
base=certs[0][1]
for label,bad in [('wrong objective',replace(base,reported_value=F(4))),('wrong residual',replace(base,primal_residual=[F(1)]*4)),('wrong dual box',replace(base,dual_witness=[F(-2),F(-2),F(2),F(2)])),('wrong dual annihilator',replace(base,dual_witness=[F(1)]*4)),('wrong alpha',replace(base,alpha=[F(0),F(1,2)])),('float objective',replace(base,reported_value=3.0))]:
    try:L1Seminorm(P,[1]*4).verify_certificate(bad)
    except L1SeminormError:mutations.append({'name':label,'status':'REJECTED'})
    else:raise RuntimeError('mutation accepted: '+label)
print(json.dumps({'scope':'Bounded Fraction fixture replay and public rational primal/dual verifier; no general LP or Lean proof.','checks_passed':len(checks),'check_labels':checks,'primal_dual_certificates':len(certs),'mutations':mutations,'fixtures':[{'label':label,'omega':list(map(str,c.omega)),'d0':[[str(v) for v in row] for row in c.d0],'weights':list(map(str,c.weights)),'alpha':list(map(str,c.alpha)),'residual':list(map(str,c.primal_residual)),'dual':list(map(str,c.dual_witness)),'value':str(c.reported_value)} for label,c in certs]},indent=2))
