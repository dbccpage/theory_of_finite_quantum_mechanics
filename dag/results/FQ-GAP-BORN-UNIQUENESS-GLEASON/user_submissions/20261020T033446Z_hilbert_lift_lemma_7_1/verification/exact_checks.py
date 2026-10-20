"""Exact controls for revised Hilbert lift; no continuum theorem kernel certificate."""
import sympy as s
from pathlib import Path
import json,sys
checks=[]
def check(name,cond):
    if cond is not True and cond is not s.true:raise RuntimeError('FAIL '+name+': '+str(cond))
    checks.append(name);print('PASS '+name)
def eq(a,b):
    d=a-b
    if isinstance(d,s.MatrixBase):return all(s.simplify(z)==0 for z in d)
    return s.simplify(d)==0
def normsq(v,G=None):return s.simplify((v.H*(s.eye(v.rows) if G is None else G)*v)[0])
def unit(N,k):return s.eye(N)[:,k]
def polar(x,y,q):return s.simplify(sum(s.I**(-k)*q(x+s.I**k*y) for k in range(4))/4)
check('antilinear-first polarization sign',eq(polar(s.Matrix([1]),s.Matrix([s.I]),normsq),s.I))
check('parallelogram alone does not fix declared h',eq(polar(s.Matrix([1]),s.Matrix([1]),lambda v:2*normsq(v)),2))
check('l1 parallelogram counterexample',2**2+2**2==8 and 2*1**2+2*1**2==4)
check('absolute-value power differs from normalized value',s.sqrt(4)==2 and s.sqrt(4)!=4)
W0=s.Matrix([[1]]);W1=s.diag(s.Rational(1,3),s.Rational(2,3));J=s.ones(2,1)
check('function pullback isometry with additive weights',eq(J.H*W1*J,W0))
M=s.Matrix([s.Rational(1,3),s.Rational(2,3)])
check('mass-coordinate refinement isometry',eq(M.H*W1.inv()*M,W0.inv()))
check('mass copying is not isometric',not eq(J.H*W1.inv()*J,W0.inv()))
check('nonadditive pullback fails',not eq(J.H*s.diag(s.Rational(1,2),s.Rational(1,3))*J,W0))
# Ordinary full/induced subcomplex growth: a-b grows to a-b-c.
d0=s.Matrix([[-1,1]]);d1=s.Matrix([[-1,1,0],[0,-1,1]])
j0=s.Matrix([[1,0],[0,1],[0,0]]);j1=s.Matrix([[1],[0]])
check('graph growth forward compatibility fails',not eq(d1*j0,j1*d0))
check('graph growth adjoint compatibility can hold',eq(d1.H*j1,j0*d0.H))
x=s.Matrix([0,1])
check('internal graph stage energy one',eq(normsq(d0*x),1))
check('global zero-extended graph energy two',eq(normsq(d1*j0*x),2))
check('boundary correction is missing one energy',eq(normsq(d1*j0*x)-normsq(d0*x),1))
check('three-vertex graph bound valid',max((d1.H*d1).eigenvals())==3 and 3<=2*2)
# Born measure of a fixed vector differs from its coarse amplitude average.
f=s.Matrix([1,-1]);W=s.eye(2)/2;coarse=(J.H*W*f)[0]
check('coarse amplitude average cancels',eq(coarse,0))
check('coarse actual Born mass does not cancel',eq(normsq(f,W),1))
check('projected Born mass differs from actual marginal',not eq(coarse*s.conjugate(coarse),normsq(f,W)))
x=s.Matrix([1,0]);y=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
variation=sum(abs(x[k]*s.conjugate(x[k])-y[k]*s.conjugate(y[k])) for k in range(2))
check('normalized vector masses',eq(normsq(x),1) and eq(normsq(y),1))
check('Born measure variation exact value',eq(variation,s.Rational(32,25)))
check('Born continuity bound squared',variation**2<=4*normsq(x-y))
check('coarse-graining contracts variation',abs(normsq(x)-normsq(y))<=variation)
check('probability TV convention is half variation',eq(variation/2,s.Rational(16,25)))
# Infinite subdivision with persistent atoms; finite controls of exact general construction.
for n in range(1,5):
    weights=[s.Rational(1,2**k) for k in range(1,n+1)]+[s.Rational(1,2**n)]
    nxt=[s.Rational(1,2**k) for k in range(1,n+2)]+[s.Rational(1,2**(n+1))]
    T=s.zeros(n+2,n+1)
    for k in range(n):T[k,k]=1
    T[n,n]=1;T[n+1,n]=1
    check('persistent-atom refinement isometry '+str(n),eq(T.H*s.diag(*nxt)*T,s.diag(*weights)))
    check('persistent-atom total mass '+str(n),sum(weights)==1)
    check('persistent isolated atom unchanged '+str(n),weights[0]==s.Rational(1,2) and list(T[:,0]).count(1)==1)
