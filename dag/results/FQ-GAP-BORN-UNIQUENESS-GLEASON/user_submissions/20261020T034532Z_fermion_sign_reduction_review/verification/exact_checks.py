"""Exact finite sign controls. No Monte Carlo, floating fits or general Lean claims."""
from fractions import Fraction as F
from itertools import product
import json
import sys
import sympy as S

checks=[]
refusals=[]
def require(condition):
    if condition is not True and condition is not S.true:
        raise ValueError('condition was not a certified true Boolean')
def check(name, condition):
    require(condition)
    if name in checks: raise ValueError('duplicate check')
    checks.append(name)
def refuse(name, thunk):
    try: thunk()
    except ValueError:
        refusals.append(name)
        return
    raise RuntimeError('expected refusal missing: '+name)
def decode(w,n):
    if w == 0:
        if any(x != 0 for x in n):
            raise ValueError('zero-weight block carries nonzero numerator')
        return tuple(0 for _ in n)
    return tuple(x/w for x in n)
def phase(weights):
    z=sum(weights); a=sum(abs(x) for x in weights)
    if not (z > 0 and a > 0): raise ValueError('positive partition and absolute norm required')
    return z/a

def push(vectors, groups):
    return [tuple(sum(vectors[i][j] for i in group) for j in range(len(vectors[0]))) for group in groups]

refuse('guard_rejects_false',lambda:require(False))
refuse('guard_rejects_unknown',lambda:require(None))
refuse('zero_block_nonzero_insertion',lambda:decode(F(0),(F(1),)))
refuse('zero_partition_refused',lambda:phase([F(1),F(-1)]))
refuse('negative_partition_refused',lambda:phase([F(-1)]))
for k in range(1,7):
    n=k*k; d=F(1,2**k); w=[(1+d)/2,-(1-d)/2]
    check(f'rate_{k}_finite_phase',phase(w)==d)
    check(f'rate_{k}_exact_absolute_norm',sum(abs(x) for x in w)==1)
    check(f'rate_{k}_overhead',d**(-2)==4**k)
    scaled=[F(2**n,1)/d*x for x in w]
    check(f'rate_{k}_fermionic_H0_partition',sum(scaled)==2**n)
    check(f'rate_{k}_normalized_log_rate',F(k,n)==F(1,k))

for n in [1,2,4,8,16]:
    q=[F(1,2**n),1-F(1,2**n)]; f=[2**n,0]
    mean=sum(p*x for p,x in zip(q,f))
    var=sum(p*(x-mean)**2 for p,x in zip(q,f))
    check(f'rare_{n}_mean',mean==1)
    check(f'rare_{n}_variance',var==2**n-1)
    check(f'rare_{n}_phase',phase(q)==1)
    d=F(1,2**n); qp=[(1+d)/2,(1-d)/2]; s=[1,-1]
    check(f'phase_{n}_denominator_variance',sum(p*(x-d)**2 for p,x in zip(qp,s))==1-d*d)
    check(f'identity_{n}_residual_zero',sum(p*(x*(1-1))**2 for p,x in zip(qp,s))==0)

for sample in product([F(-1),F(1)],repeat=3):
    den=sum(sample)
    check('identity_ratio_'+''.join('p' if x>0 else 'm' for x in sample),sum(x*1 for x in sample)/den==1)

check('complex_equal_factors_can_be_negative',S.I*S.I==-1)
z=3+2*S.I
check('conjugate_factors_nonnegative',S.expand(z*S.conjugate(z))==13)
a=-2+S.I;b=3+2*S.I
B=S.Matrix([[a,b],[-S.conjugate(b),S.conjugate(a)]])
J=S.Matrix([[0,1],[-1,0]]);I=S.eye(2)
check('kramers_T_square_minus_identity',J*J.conjugate()==-I)
check('kramers_antiunitary_commutation',J*B.conjugate()==B*J)
check('kramers_fixture_nonhermitian',B!=B.conjugate().T)
check('kramers_fixture_positive_det',S.expand((I+B).det())==15)
check('kramers_zero_case',(I+(-I)).det()==0)
C=S.diag(-2,0)
check('real_matrix_not_enough',(I+C).det()==-1)

# H=0 on one fermionic mode: Z=2 and number expectation 1/2.
for t in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
    w=[4*t-2,4-4*t]
    name=str(t).replace('/','_')
    check('continuous_'+name+'_partition',sum(w)==2)
    check('continuous_'+name+'_number',sum(x*F(1,2) for x in w)/sum(w)==F(1,2))
check('continuous_before_phase',phase([F(-2),F(4)])==F(1,3))
check('continuous_after_phase',phase([F(0),F(2)])==1)
check('negative_observable_not_sign_problem',sum(F(1,2)*(-1) for _ in range(2))==-1)

v=[(F(1),F(1)),(F(-1),F(0)),(F(1),F(0))]
p=push(v,[[0,1],[2]])
check('blocking_partition_preserved',sum(x[0] for x in p)==sum(x[0] for x in v)==1)
check('blocking_numerator_preserved',sum(x[1] for x in p)==sum(x[1] for x in v)==1)
check('zero_block_has_information',p[0]==(0,1))
check('dropping_zero_block_corrupts_observable',sum(x[1] for x in p if x[0]!=0)==0)
check('blocking_weight_norm_contraction',sum(abs(x[0]) for x in p)<=sum(abs(x[0]) for x in v))
check('blocking_phase_improves',phase([x[0] for x in p])>phase([x[0] for x in v]))
check('pushforward_composes',push(p,[[0,1]])==push(v,[[0,1,2]]))
check('pushforward_identity',push(v,[[0],[1],[2]])==v)
check('sum_order_symmetry',push(v,[[2,1,0]])==push(v,[[0,1,2]]))
check('zero_block_decodes_only_zero_insertions',decode(F(0),(F(0),))==(0,))
check('nonzero_block_decoding',decode(F(2),(F(3),F(-1)))==(F(3,2),F(-1,2)))

# Rational positive factors exp(-log(2) X), exp(-log(2) Z).
A=S.Matrix([[S.Rational(5,4),-S.Rational(3,4)],[-S.Rational(3,4),S.Rational(5,4)]])
D=S.diag(S.Rational(1,2),2)
check('trotter_factor_A_hermitian',A==A.T)
check('trotter_factor_A_eigenvalues',set(A.eigenvals())=={S.Rational(1,2),S.Integer(2)})
check('trotter_factor_D_hermitian',D==D.T)
check('trotter_product_not_hermitian',A*D!=(A*D).T)
check('trotter_noncommutation',A*D!=D*A)

print(json.dumps({'status':'PASS','controls_passed':len(checks),'expected_refusals':len(refusals),'checks':checks,'refusals':refusals,'scope':'Finite exact rational/Gaussian-rational fixtures and guard probes; no asymptotic or physical-family certificate.','python':sys.version.split()[0],'sympy':S.__version__},indent=2))
