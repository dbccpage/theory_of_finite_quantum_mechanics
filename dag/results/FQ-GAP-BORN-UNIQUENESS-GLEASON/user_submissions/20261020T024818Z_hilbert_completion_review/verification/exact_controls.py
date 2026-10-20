"""Bounded HL fixtures only. No spectral transcendence or infinite-limit computation."""
from fractions import Fraction as F
import json,sys
sys.dont_write_bytecode=True
checks=[]
def require(x,label):
    if not x:raise RuntimeError(label)
    checks.append(label)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def l1(x):return sum(abs(t) for t in x)
def n2(x,w=None):return sum((t*t*(F(1) if w is None else w[i]) for i,t in enumerate(x)),F(0))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
u=(F(1),F(0));v=(F(0),F(1));L=l1(add(u,v))**2+l1(sub(u,v))**2;R=2*l1(u)**2+2*l1(v)**2
require(L==8 and R==4,'l1 two-cell parallelogram 8 versus 4')
require(L!=R,'l1 completion cannot preserve norm and become Hilbert')
w=(F(3),F(5));require(n2(add(u,v),w)+n2(sub(u,v),w)==2*n2(u,w)+2*n2(v,w),'declared weighted quadratic norm parallelogram fixture')
x=F(2);parent=F(3);children=(F(1),F(2))
require(parent*x*x==sum(t*x*x for t in children),'function pullback with additive weights isometric')
require(parent*x*x!=sum(t*x*x for t in [F(1),F(3)]),'nonadditive constant pullback fails')
a=F(6);masses=[a*t/parent for t in children]
require(sum(masses)==a,'density refinement conserves cell mass')
require(a*a/parent==sum(m*m/t for m,t in zip(masses,children)),'density inverse-weight norm preserved')
require(a*a/parent!=sum(a*a/t for t in children),'constant-copy density map fails')
require(F(2)*F(2)-1==3 and F(2)>0,'non-diagonal swap-invariant Gram matrix positive definite')
f=lambda t:t**3+t**2-2*t-1
intervals=[(F(1),F(3,2)),(F(-1,2),F(0)),(F(-2),F(-3,2))]
signs=[]
for k,(lo,hi) in enumerate(intervals):
    require(f(lo)*f(hi)<0,'seventh-root cubic isolation sign change '+str(k+1))
    require(hi<2,'factor 2-t positive on interval '+str(k+1))
    sign=1 if lo>-1 else -1 if hi<-1 else 0
    require(sign!=0,'factor t+1 has fixed sign on interval '+str(k+1));signs.append(sign)
for t in [F(-2),F(-1,2),F(0),F(1),F(3,2)]:
    require(2+t-t*t==(2-t)*(t+1),'weight difference factorization fixture '+str(t))
require(signs==[1,1,-1],'k1 and k2 preserve order; k3 reverses')
# Growth isometry does not imply cochain compatibility.
old=(F(1),);extended=(F(1),F(0))
require(n2(old)==n2(extended),'zero extension norm isometric')
require(extended[1]-extended[0]==-1!=0,'new edge violates differential commutation')
# Graph weighted incidence estimate, edge counted once.
vertex=(F(2),F(-1));edge_weight=F(3);vertex_weights=(F(1),F(2))
energy=edge_weight*(vertex[1]-vertex[0])**2;degree=max(edge_weight/t for t in vertex_weights)
require(energy==27 and n2(vertex,vertex_weights)==6,'graph edge and vertex energies')
require(energy<=2*degree*n2(vertex,vertex_weights),'graph degree estimate fixture')
# Finite witnesses for the written nonclosable infinite functional.
N=8
seq=[]
for k in [1,2,4,8]:
    z=[F(0)]*N;z[k-1]=F(1,k);seq.append(z)
    require(n2(z)==F(1,k*k),'nonclosability shrinking norm fixture '+str(k))
    require(dot(list(map(F,range(1,N+1))),z)==1,'nonclosability constant image fixture '+str(k))
for z in seq[1:]:
    require(dot(list(map(F,range(1,N+1))),sub(z,seq[0]))==0,'nonclosability zero image differences fixture '+str(n2(z)))
# State inequality in exact squared arithmetic, no square-root approximation.
x=(F(1),F(0));y=(F(3,5),F(4,5))
l1density=sum(abs(a*a-b*b) for a,b in zip(x,y));rhs2=n2(sub(x,y))*n2(add(x,y))
require(l1density*l1density<=rhs2,'density Cauchy-Schwarz bound fixture')
require((l1density/2)**2<=n2(sub(x,y)),'normalized TV bound fixture')
yminus=tuple(-a for a in x)
require(sum(abs(a*a-b*b) for a,b in zip(x,yminus))==0 and n2(add(x,yminus))==0,'opposite phase gives zero density difference and RHS')
x=(F(3,5),F(4,5));px=(F(3,5),F(0))
require(n2(x)==1 and n2(px)==F(9,25),'projected state is subnormalized')
require(n2(px)+F(16,25)==1,'explicit missing mass restores normalization')
# Piecewise hat function: bounded integrals, not a general domain solver.
hat_norm2=2*F(1,2)**3/3;hat_energy=F(1)
require(hat_norm2==F(1,12) and hat_energy/hat_norm2==12,'hat function form Galerkin coefficient 12')
# Diagonal finite Galerkin resolvents illustrate the exact tail identities.
lam=(F(1),F(2),F(3));vec=(F(1),F(1,2),F(1,3));full=tuple(v/(a+1) for a,v in zip(lam,vec));errors=[]
for n in [1,2,3]:
    r=tuple(vec[i]/(lam[i]+1) if i<n else F(0) for i in range(3));tail=n2(sub(full,r));errors.append(tail)
    require(tail==sum(full[i]**2 for i in range(n,3)),'Galerkin resolvent tail identity '+str(n))
    if n<3:
        missing=[F(0)]*3;missing[n]=F(1)
        require(n2(missing)==1,'proper projection norm error witness at time zero '+str(n))
require(errors[0]>errors[1]>errors[2]==0,'finite diagonal resolvent errors decrease')
guards=[('l1 satisfies parallelogram',L==R),('k2 reverses weights',signs[1]<0),('nonadditive constant map is isometric',parent*x[0]**2==sum(t*x[0]**2 for t in [F(1),F(3)])),('zero extension commutes on new edge',extended[1]-extended[0]==0),('projected state still normalized',n2(px)==1),('constant density copy preserves norm',a*a/parent==sum(a*a/t for t in children))]
for name,value in guards:
    if value:raise RuntimeError('false claim survived: '+name)
print(json.dumps({'scope':'Bounded Fraction identities, inequalities and counterexample fixtures; no infinite-limit, transcendence or operator-domain theorem verified computationally.','checks_passed':len(checks),'checks':checks,'false_claim_guards':[{'name':n,'status':'REJECTED'} for n,v in guards],'exp_minus_i_transcendence':'EXTERNAL_NAMED_IMPORT_NOT_NUMERICALLY_TESTED','strong_resolvent_and_unitary_limit':'WRITTEN_CONDITIONAL_ARGUMENT_NOT_A_FINITE_REPLAY_RESULT','original_gap_closed':False},indent=2))
