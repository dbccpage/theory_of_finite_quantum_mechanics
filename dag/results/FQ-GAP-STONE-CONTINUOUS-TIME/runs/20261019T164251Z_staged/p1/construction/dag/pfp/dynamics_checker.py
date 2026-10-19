"""Independent exact predicates. No import of the dynamics producer."""
from fractions import Fraction as Q
from exact_json import require,rational
from review_exact_json import audit_bound
from structure_checker import cm,matmul,matrix,verify as prior_verify

def eq(a,b,label):require(a==b,'G3_WITNESS:'+label)
def rm(a,b):return [[sum(u*v for u,v in zip(row,col)) for col in zip(*b)] for row in a]
def rt(a):return list(map(list,zip(*a)))
def rf(a):return [x for row in a for x in row]
def power(a,k):
    if k==0:return [[Q(int(i==j)) for j in range(len(a))] for i in range(len(a))]
    b=power(a,k//2);b=rm(b,b)
    return rm(b,a) if k%2 else b
def units(v,lo,hi):require(v.denominator==1 and lo<=v<=hi,'G1_SCHEMA:bounded_integer');return int(v)
def rot(t):return [[(1-t*t)/(1+t*t),2*t/(1+t*t)],[-2*t/(1+t*t),(1-t*t)/(1+t*t)]]
def verify(kind,values,raw):
    x=list(map(rational,values));r=list(map(rational,raw))
    if kind=='path':
        a=[x[:2],x[2:4]];m=units(x[4],0,3);n=units(x[5],0,3);want=rf(power(a,m+n));eq(r,want*3,'bounded_path_and_power_composition')
    elif kind=='transfer':
        a,b=[x[:2],x[2:4]],[x[4:6],x[6:8]];v=[[x[8]],[x[9]]];f=[x[10:12]]
        eq(r,[q for mat in [rm(a,b),rm(rm(a,b),v),rm(a,rm(b,v)),rm(f,a),rm(f,rm(a,v)),rm(rm(f,a),v)] for q in rf(mat)],'Fubini_action_and_dual')
    elif kind=='overcount':
        a,b,d=x;z=[1,0,0,a,1,0,d+a*b,b,1];zz=[1,0,0,2*a,1,0,2*d+3*a*b,2*b,1]
        eq(r,z+zz+[a*b,d,d+a*b,2*d+3*a*b],'all_acyclic_split_points')
    elif kind=='refinement':
        n,m,k,u=x;eq(r,[u+n-k,u+n-k,n,k-n,abs(k-n)],'affine_refinement_not_convergence')
    elif kind=='histories':
        a,b,c,d=x;p=a*c;q=b*d;eq(r,[p,q,p+q,(p+q)**2,p*p+q*q,2*p*q],'declared_history_interference')
    elif kind=='held':
        a,b=x;eq(r,[a*a,b*b,a*a,b*b,a*a+2*a*b+b*b,a*a-2*a*b+b*b,4*a*b],'phase_blind_lift_ambiguity')
    elif kind=='schrodinger':
        h0,h1,u,v,a,b,c,d,dt,hbar=x;require(hbar>0 and len(r)==17,'G1_SCHEMA:Hermitian_rate_domain')
        hp=[h0*a+u*c-v*d,h0*b+u*d+v*c,u*a+v*b+h1*c,u*b-v*a+h1*d];der=[hp[1]/hbar,-hp[0]/hbar,hp[3]/hbar,-hp[2]/hbar];ps=[a,b,c,d];e=[q+dt*z for q,z in zip(ps,der)]
        rate=2*sum(q*z for q,z in zip(ps,der));n0=sum(q*q for q in ps);n1=sum(q*q for q in e)
        eq(r,hp+der+[rate,n0]+e+[n1,n1-n0,dt*dt*sum(q*q for q in der)],'actual_Hpsi_and_Euler_step');eq(rate,0,'instantaneous_mass_rate')
    elif kind=='cayley':
        t=x[0];u=rot(t);e=[[1,t],[-t,1]];eye=[1,0,0,1]
        eq(r,rf(u)+rf(rm(rt(u),u))+rf(e)+rf(rm(rt(e),e))+[0]*4+eye+eye+[1+t*t],'Cayley_Euler_and_Clifford');eq(r[4:8],eye,'Cayley_orthogonality')
    elif kind=='lambda':
        require(len(r)==204,'G1_SCHEMA:three_Gaussian_matrices');s=x[0];z=(Q(0),Q(0));ls=[[[z,(s,Q(0)),z],[(s,Q(0)),z,z],[z,z,z]],[[z,(Q(0),-s),z],[(Q(0),s),z,z],[z,z,z]],[[(s,Q(0)),z,z],[z,(-s,Q(0)),z],[z,z,z]]]
        for i in range(3):eq(matrix(r[18*i:18*(i+1)],3,3),ls[i],'declared_GellMann_block')
        for i in range(3):
            a,b=matmul(ls[i],ls[(i+1)%3]),matmul(ls[(i+1)%3],ls[i]);comm=[[(a[j][k][0]-b[j][k][0],a[j][k][1]-b[j][k][1]) for k in range(3)] for j in range(3)];rhs=[[cm((0,2*s),q) for q in row] for row in ls[(i+2)%3]]
            eq(matrix(r[54+18*i:72+18*i],3,3),comm,'actual_commutator');eq(matrix(r[108+18*i:126+18*i],3,3),rhs,'scaled_cyclic_relation');eq(comm,rhs,'cyclic_relation')
        for k in range(2):eq(matrix(r[162+18*k:180+18*k],3,3),[[(Q(int(i==j==k)),Q(0)) for j in range(3)] for i in range(3)],'projector_square')
        eq(r[198:],[0]*6,'zero_traces_not_zero_commutators')
    elif kind=='heisenberg':
        t,a,b,c,v,w=x;u=rot(t);A=[[a,b],[b,c]];psi=[[v],[w]];ah=rm(rt(u),rm(A,u));ps=rm(u,psi)
        f=rm(rt(ps),rm(A,ps))[0][0];g=rm(rt(psi),rm(ah,psi))[0][0];eq(r,rf(ah)+rf(ps)+rf(rm(rt(u),u))+[f,g],'declared_picture_identity');eq(f,g,'picture_pairing')
    elif kind=='decoherence':
        a,b=x;eq(r,[a*a,a*b,a*b,b*b,a*a,b*b,0,a*a+b*b,(a+b)**2,a+b,a*a+b*b],'actual_class_operator_Gram')
    elif kind=='global':
        a,b,c=x;eq(r,[a+c,a+2*b+c,2*b,a-2*b+c],'offdiagonal_global_weight')
    elif kind=='ccr':
        n=units(x[0],1,3);a=[x[1+i*n:1+(i+1)*n] for i in range(n)];at=1+n*n;b=[x[at+i*n:at+(i+1)*n] for i in range(n)];ab=rm(a,b);ba=rm(b,a);comm=[[ab[i][j]-ba[i][j] for j in range(n)] for i in range(n)];tr=sum(comm[i][i] for i in range(n));eq(r,rf(comm)+[tr,n*x[-1],n],'finite_CCR_trace');eq(tr,0,'cyclic_trace')
    elif kind=='dichotomy':
        k=units(x[0],1,8);p=(Q(1),Q(0));i=(Q(1),Q(0))
        for _ in range(k):p=cm(p,(Q(3),Q(4)));i=cm(i,(Q(0),Q(1)))
        den=5**k;eq(r,[p[0],p[1],den,p[0]/den,p[1]/den,p[0]%5,p[1]%5,*i,(p[0]**2+p[1]**2)/den**2,int(i==(1,0))],'actual_power_residue_and_periodic_control');require(p[1]!=0,'G3_WITNESS:nonidentity_on_retained_powers')
    elif kind=='stone':return prior_verify('time',values,raw)
    elif kind=='everett':
        require(x and all(q>=0 for q in x) and sum(x)==1 and len(r)==len(x)+10,'G1_SCHEMA:normalized_weights')
        N=r[0];counts=r[1:1+len(x)];require(N.denominator==1 and N>0 and all(q.denominator==1 and q>=0 for q in counts),'G1_SCHEMA:integer_finegraining')
        require(all(a/N==b for a,b in zip(counts,x)) and sum(counts)==r[1+len(x)]==N,'G3_WITNESS:exact_multiplicities')
        # Every normalized denominator must divide N; test the actual minimal common denominator independently.
        from math import lcm
        require(int(N)==lcm(*(q.denominator for q in x)),'G3_WITNESS:minimal_denominator')
        eq(r[2+len(x):],[0,0,0,0,1,0,Q(1,2),Q(1,10)],'quadratic_irrational_witness_coefficients')
    elif kind=='embedding':
        a,b,c,d,n=x;n=units(n,3,120);g=[cm((a,b),(a,b),5),cm((a,b),(c,d),5),cm((c,d),(c,d),5)];gc=[(a,-b) for a,b in g]
        expected=[z for p in g+gc+[(0,0),(-2,1),(3,-1),(-2,-1),(3,1)] for z in p]
        phi=n;v=n;p=2
        while p*p<=v:
            if v%p==0:
                phi-=phi//p
                while v%p==0:v//=p
            p+=1
        if v>1:phi-=phi//v
        eq(r,expected+[phi,Q(phi,2),2,3,4,5,9,Q(1,16)],'actual_quadratic_field_coefficients_and_isolation');require(4<5<9,'G3_WITNESS:real_root_interval')
    elif kind=='stone_gap':
        n=units(x[0],0,16);k=units(x[1],-16,16);eq(r,[n*k%4,n*(k+4)%4,n*k%8,n*(k+4)%8,0],'finite_phase_aliasing')
    elif kind=='cptp':
        t=x[0];require(t>=0 and len(r)==40,'G1_SCHEMA:Bell_scale');v=[1,0,0,1];rho=[[t*v[i]*v[j]/2 for j in range(4)] for i in range(4)];pt=[[rho[2*(i//2)+j%2][2*(j//2)+i%2] for j in range(4)] for i in range(4)];w=[0,1,-1,0];quad=sum(w[i]*pt[i][j]*w[j] for i in range(4) for j in range(4));eq(r,rf(rho)+rf(pt)+[quad,2,t,t,1,0,0,1],'positive_input_and_partial_transpose');eq(quad,-t,'negative_quadratic_control')
    elif kind=='condition':
        n=units(x[0],1,4);w=x[1:1+n];mask=x[1+n:];require(len(mask)==n and all(q>=0 for q in w) and all(s in (0,1) for s in mask),'G1_SCHEMA:sector_weights');mass=sum(q*s for q,s in zip(w,mask));require(mass>0,'G1_SCHEMA:positive_sector_mass');p=[q*s/mass for q,s in zip(w,mask)];eq(r,[mass]+p+p+[1],'Bayesian_idempotence')
    else:raise ValueError('G1_SCHEMA:unknown_operation')

def check(request,candidate,task,config,root):
    _,c,public=audit_bound(request,candidate,task,config);require(set(c['data'])=={'records'} and len(c['data']['records'])==len(public['cases']),'G1_SCHEMA:record_coverage')
    for record,values in zip(c['data']['records'],public['cases']):require(record['input']==values,'G5_SCOPE:public_input_identity');verify(public['kind'],values,record['output'])
    return {'records_checked':len(public['cases']),'scope':'Exact retained cases and literal named Lean statements; mathematical imports and transport obligations remain explicit.'}
