"""Exact local controls for the MUB atlas review. No dimension-six atlas is computed."""
from pathlib import Path
import sympy as s
from fractions import Fraction as Q
from itertools import product
import json,sys
checks=[]
def eq(a,b):
    d=a-b
    if isinstance(d,s.MatrixBase):return all(s.simplify(s.expand_complex(z))==0 for z in d)
    return s.simplify(d)==0
def check(name,cond):
    if cond is not True:raise RuntimeError('FAIL '+name+': '+str(cond))
    checks.append(name);print('PASS '+name)
def norms(M):return M.applyfunc(lambda z:s.simplify(s.expand_complex(z*s.conjugate(z))))
def flat(M,n):return all(eq(z,s.Rational(1,n)) for z in norms(M))
H=s.Matrix([[1,1],[1,-1]]);D=s.diag(1,s.I)
U=H/s.sqrt(2);V=D*H/s.sqrt(2)
check('transpose d2 original unitaries',eq(U.H*U,s.eye(2)) and eq(V.H*V,s.eye(2)))
check('transpose d2 original flat',flat(U,2) and flat(V,2))
check('transpose d2 original pair MU',flat(U.H*V,2))
check('transpose d2 loses pair MU',not flat(s.conjugate(U)*V.T,2))
check('transpose d2 cross becomes diagonal',eq(s.conjugate(U)*V.T,D))
z=-s.Rational(1,2)+s.sqrt(3)*s.I/2
F=s.Matrix(3,3,lambda j,k:s.expand_complex(z**(j*k)))
G=s.diag(1,z,z)*F
A=s.kronecker_product(H,F);B=s.kronecker_product(D*H,G)
check('transpose d6 A Gram exact',eq(A.H*A,6*s.eye(6)))
check('transpose d6 B Gram exact',eq(B.H*B,6*s.eye(6)))
check('transpose d6 entries all phase',all(eq(v,1) for v in norms(A)) and all(eq(v,1) for v in norms(B)))
C=A.H*B
check('transpose d6 original pair MU',all(eq(v,6) for v in norms(C)))
CT=s.conjugate(A)*B.T
check('transpose d6 pair MU destroyed',not all(eq(v,6) for v in norms(CT)))
check('transpose d6 has exact zero overlap',eq(CT[0,3],0))
# Valid coupled transposition on a triple of bases (I,U,V), with U,V flat MU.
UT=U.T;VT=U.T*s.conjugate(V)
check('coupled rebase transpose preserves flatness',flat(UT,2) and flat(VT,2))
check('coupled rebase transpose preserves MU',flat(UT.H*VT,2))
check('dephased ambient phase count',36-(6+6-1)==25)
# Exact interval arithmetic constants: rational upper bound for both bridges in turns.
check('sqrt6 lower bound used for radius',2**2<6)
check('turn Lipschitz rational bound',Q(220,7)<32)
check('original weak E radian constant simplifies to ten',eq(2*s.sqrt(6)*s.sqrt(s.Rational(25,6)),10))
check('original weak E radius gives eta over ten',eq(1/(2*s.sqrt(6)*s.sqrt(s.Rational(25,6))),s.Rational(1,10)))
check('sharper entrywise E radius matches proposed radius',eq(1/(2*s.sqrt(s.Rational(25,6))),s.sqrt(6)/10))
# Threshold logical control in a singleton compact min-max model; not a MUB counterexample.
delta=Q(1,4);a,b,c=delta,Q(0),Q(0)
check('closed open threshold mix fails in scalar model',max(a,b,c)>=delta and a<=delta and b<=delta and c<delta)
check('all strict threshold equivalence scalar model',not(a<delta and b<delta and c<delta))
# A Hadamard's own column is not unbiased to that same Hadamard.
v=U[:,0]
check('own column is unbiased to standard basis',flat(v,2))
check('own column fails own basis unbiasedness',not flat(U.H*v,2))
F6=s.kronecker_product(H,F)/s.sqrt(6)
v6=F6[:,0]
check('own d6 column not S0 witness',eq(F6.H*v6,s.eye(6)[:,0]) and not flat(F6.H*v6,6))
# Nonunitarity margin at an exact nonunitary flat center; no D value is claimed.
R=s.ones(6)/s.sqrt(6);E=R.H*R-s.eye(6)
check('nonunitary center exact E one',all(eq(E[j,k],0 if j==k else 1) for j in range(6) for k in range(6)))
# Finite cover checker below is only a small-dimensional control for coverage semantics.
def covers(boxes,dimension):
    if not isinstance(dimension,int) or isinstance(dimension,bool) or dimension<1:raise ValueError('positive dimension required')
    for box in boxes:
        if len(box)!=dimension:raise ValueError('dimension mismatch')
        for lo,hi in box:
            if not isinstance(lo,Q) or not isinstance(hi,Q):raise ValueError('rational endpoints required')
            if not(0<=lo<=hi<=1):raise ValueError('invalid endpoint order')
    axes=[]
    for d in range(dimension):
        endpoints=sorted({Q(0),Q(1)}|{q for box in boxes for q in box[d]})
        axes.append(endpoints+[(a+b)/2 for a,b in zip(endpoints,endpoints[1:])])
    for point in product(*axes):
        if not any(all(lo<=x<=hi for x,(lo,hi) in zip(point,box)) for box in boxes):return False
    return True
half=Q(1,2);zero=Q(0);one=Q(1)
intervals=[(zero,half),(half,one)]
boxes=[(x,y) for x in intervals for y in intervals]
check('coverage exact square quadrants',covers(boxes,2))
check('coverage missing quadrant refused',not covers(boxes[:-1],2))
check('coverage empty refused',not covers([],1))
check('coverage seam covered',covers([((zero,half),),((half,one),)],1))
check('coverage small rational hole detected',not covers([((zero,half),),((half+Q(1,1000000),one),)],1))
def admit_margin(lower,radius):
    if not isinstance(lower,Q) or not isinstance(radius,Q):raise ValueError('rational proof data required')
    if lower<=0 or radius<0:raise ValueError('positive margin and nonnegative radius required')
    return lower-32*radius>0
check('strict bridge valid margin',admit_margin(Q(1,4),Q(1,256)))
check('strict bridge zero remaining margin refused',not admit_margin(Q(1,4),Q(1,128)))
check('strict bridge negative remaining margin refused',not admit_margin(Q(1,4),Q(1,100)))
refused=[]
for name,fn in [
 ('Boolean dimension',lambda:covers(boxes,True)),
 ('wrong box dimension',lambda:covers(boxes,1)),
 ('float corner',lambda:covers([((0.0,one),)],1)),
 ('reversed interval',lambda:covers([((one,zero),)],1)),
 ('float margin',lambda:admit_margin(0.25,Q(1,256))),
 ('negative radius',lambda:admit_margin(Q(1,4),Q(-1,256)))]:
    try:fn()
    except ValueError:refused.append(name);print('REFUSED '+name)
    else:raise RuntimeError('Missing invalid input refusal '+name)
result={'python':sys.version,'sympy':s.__version__,'optimized':not __debug__,'passed':len(checks),'checks':checks,'invalid_inputs_refused':refused,'scope':'Exact transpose countermodels, bridge coefficient arithmetic, scalar threshold logic, and toy rational coverage controls. No evaluation/lower bound of D, no dimension-six atlas, no global MUB bound, no Lean certificate.'}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('RESULT '+json.dumps({'passed':len(checks),'refused':len(refused),'optimized':not __debug__}))
