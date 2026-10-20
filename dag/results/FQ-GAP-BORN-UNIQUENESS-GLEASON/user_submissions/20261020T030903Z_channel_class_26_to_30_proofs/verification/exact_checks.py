"""Exact finite controls for CC-26:30 prose corrections; no theorem certification."""
import json,sys
import sympy as s
from pathlib import Path
I=s.I; R=s.Rational
checks=[]
def clean(x):return x.applyfunc(s.simplify) if isinstance(x,s.MatrixBase) else s.simplify(x)
def eq(a,b):return clean(a-b)==(s.zeros(a.rows,a.cols) if isinstance(a,s.MatrixBase) else 0)
def check(name,condition):
    if condition is not True:raise RuntimeError('FAIL '+name+': '+str(condition))
    checks.append(name);print('PASS '+name)
def E(n,j,k):
    x=s.zeros(n);x[j,k]=1;return x
def delta(x):return s.diag(*x.diagonal())
def ad(u,x):return clean(u*x*u.H)
def shadow(u):return s.Matrix(u.rows,u.cols,lambda j,k:clean(u[j,k]*s.conjugate(u[j,k])))
def in_qi(x):return all(s.re(z).is_Rational is True and s.im(z).is_Rational is True for z in x)
def same_norm_update(a,b):
    if a.shape!=b.shape or a.cols!=1:raise ValueError('column shapes required')
    if not eq((a.H*a)[0],(b.H*b)[0]):raise ValueError('equal norm required')
    if eq(a,b):return s.eye(a.rows)
    w=a-b;c=clean((w.H*a)[0])
    if c==0:raise ValueError('unexpected zero denominator')
    return clean(s.eye(a.rows)-w*w.H/c)
def equal_gram(A,B):
    if A.shape!=B.shape:raise ValueError('pad to same shape first')
    if not eq(A*A.H,B*B.H):raise ValueError('equal Gram required')
    T=s.eye(A.cols)
    for j in range(A.rows):
        a=clean(T*A[j,:].H);b=B[j,:].H
        T=clean(same_norm_update(a,b)*T)
    return T.H

e0=s.Matrix([1,0]);e1=s.Matrix([0,1]);pplus=(e0+e1)*(e0+e1).H/2
pminus=(e0-I*e1)*(e0-I*e1).H/2
check('CC26 imaginary probe outside Q',any(z.is_Rational is not True for z in pminus))
check('CC26 imaginary probe inside Qi',in_qi(pminus))
check('CC26 real probes span dimension three',s.Matrix.hstack(*[x.reshape(4,1) for x in [E(2,0,0),E(2,1,1),pplus]]).rank()==3)
check('CC26 complex probes span dimension four',s.Matrix.hstack(*[x.reshape(4,1) for x in [E(2,0,0),E(2,1,1),pplus,pminus]]).rank()==4)
Y=s.Matrix([[0,-I],[I,0]]);AQ=s.eye(2)+Y/2
for label,p in [('D0',E(2,0,0)),('D1',E(2,1,1)),('plus',pplus)]:check('CC26 missing-imaginary query passes '+label,eq(s.trace(AQ*p),1))
check('CC26 omitted imaginary query fails',not eq(s.trace(AQ*pminus),1))
check('CC26 positive nonidentity effect',eq(AQ,AQ.H) and sorted(AQ.eigenvals().keys())==[R(1,2),R(3,2)])
AR=s.Matrix([[1,R(1,2)],[R(1,2),1]])
check('CC26 real missing-plus countermodel',eq(AR[0,0],1) and eq(AR[1,1],1) and not eq(s.trace(AR*pplus),1))
check('CC26 real countermodel positive',sorted(AR.eigenvals().keys())==[R(1,2),R(3,2)])
U=s.Matrix([[3,4],[-4,3]])/5;V=s.Matrix([[3,4*I],[4*I,3]])/5
check('CC27 U unitary',eq(U.H*U,s.eye(2)))
check('CC27 V unitary',eq(V.H*V,s.eye(2)))
x01=delta(ad(V,E(2,0,1)));x10=delta(ad(V,E(2,1,0)))
check('CC27 nonzero detected coherence',eq(x01,s.diag(-12*I,12*I)/25) and x01!=s.zeros(2))
check('CC27 detected coherences cancel',eq(x01,-x10))
for j in range(2):
    x=ad(U,E(2,j,j));off=x-delta(x)
    check('CC27 source coherence present '+str(j),off!=s.zeros(2))
    check('CC27 Omega zero by cancellation '+str(j),eq(delta(ad(V,off)),s.zeros(2)))
