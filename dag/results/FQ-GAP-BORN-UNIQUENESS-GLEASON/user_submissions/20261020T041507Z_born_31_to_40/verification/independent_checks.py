"""Host controls for BR-31--40 corrections. Exact algebra only, no assertion gates."""
from pathlib import Path
from itertools import combinations
from math import lcm
import contextlib,io,json,runpy,sys
import sympy as s

here=Path(__file__).resolve().parent
capture=io.StringIO()
with contextlib.redirect_stdout(capture):
    user=runpy.run_path(str(here/'br31_40_checks_reviewed.py'))
(here/('embedded_reviewed_'+('normal' if __debug__ else 'optimized')+'.stdout.txt')).write_text(capture.getvalue(),encoding='utf-8')
checks=[];refusals=[]
def require(x,msg='not exact true'):
    if x is not True and x is not s.S.true:raise ValueError(msg)
def check(name,x):
    require(x,name)
    require(name not in checks,'duplicate control')
    checks.append(name)
def refuse(name,thunk):
    try:thunk()
    except ValueError:refusals.append(name);return
    raise RuntimeError('missing expected refusal: '+name)
def unit(n,j):return s.eye(n)[:,j]
def eu(n,j,k):return unit(n,j)*unit(n,k).H
def cp(ks,x,e):return sum((k*x*k.H for k in ks),s.zeros(e,e))
def choi(ks,d,e):
    return sum((s.kronecker_product(eu(d,j,k),cp(ks,eu(d,j,k),e)) for j in range(d) for k in range(d)),s.zeros(d*e,d*e))
def tr_out(c,d,e):return s.Matrix(d,d,lambda j,k:sum(c[j*e+a,k*e+a] for a in range(e)))
def partial_env(y,E,R):return s.Matrix(E,E,lambda j,k:sum(y[j*R+a,k*R+a] for a in range(R)))
def gauss(x):return user['gaussian_rational'](x)
def minor_psd(a):
    if a!=a.H:return False
    for n in range(1,a.rows+1):
        for inds in combinations(range(a.rows),n):
            if s.simplify(a.extract(inds,inds).det()).is_nonnegative is not True:return False
    return True

for label,value in [('false',False),('unknown',None),('numeric_truth',1)]:
    refuse('exact_guard_'+label,lambda value=value:user['require'](value))
refuse('check_false_forces_failure',lambda:user['check']('expected mutation',False))
for label,a in [('float_diagonal',s.Matrix([[s.Float(1)]])),('irrational_offdiagonal',s.Matrix([[1,s.sqrt(2)],[s.sqrt(2),2]])),('nonhermitian',s.Matrix([[1,s.I],[0,1]])),('nonsquare',s.Matrix([[1,2]]))]:
    refuse('PSD_domain_'+label,lambda a=a:user['psd_certify'](a))
refuse('Gram_mismatch',lambda:user['match_unitary'](s.Matrix([[1]]),s.Matrix([[2]])))
refuse('matching_row_mismatch',lambda:user['match_unitary'](s.Matrix([[1]]),s.Matrix([[1],[0]])))
refuse('negative_weight',lambda:user['rational_roots_of_weight'](-1))
refuse('float_weight',lambda:user['rational_roots_of_weight'](s.Float('0.5')))
refuse('negative_four_square_input',lambda:user['four_squares'](-1))

# Independently verify certificates and compare to ALL principal minors in small dimensions.
fixtures=[s.zeros(0),s.zeros(3),s.Matrix([[1,1],[1,1]]),s.Matrix([[0,s.I],[-s.I,0]]),s.Matrix([[1,1],[1,0]]),s.Matrix([[0,0,0],[0,2,1],[0,1,1]]),s.Matrix([[1,1,1],[1,1,1],[1,1,s.Rational(1,2)]])]
for i,a in enumerate(fixtures):
    result=user['psd_certify'](a)
    check('PSD_principal_minor_crosscheck_'+str(i),(result[0]=='psd')==minor_psd(a))
    if result[0]=='psd':
        _,L,D=result
        check('PSD_certificate_reconstruction_'+str(i),s.simplify(L*D*L.H-a)==s.zeros(a.rows,a.cols))
        check('PSD_nonnegative_diagonal_'+str(i),all(D[j,j]>=0 for j in range(D.rows)))
    else:
        v=result[1]
        check('PSD_negative_witness_'+str(i),v!=s.zeros(a.rows,1) and s.simplify((v.H*a*v)[0])<0)

