"""Exact scoped controls for GPT reconstruction review; no reconstruction certificate."""
import sympy as s
from pathlib import Path
import sys,json
checks=[]
def eq(a,b):
    d=a-b
    if isinstance(d,s.MatrixBase):return all(s.simplify(z)==0 for z in d)
    return s.simplify(d)==0
def check(name,condition):
    if condition is not True:raise RuntimeError('FAIL '+name+': '+str(condition))
    checks.append(name);print('PASS '+name)
def E(n,j,k):
    M=s.zeros(n);M[j,k]=1;return M
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
vec=s.Matrix([1,0,0,1]);bell=vec*vec.H/2
pt=s.Matrix(4,4,lambda j,k:bell[(j//2)*2+k%2,(k//2)*2+j%2])
check('Bell normalized',eq(s.trace(bell),1))
check('Bell positive pure',eq(bell*bell,bell) and eq(bell,bell.H))
check('partial transpose eigenvalues exact',pt.eigenvals()=={-s.Rational(1,2):1,s.Rational(1,2):3})
anti=s.Matrix([0,1,-1,0])
check('partial transpose negative quadratic form',eq((anti.H*pt*anti)[0],-1))
check('partial transpose preserves trace but fails positivity',eq(s.trace(pt),1) and (anti.H*pt*anti)[0]<0)
rho=(I+Y)/2
check('single-qubit transpose stays a pure state',eq(rho.T*rho.T,rho.T) and eq(s.trace(rho.T),1))
check('single transpose is involutive',eq(rho.T.T,rho))
check('single transpose flips Y',eq(rho.T,(I-Y)/2))
# Dimension diagnostics; these are not tensor-cone classification proofs.
n,m=s.symbols('n m',integer=True,positive=True)
KR=lambda n:n*(n+1)/2;KC=lambda n:n*n;KH=lambda n:n*(2*n-1)
check('complex matrix dimensions multiply',eq(KC(n*m),KC(n)*KC(m)))
check('classical dimensions also multiply',eq(n*m,n*m))
check('real dimension defect identity',eq(KR(n*m)-KR(n)*KR(m),n*m*(n-1)*(m-1)/4))
check('quaternionic dimension defect identity',eq(KH(n*m)-KH(n)*KH(m),-2*n*m*(n-1)*(m-1)))
check('two rebits fail standard local tomography',KR(4)==10 and KR(2)**2==9)
check('two quaternionic bits dimension mismatch',KH(4)==28 and KH(2)**2==36)
check('dimension-only spin-factor candidate passes counts',7*4==KH(4) and 2*2==4)
q=s.symbols('q',integer=True,nonnegative=True);c=q+2
check('classical-qubit simple-real excess factor',eq(KR(2*c)-4*c,c*(2*c-3)) and (c*(2*c-3)).is_positive is True)
check('classical-qubit simple-complex excess factor',eq(KC(2*c)-4*c,4*c*(c-1)) and (4*c*(c-1)).is_positive is True)
check('classical-qubit simple-quaternionic excess factor',eq(KH(2*c)-4*c,2*c*(4*c-3)) and (2*c*(4*c-3)).is_positive is True)
# Concrete finite witnesses for the general powers-of-two theory argument in the notes.
def power_two(k):
    if not isinstance(k,int) or isinstance(k,bool) or k<0:raise ValueError('nonnegative integer exponent required')
    return 2**k
for j in range(4):
    for k in range(4):check('powers-of-two object tensor closure '+str(j)+','+str(k),power_two(j)*power_two(k)==power_two(j+k))
check('qutrit dimension cannot be qubit or unit dimension',3 not in [1,2,4] and 3%2==1)
check('qutrit affine dimension differs from unit and qubit',3**2-1==8 and 8 not in [1**2-1,2**2-1])
# All qubit local statistics span composite Hermitian matrices in standard complex QM.
paulis=[I,X,Y,Z]
products=[s.kronecker_product(a,b) for a in paulis for b in paulis]
check('local quantum product operator basis rank sixteen',s.Matrix.hstack(*[p.reshape(16,1) for p in products]).rank()==16)
check('quantum K differs from normalized affine dimension',len(paulis)==4 and len(paulis)-1==3)
# Hanche-Olsen compatibility identities in the actual standard matrix tensor product.
def jordan(a,b):return (a*b+b*a)/2
A=I+X;B=I+Y;v=X+Z;w=I+Y
check('HO first unit-leg compatibility',eq(jordan(s.kronecker_product(A,I),s.kronecker_product(B,v)),s.kronecker_product(jordan(A,B),v)))
check('HO second unit-leg compatibility',eq(jordan(s.kronecker_product(I,v),s.kronecker_product(A,w)),s.kronecker_product(A,jordan(v,w))))
check('Jordan product is not naive factorwise tensor',not eq(jordan(s.kronecker_product(X,X),s.kronecker_product(Z,Z)),s.kronecker_product(jordan(X,Z),jordan(X,Z))))
check('correct nonfactorwise product value',eq(jordan(s.kronecker_product(X,X),s.kronecker_product(Z,Z)),-s.kronecker_product(Y,Y)))
# A POVM fixes probabilities but does not fix the associated state update.
P0=E(2,0,0);P1=E(2,1,1);K=E(2,0,1)
check('two instruments same outcome-zero effect',eq(P0.H*P0,P0))
check('two instruments same outcome-one effect',eq(K.H*K,P1.H*P1))
check('both instruments normalized',eq(P0.H*P0+K.H*K,I) and eq(P0.H*P0+P1.H*P1,I))
check('same probability on outcome one',eq(s.trace(P1*P1*P1),s.trace(K*P1*K.H)))
check('different postmeasurement state on outcome one',eq(P1*P1*P1,P1) and eq(K*P1*K.H,P0) and P0!=P1)
# Ordered-frame transitivity is more than permuting one fixed measurement.
H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);plus=H*P0*H.H
check('frame change gives distinct measurement',plus!=P0 and plus!=P1)
check('Hadamard transports frame',eq(H*P1*H.H,I-plus))
# Born probabilities once the complex matrix state/effect representation is supplied.
state=(I+Y)/2;effect=(I+X/2+Y/2)/2
check('effect within unit interval',all(z>=0 for z in effect.eigenvals()) and all(z>=0 for z in (I-effect).eigenvals()))
check('trace pairing exact probability',eq(s.trace(effect*state),s.Rational(3,4)))
refused=[]
for name,value in [('Boolean exponent',True),('negative exponent',-1),('floating exponent',1.0)]:
    try:power_two(value)
    except ValueError:refused.append(name);print('REFUSED '+name)
    else:raise RuntimeError('Expected input refusal '+name)
result={'python':sys.version,'sympy':s.__version__,'optimized':not __debug__,'passed':len(checks),'checks':checks,'invalid_inputs_refused':refused,'scope':'Finite exact matrix controls and dimension identities. General qubit-only countertheory proved in written note, not by finite exponent samples. No proof of A0-A4 sufficiency or kernel-checked reconstruction.'}
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('RESULT '+json.dumps({'passed':len(checks),'refused':len(refused),'optimized':not __debug__}))
