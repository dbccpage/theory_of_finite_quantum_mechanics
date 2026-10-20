"""Exact finite GF witnesses. No random sampling or general Gleason proof."""
import sys,json
from fractions import Fraction as F
sys.dont_write_bytecode=True
checks=[]
def require(x,label):
    if not x:raise RuntimeError(label)
    checks.append(label)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def scale(c,v):return tuple(c*x for x in v)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def basis(B):return all(dot(x,y)==F(i==j) for i,x in enumerate(B) for j,y in enumerate(B))
def quad(r,v):return sum((v[i]*r[i][j]*v[j] for i in range(len(v)) for j in range(len(v))),F(0))
def diag(xs):return [[F(x) if i==j else F(0) for j in range(len(xs))] for i,x in enumerate(xs)]
E=((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(0),F(0),F(1)))
v=(F(20,29),F(21,29),F(0));u=(F(21,29),F(-20,29),F(0));z=E[2]
Bp=(v,u,z);B=(v,add(scale(F(3,5),u),scale(F(4,5),z)),add(scale(F(-4,5),u),scale(F(3,5),z)))
require(basis(Bp),'Bprime exactly orthonormal')
require(basis(B),'B exactly orthonormal')
p=[x[0]**2 for x in B];pp=[x[0]**2 for x in Bp]
require(sum(p)==sum(pp)==1,'CE2 squared overlaps sum to one')
require(p[0]>p[1] and p[0]>p[2],'CE2 shared v uniquely wins B')
require(pp[1]>pp[0] and pp[1]>pp[2],'CE2 shared v loses Bprime')
require(B[0]==Bp[0],'CE2 exact shared vector')
def l1prob(B):return abs(B[0][0])/sum(abs(x[0]) for x in B)
require(l1prob(Bp)==F(20,41),'l1 Bprime 20/41')
require(l1prob(B)==F(100,247),'l1 B 100/247')
require(l1prob(B)!=l1prob(Bp),'l1 shared-ray context dependence')
C=((F(3,5),F(4,5),F(0)),(F(-4,5),F(3,5),F(0)),E[2])
require(basis(C),'quartic rational orthonormal witness')
require(sum(x[0]**4 for x in E)==1,'quartic coordinate total 1')
require(sum(x[0]**4 for x in C)==F(337,625),'quartic rotated total 337/625')
require(sum(x[0]**4 for x in E)!=sum(x[0]**4 for x in C),'quartic violates constant trace totals')
def ce1(n):return (1+n[2]**3)/2
nx=(F(1),F(0),F(0));ny=(F(0),F(1),F(0));nz=(F(0),F(0),F(1));n=(F(4,5),F(0),F(3,5))
for i,k in enumerate([nx,ny,nz,n]):
    require(dot(k,k)==1,'CE1 unit Bloch fixture '+str(i))
    require(ce1(k)+ce1(scale(F(-1),k))==1,'CE1 antipodal sum fixture '+str(i))
    require(0<=ce1(k)<=1,'CE1 nonnegative fixture '+str(i))
require([ce1(nx),ce1(ny),ce1(nz)]==[F(1,2),F(1,2),F(1)],'CE1 axes force Bloch candidate')
require(ce1(n)==F(76,125),'CE1 tilted value 76/125')
require((1+n[2])/2==F(4,5)!=ce1(n),'CE1 exact Bloch contradiction')
x=(F(3,5),F(4,5));xm=(F(-3,5),F(4,5))
def realce(x):return (1+(x[0]**2-x[1]**2)**3)/2
require(realce(x)==realce(xm),'real d2 even coordinate signs')
require(realce(x)!=x[0]**2,'real d2 not forced diagonal form')
b1=(realce(x)-x[0]**2)/(2*x[0]*x[1]);b2=(realce(xm)-xm[0]**2)/(2*xm[0]*xm[1])
require(b1!=b2,'real d2 inconsistent off-diagonal coefficients')
r0=diag([F(1,3)]*3);r1=diag([F(1,3)]*3);r1[0][1]=r1[1][0]=F(1,6)
require([quad(r0,e) for e in E]==[quad(r1,e) for e in E]==[F(1,3)]*3,'classical context sees same diagonal trace values')
require(F(1,3)+F(1,6)>0 and F(1,3)-F(1,6)>0,'perturbed real density positive block eigenvalues')
require(quad(r0,C[0])!=quad(r1,C[0]),'rotated context distinguishes density completions')
pure=diag([1,0,0])
require(quad(pure,E[0])==1!=quad(r0,E[0]),'different valid states give different assignments')
for i,rho in enumerate([r0,r1,pure]):
    for j,frame in enumerate([E,C,B,Bp]):
        require(sum(quad(rho,e) for e in frame)==1,'trace dictionary fixture '+str(i)+':'+str(j))
for k in [2,3]:
    require(sum([F(1,k)]*k)==1,'indexed repeated I/k normalizes '+str(k))
    require(sum(set([F(1,k)]*k))!=1,'set collapse loses multiplicity '+str(k))
guards=[('quartic normalized',sum(x[0]**4 for x in C)==1),('shared winner unchanged',p[0]<p[1]),('l1 shared probability equal',l1prob(B)==l1prob(Bp)),('CE1 fitted tilted value',ce1(n)==F(4,5)),('classical data lack trace form',quad(pure,E[0])!=1),('duplicate effects counted once',sum(set([F(1,2)]*2))==1)]
for name,value in guards:
    if value:raise RuntimeError('false claim survived: '+name)
print(json.dumps({'scope':'Bounded exact rational witnesses and trace dictionary. No universal axiom validation, least-squares fit, Hamel sampler or Gleason proof.','checks_passed':len(checks),'checks':checks,'false_claim_guards':[{'name':name,'status':'REJECTED'} for name,value in guards],'CE4':'PROOF_ONLY_NOT_EXECUTED','D1_D3':'OPEN'},indent=2))