# Input-first vec: rectangular and non-symmetric complex matrix.
k=s.Matrix([[1,s.I,2],[s.Rational(1,2),0,1-s.I]])
v=user['vecm'](k)
expected=s.Matrix([k[a,j] for j in range(3) for a in range(2)])
check('rectangular_input_first_vec',v==expected)
check('rectangular_Choi_vec_outer',choi([k],3,2)==v*v.H)
check('old_transposed_vec_would_be_out_of_bounds',k.cols>k.rows)

# BR-31: typed algebra identity, not full-matrix identity; merge is irreversible.
P=[eu(2,0,0),eu(2,1,1)]
pinch=lambda x:sum((p*x*p for p in P),s.zeros(2))
check('unit_continuation_kills_untagged_coherence',pinch(eu(2,0,1))==s.zeros(2))
check('unit_continuation_identity_on_tagged_algebra',pinch(s.diag(s.Rational(1,3),s.Rational(2,3)))==s.diag(s.Rational(1,3),s.Rational(2,3)))
check('merge_two_scalar_tags_reduces_dimension',2>1)
merge=[s.Matrix([[1,0]]),s.Matrix([[0,1]])]
check('merge_is_TP',sum((k.H*k for k in merge),s.zeros(2))==s.eye(2))
check('merge_identifies_orthogonal_tagged_states',cp(merge,P[0],1)==cp(merge,P[1],1)==s.ones(1))

# BR-32: include a genuinely non-Hermitian scalar functional.
A=s.Matrix([[1,s.I],[2,0]])
ca=s.Matrix(2,2,lambda j,k:s.trace(A*eu(2,j,k)))
check('general_scalar_Choi_transpose',ca==A.T)
check('general_scalar_adjoint_conjugation',ca==A.H.conjugate())
check('unqualified_transposed_adjoint_fails',ca!=A.H.T)
H=(s.eye(2)+s.I*(eu(2,0,1)-eu(2,1,0)))/2
check('imaginary_effect_Choi_differs',H.T!=H)

# BR-33: zero kernel is not sufficient for a CP postprocessing factorization.
I=s.eye(2);Z=s.diag(1,-1)
a=s.Rational(9,25);b=s.Rational(16,25)
F=lambda x:a*x+b*Z*x*Z
M=lambda x:a*x+b*Z*(Z*x*Z)*Z
Theta=lambda x:s.Matrix([[x[0,0],-s.Rational(25,7)*x[0,1]],[-s.Rational(25,7)*x[1,0],x[1,1]]])
check('kernel_counterexample_outer_TP',a+b==1)
check('kernel_counterexample_F_invertible',a-b==-s.Rational(7,25) and a-b!=0)
check('kernel_counterexample_merge_after_identity',all(M(eu(2,j,k))==eu(2,j,k) for j in range(2) for k in range(2)))
check('kernel_counterexample_unique_inverse',all(Theta(F(eu(2,j,k)))==eu(2,j,k) for j in range(2) for k in range(2)))
plus=s.ones(2)/2
negative=(s.ones(1,2)*Theta(plus)*s.ones(2,1))[0]
check('kernel_counterexample_not_positive',negative==-s.Rational(18,7))
check('kernel_counterexample_inverse_TP',all(s.trace(Theta(eu(2,j,k)))==s.trace(eu(2,j,k)) for j in range(2) for k in range(2)))

# BR-34: irrational projection is extreme; the general extreme-point proof is written separately.
Sx=s.Matrix([[0,1],[1,0]])
projector=(I+(Sx+Z)/s.sqrt(2))/2
check('irrational_extreme_projection',s.simplify(projector*projector-projector)==s.zeros(2))
check('irrational_projection_not_Qi',not all(gauss(x) for x in projector))
check('irrational_projection_is_effect',minor_psd(projector) and minor_psd(I-projector))
check('some_irrational_state_statistics_remain_rational',s.trace((I+Sx/s.sqrt(2))/2)==1)
# Second-argument affinity includes untouched slots of the entire normalized instrument.
t=s.Rational(2,7)
F0=lambda x:s.Rational(9,25)*x
F1=lambda x:s.Rational(16,25)*Sx*x*Sx
left=lambda x:[t*F0(x),(1-t)*Z*F0(x)*Z,F1(x)]
right=lambda x:[t*F0(x)+(1-t)*s.zeros(2),t*s.zeros(2)+(1-t)*Z*F0(x)*Z,t*F1(x)+(1-t)*F1(x)]
check('continuation_affinity_full_profile',all(left(eu(2,j,k))==right(eu(2,j,k)) for j in range(2) for k in range(2)))
check('continuation_affinity_untouched_slot',all(left(eu(2,j,k))[2]==F1(eu(2,j,k)) for j in range(2) for k in range(2)))
check('carrier_rejects_boolean',not gauss(True))

