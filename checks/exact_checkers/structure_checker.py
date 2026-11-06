"""Independent exact predicates, with no import of the witness producer."""
from fractions import Fraction as Q
from exact_json import require,rational
from review_exact_json import audit_bound

def cm(a,b,d=-1):return (a[0]*b[0]+d*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def ca(a,b):return (a[0]+b[0],a[1]+b[1])
def dot(a,b,d=-1):
    acc=(Q(0),Q(0))
    for u,v in zip(a,b):acc=ca(acc,cm(u,v,d))
    return acc
def matmul(a,b,d=-1):return [[dot(row,col,d) for col in zip(*b)] for row in a]
def matrix(raw,n,m):
    pairs=list(zip(raw[::2],raw[1::2]));require(len(raw)==2*n*m,'G1_SCHEMA:matrix_shape');return [pairs[i*m:(i+1)*m] for i in range(n)]
def equals(actual,wanted,label):require(actual==wanted,'G3_WITNESS:'+label)

def verify(kind,values,raw):
    v=list(map(rational,values));r=list(map(rational,raw))
    if kind=='power':
        p=v[0];require(p.denominator==1 and 1<=p<=16,'G1_SCHEMA:positive_integer_power');p=int(p)
        require(len(r)==6,'G1_SCHEMA:power_record');n=(5**p+3**p+4**p)/Q(5**p)
        equals(r,[n,Q(1,2),1/n,(n-2)/(2*n),Q(3**p-3*2**p+3),Q(4-2**p)],'power_context_and_sign_control')
    elif kind=='selection':
        a,b=v;require(len(r)==7 and a*a+b*b>0,'G1_SCHEMA:nonzero_preparation')
        n,m,p,q,u,w,d=r
        require(n==a*a+b*b and m==a**4+b**4 and n*p==a*a and n*q==b*b and m*u==a**4 and m*w==b**4 and d==p-u and p+q==u+w==1,'G3_WITNESS:distinct_supplied_readouts')
    elif kind=='quotient':
        require(all(x.denominator==1 for x in v) and len(r)==1+len(v)+len(v)**2,'G1_SCHEMA:finite_report_domain')
        labels=sorted(set(v));equals(r[0],len(labels),'class_count');equals(r[1:1+len(v)],[labels.index(x) for x in v],'canonical_class_map')
        rel=r[1+len(v):]
        for i,a in enumerate(v):
            for j,b in enumerate(v):require(rel[i*len(v)+j]==int(a==b),'G3_WITNESS:report_kernel')
    elif kind=='sorkin':
        a,b,c,alpha,beta,A,B=v
        require(len(r)==8,'G1_SCHEMA:sorkin_record')
        equals(r[0],12*beta*a*b*c*(a+b+c),'polynomial_I3');equals(r[1],r[0],'I3_closed_form')
        equals(r[2:6],[7,4,7,-4],'actual_zeta_norm_coordinates')
        equals(r[6:],[7*A+4*B,7*A-4*B],'readout_basis_coordinates')
    elif kind=='pinching':
        a,b,c=v;require(c>0,'G1_SCHEMA:positive_scale')
        equals(r,[4*(a*a+b*b),4*a*a,4*b*b,4*c*c*(a*a+b*b),4*c*c*a*a],'trace_norm_squared_pinching')
        require(r[1]<=r[0] and r[4]<=r[3],'G3_WITNESS:contraction')
    elif kind=='k23':
        t=v[0];require(t>=0 and len(r)==133,'G1_SCHEMA:k23_shape_scale');at=0
        def read(rows):
            nonlocal at
            out=[r[at+3*i:at+3*i+3] for i in range(rows)];at+=rows*3;return out
        defects,mtz,mall,pot,res,dt,da=read(6),read(6),read(6),read(5),read(6),read(5),read(5)
        edges=[(a,2+k) for a in range(2) for k in range(3)]
        for e,(u,w) in enumerate(edges):
            k=e%3;D=[Q(2 if j==k else -1) for j in range(3)]
            equals(defects[e],[t*d if u==0 else 0 for d in D],'matrix_defect')
            equals(mtz[e],[d/Q(3)*(1 if u==0 else -1) for d in D],'tracezero_dual');equals(mall[e],[d/Q(4)*(1 if u==0 else -1) for d in D],'allHermitian_dual')
            require(max(mtz[e])-min(mtz[e])<=1 and max(map(abs,mall[e]))<=Q(1,2),'G3_WITNESS:correct_polar_balls')
            equals(res[e],[defects[e][j]-pot[w][j]+pot[u][j] for j in range(3)],'actual_repair_residual')
        equals(pot,[[t,t,t]]+[[0,0,0]]*4,'allHermitian_primal_potential')
        for ms,declared in [(mtz,dt),(mall,da)]:
            div=[[sum((m[j] if u==i else -m[j] if w==i else 0) for m,(u,w) in zip(ms,edges)) for j in range(3)] for i in range(5)]
            equals(declared,div,'actual_dual_divergence');equals(div,[[0,0,0]]*5,'dual_feasibility')
        pc=[sum(map(abs,d))/2 for d in defects];ac=[sum(map(abs,d))/2 for d in res]
        equals(r[117:123],pc,'tracezero_costs');equals(r[123:129],ac,'allHermitian_costs')
        obj=lambda m:sum(sum(a*b for a,b in zip(z,y)) for z,y in zip(m,defects))
        equals(r[129:],[sum(pc),obj(mtz),sum(ac),obj(mall)],'primal_dual_objectives')
        require(r[129]==r[130]==6*t and r[131]==r[132]==Q(9,2)*t,'G3_WITNESS:zero_gaps')
    elif kind=='tsirelson':
        require(v in ([Q(1)],[Q(-1)]) and len(r)==162,'G1_SCHEMA:SOS_shape_sign');sign=int(v[0])
        C,S,T,L,R=[matrix(r[i:i+32],4,4) for i in range(0,160,32)]
        Z=[1,-1];X=[[0,1],[1,0]]
        P=[[(Z[i//2]*Z[i%2] if i==j else 0)+X[i//2][j//2]*X[i%2][j%2] for j in range(4)] for i in range(4)]
        equals(C,[[(0,p) for p in row] for row in P],'CHSH_operator')
        for a,mat in [(0,S),(1,T)]:
            U=[[1,0],[0,-1]] if a==0 else X
            wanted=[[(Q((U[i//2][j//2] if i%2==j%2 else 0)-sign*(U[i%2][j%2] if i//2==j//2 else 0)),Q(0)) for j in range(4)] for i in range(4)]
            equals(mat,wanted,'SOS_factor');require(mat==list(map(list,zip(*mat))),'G3_WITNESS:self_adjoint_factor')
        ss,tt=matmul(S,S,2),matmul(T,T,2)
        rhs=[[cm((0,Q(1,2)),ca(ss[i][j],tt[i][j]),2) for j in range(4)] for i in range(4)]
        lhs=[[ca((0,Q(2 if i==j else 0)),(0,-sign*P[i][j])) for j in range(4)] for i in range(4)]
        equals(L,lhs,'SOS_lhs');equals(R,rhs,'SOS_rhs');equals(L,R,'exact_two_sided_SOS')
        equals(r[160:],[0,2],'Bell_density_expectation')
    elif kind=='census':
        require(len(v)==8 and all(x in (0,1) for x in v),'G1_SCHEMA:declared_census_labels')
        lost=[i for i,x in enumerate(v) if x];opened=[i for i,x in enumerate(v) if not x]
        equals(r,[8,len(lost),len(opened)]+lost+opened,'declared_partition_not_necessity')
    elif kind=='matrix':
        require(len(v)==24 and all(x.denominator==1 for x in v) and len(r)==40,'G1_SCHEMA:Gaussian_domain')
        A,B=matrix(v[:8],2,2),matrix(v[8:16],2,2);vec=matrix(v[16:20],2,1);u=matrix(v[20:24],2,1)
        AB,Av,ABv,AB_v,AH=matrix(r[:8],2,2),matrix(r[8:12],2,1),matrix(r[12:16],2,1),matrix(r[16:20],2,1),matrix(r[20:28],2,2)
        equals(AB,matmul(A,B),'Gaussian_product');equals(Av,matmul(A,vec),'Gaussian_action');equals(ABv,matmul(AB,vec),'composed_action');equals(AB_v,matmul(A,matmul(B,vec)),'successive_action');equals(ABv,AB_v,'composition_law')
        adjA=[[(A[j][i][0],-A[j][i][1]) for j in range(2)] for i in range(2)];equals(AH,adjA,'conjugate_transpose')
        pair=lambda a,b:dot([(a[i][0][0],-a[i][0][1]) for i in range(2)],[b[i][0] for i in range(2)])
        equals(tuple(r[28:30]),pair(Av,u),'left_pairing');equals(tuple(r[30:32]),pair(vec,matmul(adjA,u)),'adjoint_pairing');equals(r[28:30],r[30:32],'adjoint_law');equals(r[32:],v[:8],'basis_recovery')
    elif kind=='time':
        require(len(v)==2 and all(x.denominator==1 for x in v) and len(r)==30,'G1_SCHEMA:time_domain')
        equals(r[:2],[2*v[0]+1,2*v[1]+1],'declared_branch_labels_not_logarithms')
        codes=[]
        for table in ([0,0],[0,1],[1,0],[1,1]):codes.append(2*table[table[0]]+table[table[1]])
        equals(r[2:6],codes,'actual_Bool_map_squares');require(2 not in codes,'G3_WITNESS:no_Bool_half_step')
        equals(r[6:14],[0,0,4,0,4,0,0,0],'scaled_Gaussian_root');equals(r[14:22],r[6:14],'distinct_negative_root');equals(r[22:],[4,0,0,0,0,0,4,0],'scaled_unitarity')
    else:raise ValueError('G1_SCHEMA:unknown_domain')

def check(request,candidate,task,config,root):
    _,c,public=audit_bound(request,candidate,task,config)
    require(set(c['data'])=={'records'} and len(c['data']['records'])==len(public['cases']),'G1_SCHEMA:record_coverage')
    for record,values in zip(c['data']['records'],public['cases']):
        require(record['input']==values,'G5_SCOPE:public_input_identity');verify(public['kind'],values,record['output'])
    return {'records_checked':len(public['cases']),'scope':'Exact finite records, actual named Lean statements and explicit unpaid imports.'}