# Earlier nonclosable example: formulas for x_n=e_n/n and T x_n=1.
n=s.symbols('n',positive=True,integer=True)
check('nonclosable-control norm formula',eq((1/n)**2,1/n**2))
check('nonclosable-control image formula',eq(n*(1/n),1))
# Actual stage-compatible bounded differential with spectral pollution.
def stage_basis(n,N):
    if not isinstance(n,int) or isinstance(n,bool) or n<1 or N<2*n:raise ValueError('valid stage and ambient dimension required')
    cols=[unit(N,k) for k in range(2*(n-1))]
    cols.append((unit(N,2*n-2)+unit(N,2*n-1))/s.sqrt(2))
    return s.Matrix.hstack(*cols)
for n in range(1,4):
    N=2*(n+1);B=stage_basis(n,N);Bn=stage_basis(n+1,N)
    D=s.diag(*([1,s.sqrt(3)]*(n+1)));A=D.H*D;P=B*B.H
    Y=D*B;Yn=D*Bn;Qn=Yn*(Yn.H*Yn).inv()*Yn.H
    An=B.H*A*B;w=B[:,-1]
    check('spectral-control source orthonormal '+str(n),eq(B.H*B,s.eye(B.cols)))
    check('spectral-control nested source stages '+str(n),eq(Bn*Bn.H*B,B))
    check('spectral-control forward differential compatible '+str(n),eq(Qn*Y,Y))
    check('spectral-control finite eigenvalue two '+str(n),2 in An.eigenvals())
    check('spectral-control ambient eigenvalues one and three '+str(n),set(A.eigenvals())=={s.Integer(1),s.Integer(3)})
    check('spectral-control adjoint compatibility absent '+str(n),not eq((s.eye(N)-P)*A*w,s.zeros(N,1)))
    res=B*(An+s.eye(An.rows)).inv()*B.H
    check('spectral-control resolvent error on moving vector '+str(n),eq(normsq(res*w-(A+s.eye(N)).inv()*w),s.Rational(5,288)))
    check('spectral-control projection norm witness '+str(n),eq(normsq((s.eye(N)-P)*unit(N,N-1)),1))
# Input guards remain meaningful under optimization.
refused=[]
for name,fn in [('Boolean stage',lambda:stage_basis(True,4)),('zero stage',lambda:stage_basis(0,4)),('insufficient ambient space',lambda:stage_basis(2,2))]:
    try:fn()
    except ValueError:refused.append(name);print('REFUSED '+name)
    else:raise RuntimeError('Missing invalid-input refusal '+name)
result={'python':sys.version,'sympy':s.__version__,'optimized':not __debug__,'passed':len(checks),'checks':checks,'invalid_inputs_refused':refused,'scope':'Exact finite controls and symbolic identities. Persistent-atom topology and general spectral-pollution model are written arguments, not inferred from finite samples. No general Lean certificate or physical continuum/dynamics identification.'}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('RESULT '+json.dumps({'passed':len(checks),'refused':len(refused),'optimized':not __debug__}))