check('CC27 shadows compose despite termwise detection',eq(shadow(V*U),shadow(V)*shadow(U)))
check('CC27 composed exact value',eq(shadow(V*U),s.Matrix([[337,288],[288,337]])/625))
B=s.diag(s.ones(1),U);value=delta(ad(B,E(3,1,2)))
check('CC27 corrected three-cell diagonal',eq(value,s.diag(0,12,-12)/25))
check('CC27 three-cell trace zero',eq(s.trace(value),0))
check('CC27 submitted three-cell value false',not eq(value,R(12,25)*E(3,1,1)))
A3=s.diag(U,s.ones(1))
check('CC27 support success survives correction',eq(shadow(B*A3),shadow(B)*shadow(A3)))

K=[E(2,0,0),E(2,0,1)]
def reset(x):return sum([k*x*k.H for k in K],s.zeros(2))
def dual(x):return sum([k.H*x*k for k in K],s.zeros(2))
check('CC29 reset normalized',eq(sum([k.H*k for k in K],s.zeros(2)),s.eye(2)))
check('CC29 adjoint unital',eq(dual(s.eye(2)),s.eye(2)))
check('CC29 adjoint not TP exact trace two',eq(s.trace(dual(E(2,0,0))),2))
lam=s.sqrt(2)/2
mixed=clean(lam*E(2,0,1)+(1-lam)*delta(E(2,0,1)))
check('CC26 arbitrary-real mixing leaves carrier',not in_qi(mixed) and eq(mixed[0,1],lam))
check('CC28 dephasing not ambient identity',delta(E(2,0,1))!=E(2,0,1))
check('CC28 dephasing is idempotent',eq(delta(delta(pplus)),delta(pplus)))
S=s.ones(1,3);X=s.Matrix([[1,I,2],[3,4,5],[6,7,8]])
check('CC28 scalar stochastic output is trace',eq((S*s.Matrix(X.diagonal()).T)[0],s.trace(X)))

for label,a,b in [
 ('nonunit real',s.Matrix([1,1]),s.Matrix([1,-1])),
 ('complex',s.Matrix([1,I,2]),s.Matrix([I,1,-2])),
 ('zero',s.zeros(2,1),s.zeros(2,1)),
 ('same',s.Matrix([1,I]),s.Matrix([1,I]))]:
    T=same_norm_update(a,b)
    check('GRAM '+label+' unitary',eq(T.H*T,s.eye(T.rows)))
    check('GRAM '+label+' maps vector',eq(T*a,b))
    check('GRAM '+label+' carrier',in_qi(T))
a=s.Matrix([1,1,1]);b=s.Matrix([1,1,-1]);T=same_norm_update(a,b);fixed=s.Matrix([1,0,0])
check('GRAM update fixes previous match',eq(T*fixed,fixed))
fixtures=[]
va=s.Matrix([1,0,0,1]);AA=s.Matrix.hstack(va,s.zeros(4,1));BB=s.Matrix.hstack(R(3,5)*va,R(4,5)*va)
fixtures.append(('padded Kraus',AA,BB))
AA=s.Matrix([[1,1],[1,-1],[0,0],[2,2]])
fixtures.append(('dependent nonorthonormal',AA,AA*s.diag(1,I)))
AA=s.Matrix([[1,I,2],[2,0,1],[0,0,0],[1,I,2]])
W=s.diag(U,s.ones(1))*s.diag(I,1,1)
fixtures.append(('rectangular complex',AA,AA*W))
fixtures.append(('empty Kraus',s.zeros(3,0),s.zeros(3,0)))
for label,AA,BB in fixtures:
    W=equal_gram(AA,BB)
    check('GRAM '+label+' equal input Gram',eq(AA*AA.H,BB*BB.H))
    check('GRAM '+label+' unitary',eq(W.H*W,s.eye(W.rows)))
    check('GRAM '+label+' reconstructs',eq(AA*W,BB))
    check('GRAM '+label+' carrier',in_qi(W))

refused=[]
for name,f in [
 ('unequal norms',lambda:same_norm_update(s.Matrix([1,0]),s.Matrix([2,0]))),
 ('unequal Gram',lambda:equal_gram(s.eye(2),2*s.eye(2))),
 ('unpadded shape',lambda:equal_gram(s.zeros(2,1),s.zeros(2,2))),
 ('noncolumn',lambda:same_norm_update(s.eye(2),s.eye(2)))]:
    try:f()
    except ValueError:refused.append(name);print('REFUSED '+name)
    else:raise RuntimeError('Expected invalid input refusal '+name)
result={'python':sys.version,'sympy':s.__version__,'optimized':not __debug__,'passed':len(checks),'checks':checks,'invalid_inputs_refused':refused,'scope':'Finite exact controls plus executable equal-Gram construction. No general theorem kernel certificate. Irrational coefficient appears only as an intentional carrier-rejection fixture.'}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('RESULT '+json.dumps({'passed':len(checks),'refused':len(refused),'optimized':not __debug__}))