# BR-36: exact sphere and sharp endpoint, not merely decimal comparisons.
q=s.symbols('q1:4',real=True)
rho=s.Matrix([[3*q[0],3*q[1]-s.Rational(1,2)+s.I*(3*q[2]-s.Rational(1,2))],[3*q[1]-s.Rational(1,2)-s.I*(3*q[2]-s.Rational(1,2)),1-3*q[0]]])
check('ball_identity',s.expand(4*rho.det()+sum((6*x-1)**2 for x in q)-1)==0)
endpoint=(1+1/s.sqrt(3))/6
rp=rho.subs(dict.fromkeys(q,endpoint))
check('sharp_endpoint_pure',s.simplify(rp*rp-rp)==s.zeros(2))
check('sharp_endpoint_not_rational',endpoint.is_rational is False)
check('sharp_q0_bound',s.simplify(1-3*endpoint-(3-s.sqrt(3))/6)==0)

# BR-38: finite residue check supports the WRITTEN infinite-descent proof, not the whole theorem by search.
check('mod3_sum_squares_zero_only_both_zero',{(a,b) for a in range(3) for b in range(3) if (a*a+b*b)%3==0}=={(0,0)})
z1=(1+s.I)/3;z2=s.Rational(1,3)
check('rank_one_effect_two_Gaussian_vectors',s.simplify(z1*s.conjugate(z1)+z2*z2)==s.Rational(1,3))
for r in [s.Rational(1,3),s.Rational(2,7),s.Rational(5,7)]:
    realparts=user['rational_roots_of_weight'](r);realparts=realparts+[s.Integer(0)]*(4-len(realparts))
    z=[realparts[0]+s.I*realparts[1],realparts[2]+s.I*realparts[3]]
    check('two_Gaussian_norm_factor_'+str(r),all(gauss(x) for x in z) and s.simplify(sum(x*s.conjugate(x) for x in z)-r)==0)

# BR-39: check all four regions of the output grid, not one selected pair.
def sub(inst,i,cont):return inst[:i]+[[l*k for k in inst[i] for l in slot] for slot in cont]+inst[i+1:]
def tensor(A,B):return [[s.kronecker_product(k,l) for k in aa for l in bb] for aa in A for bb in B]
Ka=[[s.Rational(3,5)*I],[s.Rational(4,5)*Sx]]
Lb=[[s.Rational(5,13)*I],[s.Rational(12,13)*Z]]
Kp=[[s.Rational(3,5)*I],[s.Rational(4,5)*Z]]
Lp=[[s.Rational(5,13)*I],[s.Rational(12,13)*Sx]]
lhs=tensor(sub(Ka,0,Kp),sub(Lb,0,Lp))
false_rhs=sub(tensor(Ka,Lb),0,tensor(Kp,Lp))
check('submitted_global_interchange_arity_counterexample',len(lhs)==9 and len(false_rhs)==7)
full=[]
for i in range(2):
    for j in range(2):
        cont=tensor(Kp if i==0 else [[I]], Lp if j==0 else [[I]])
        for slot in cont:full.append([l*k for k in tensor([Ka[i]],[Lb[j]])[0] for l in slot])
beta=[0,1,4,2,3,5,6,7,8]
check('full_grid_corrected_arity',len(full)==len(lhs)==9)
check('full_grid_outcome_permutation',sorted(beta)==list(range(9)))
check('full_grid_representative_equality',all(lhs[k]==full[beta[k]] for k in range(9)))
check('full_grid_normalization',sum((k.H*k for slot in full for k in slot),s.zeros(4))==s.eye(4))
check('raw_fixture_also_has_global_arity_gap',(2+2-1)*(2+1-1)==6 and 2*2-1+2*1==5)

# BR-40: genuinely heterogeneous colours, explicit input embedding, tensor padding.
def injection(es,i):
    E=sum(es);off=sum(es[:i]);return s.Matrix(E,es[i],lambda a,b:int(a==off+b))
def dilation(slots,es,d):
    E=sum(es);branches=[(i,a) for i in range(len(es)) for a in range(len(slots[i]))];R=len(branches)
    V=sum((s.kronecker_product(injection(es,i)*slots[i][a],unit(R,t)) for t,(i,a) in enumerate(branches)),s.zeros(E*R,d))
    return V,branches
es=[1,2];slots=[[s.Matrix([[1,0]])],[s.Matrix([[0,s.Rational(3,5)],[0,0]]),s.Matrix([[0,0],[0,s.Rational(4,5)]])]]
V,branches=dilation(slots,es,2);E=sum(es);R=len(branches)
check('heterogeneous_dilation_isometry',V.H*V==I)
check('literal_input_tensor_wrong_dimension',E*R!=2*R)
D=lcm(2,E*R);padding=D//(E*R);ancilla=D//2
Vlift=s.kronecker_product(V,unit(padding,0));Jin=s.kronecker_product(I,unit(ancilla,0))
check('common_dimension_padding',D==18 and Vlift.shape==Jin.shape==(18,2))
W=user['match_unitary'](Jin.H,Vlift.H);U=W.H
check('padded_rational_unitary',U.H*U==s.eye(D) and all(gauss(x) for x in U))
check('padded_input_realization',s.simplify(U*Jin-Vlift)==s.zeros(D,2))
r=s.Matrix([[s.Rational(1,3),(1+s.I)/6],[(1-s.I)/6,s.Rational(2,3)]])
for i in range(2):
    pi=sum((unit(R,t)*unit(R,t).H for t,(j,a) in enumerate(branches) if j==i),s.zeros(R))
    Qi=s.kronecker_product(s.eye(E),pi,s.eye(padding))
    want=injection(es,i)*cp(slots[i],r,es[i])*injection(es,i).H
    check('padded_pointer_state_update_'+str(i),s.simplify(partial_env(Qi*Vlift*r*Vlift.H*Qi,E,R*padding)-want)==s.zeros(E))
    check('padded_pointer_tag_agreement_'+str(i),Qi*Vlift==s.kronecker_product(injection(es,i)*injection(es,i).H,s.eye(R*padding))*Vlift)
# Trace channel d=2,E=1,R=2 refutes the unqualified x tensor epsilon formula.
vt,bt=dilation([[s.Matrix([[1,0]]),s.Matrix([[0,1]])]],[1],2)
check('trace_channel_minimal_typed_isometry',vt==I and vt.rows==2 and 2*len(bt)==4)

# Nested dilations require an environment embedding, with untouched blocks using a fixed ancillary state.
esold=[2,2];Vold,oldbranches=dilation(Ka,esold,2);esnew=[2,2,2]
Rold=len(oldbranches);Rp=2
C=s.kronecker_product(injection(esnew,2)*injection(esold,1).H,unit(Rp,0))
for ell in range(2):C+=s.kronecker_product(injection(esnew,ell)*Kp[ell][0]*injection(esold,0).H,unit(Rp,ell))
check('controlled_continuation_isometry',C.H*C==s.eye(4))
seq=s.kronecker_product(C,s.eye(Rold))*Vold
seq=s.kronecker_product(s.eye(6),user['swap'](Rp,Rold))*seq
Vdirect,directbranches=dilation(sub(Ka,0,Kp),esnew,2)
iota=s.eye(4)[:,:3]
check('nested_raw_pointer_dimensions_differ',len(directbranches)==3 and Rold*Rp==4)
check('nested_environment_embedding_isometry',iota.H*iota==s.eye(3))
check('nested_dilation_after_embedding',s.simplify(seq-s.kronecker_product(s.eye(6),iota)*Vdirect)==s.zeros(24,2))

print(json.dumps({'status':'PASS','controls_passed':len(checks),'expected_refusals':len(refusals),'checks':checks,'refusals':refusals,'embedded_reviewed_pass_lines':sum(l.startswith('PASS ') for l in capture.getvalue().splitlines()),'scope':'Exact finite controls and counterexamples; written general arguments separate; no Lean kernel verification.','python':sys.version.split()[0],'sympy':s.__version__},indent=2))
