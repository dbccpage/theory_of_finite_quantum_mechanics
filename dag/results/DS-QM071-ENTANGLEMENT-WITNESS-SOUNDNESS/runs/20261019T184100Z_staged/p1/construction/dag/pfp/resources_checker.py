"""Independent equations for resource certificates; no producer imports."""
from fractions import Fraction as Q
from itertools import product
from exact_json import require,rational
from review_exact_json import audit_bound

def eq(a,b):require(a==b,'G3_WITNESS:resource_equations')
def u(a):require(0<=a<=1,'G1_SCHEMA:unit_interval')
def integer(a,lo,hi):require(a.denominator==1 and lo<=a<=hi,'G1_SCHEMA:integer_domain');return int(a)
def contextual(v):
    require(len(v)==16 and min(v)>=0,'G1_SCHEMA:context_table')
    A=[];B=[];E=[]
    for k in range(4):
        a,b,c,d=v[4*k:4*k+4];eq(a+b+c+d,1);A.extend([a+b,c+d]);B.extend([a+c,b+d]);E.append(a-b-c+d)
    D=[A[i]-A[i+2] for i in (0,1,4,5)]+[B[i]-B[i+4] for i in range(4)]
    F=[v[4*k+2*a+b]-A[2*k+a]*B[2*k+b] for k in range(4) for a,b in product(range(2),repeat=2)]
    return [Q(1)]*4+A+B+D+E+[E[0]+E[1]+E[2]-E[3]]+F
def noisy(v):
    u(v);hi=(1+v)/4;lo=(1-v)/4
    return [hi,lo,lo,hi]*3+[lo,hi,hi,lo]
def verify(kind,values,raw):
    x=list(map(rational,values));r=list(map(rational,raw))
    if kind=='projection':
        a,b,e,f=x;require(a>=0 and b>=0 and a+b>0,'G1_SCHEMA:weights');u(e);u(f)
        eq(r,[e*a,f*b,e*e*a,f*f*b,e*(e-1),f*(f-1),a/(a+b),a*a/(a*a+b*b)])
    elif kind in ('fiber','interference'):
        a,b,c,d=x;A=a*a+b*b;B=c*c+d*d;h=2*(a*c+b*d)
        eq(r,[A,B,A,B,A+B+h,A+B-h,h,h,-h,2*h])
    elif kind=='buildability':
        la,mu,eps,floor,reach,adv=x;require(min(la,mu,eps)>=0,'G1_SCHEMA:nonnegative_rates');integer(reach,0,1);integer(adv,0,1)
        b=[int(la<=mu+eps),int(floor>0),int(reach),int(adv)];eq(r,[la-mu-eps]+b+[int(sum(b)==4)])
    elif kind=='torsion':
        k=integer(x[0],0,32);patterns=[[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0]]
        eq(r,patterns[k%4]+[k%4,k%4,k+4])
    elif kind=='selector':
        a,b,c,d=x;z=a*c-b*d;w=a*d+b*c;s=a*a+b*b;eq(r,[z,-w,w,z,z,w,s,0,0,s])
    elif kind=='holonomy':
        a,b,c,d,t=x;den=1+t*t;g=(1-t*t)/den;h=2*t/den;ga=g*a-h*b;gb=h*a+g*b;gc=g*c-h*d;gd=h*c+g*d;H=a*c+b*d;I=a*d-b*c;intensity=(a+c)**2+(b+d)**2
        eq(r,[g,h,ga,gb,gc,gd,H,I,H,I,a*a+b*b,c*c+d*d,intensity,intensity,2*H]);eq(g*g+h*h,1)
    elif kind=='annex':
        a,b,c,f,g,h,p,q,v,w,t=x;u(p);u(q);s=p*v+q*w;z=(1-p)*v+(1-q)*w
        eq(r,[g-f,h-g,f-h,0,a+b+c,a+b+c,s,z,abs(v)+abs(w),abs(s)+abs(z)]+contextual(noisy(t)))
        require(abs(s)+abs(z)<=abs(v)+abs(w),'G3_WITNESS:contraction')
    elif kind=='product':
        a,b,c,d=x;require(min(x)>=0 and sum(x)>0,'G1_SCHEMA:joint_weights');W=sum(x);row=[a+b,c+d];col=[a+c,b+d];det=a*d-b*c
        eq(r,[W]+row+col+[z/W for z in row+col]+[s*t/(W*W) for s in row for t in col]+[z/W for z in x]+[det,-det,-det,det,4*det*det,det])
    elif kind=='witness':
        a,b,c,d=x;eq(a*a+b*b,1);eq(c*c+d*d,1);v=[a*c,a*d,b*c,b*d];f=(a*c+b*d)**2/2;gap=(a*d-b*c)**2/2
        eq(r,v+[s*t for s in v for t in v]+[1,f,gap,gap,1,Q(1,2)]);require(f<=Q(1,2),'G3_WITNESS:product_fidelity')
    elif kind=='qubit':
        a,b=x;N=a*a+b*b;require(N>0,'G1_SCHEMA:nonzero_lift');p=a*a/N;c=a*b/N
        eq(r,[p,c,c,1-p,p,-c,-c,1-p,p,0,0,1-p,p,1-p,Q(1,2)+c,Q(1,2)-c,1,p*p+(1-p)**2])
    elif kind=='bell_import':eq(r,noisy(x[0])+contextual(noisy(x[0])))
    elif kind=='chsh':
        require(len(x)==16 and min(x)>=0 and sum(x)==1,'G1_SCHEMA:global_joint');rows=list(product((-1,1),repeat=4));E=[sum(w*s[i]*s[2+j] for w,s in zip(x,rows)) for i,j in product(range(2),repeat=2)];C=[s[0]*s[2]+s[0]*s[3]+s[1]*s[2]-s[1]*s[3] for s in rows];value=E[0]+E[1]+E[2]-E[3]
        eq(r,C+E+[value,2,2]+noisy(Q(1)));require(abs(value)<=2,'G3_WITNESS:global_CHSH')
    elif kind=='nosignal':eq(r,contextual(x))
    elif kind=='trace_select':
        p,q,c=x;u(p);u(q);require(c>=0,'G1_SCHEMA:scale');a=abs(p-q);eq(r,[p-q,q-p,a,a,a,a,c*a,2*a])
    elif kind=='dual':
        a,s,t,k=x;require(abs(s)<=1 and abs(t)<=1,'G1_SCHEMA:dual_ball');sg=1 if a>=0 else -1;v=a*(s-t);eq(r,[v,v,2*abs(a),2*abs(a),sg,-sg,abs(a)]);require(abs(v)<=2*abs(a),'G3_WITNESS:dual_bound')
    elif kind=='monotone':
        p,q,a,b=x;u(p);u(q);v=p*a+q*b;w=(1-p)*a+(1-q)*b;A=abs(a)+abs(b);B=abs(v)+abs(w);eq(r,[v,w,A,B,2*A,2*B,A-B,2*(A-B)]);require(B<=A,'G3_WITNESS:contraction')
    elif kind=='stochastic':
        require(len(x)==12 and min(x[:9])>=0,'G1_SCHEMA:kernel3');K=x[:9];v=x[9:];eq([sum(K[3*i+j] for i in range(3)) for j in range(3)],[1]*3)
        y=[sum(K[3*i+j]*v[j] for j in range(3)) for i in range(3)];b=[sum(K[3*i+j]*abs(v[j]) for j in range(3)) for i in range(3)];A=sum(map(abs,v));B=sum(map(abs,y));eq(r,[1]*3+y+[A,B]+b);require(B<=A,'G3_WITNESS:finite_kernel_contraction')
    elif kind=='channel':
        t,u0,p,c=x;u(p);require(c*c<=p*(1-p),'G1_SCHEMA:density');r0=(1-t*t)/(1+t*t);s0=2*t/(1+t*t);r1=(1-u0*u0)/(1+u0*u0);s1=2*u0/(1+u0*u0);K=[r0*r0,r1*r1,s0*s0,s1*s1];a=K[0]*p+K[1]*(1-p);b=1-a
        eq(r,K+[r0,0,0,0,0,0,s0,0,0,r1,0,0,0,0,0,s1]+[1,0,0,1]+[a,0,0,b]+[p,c,c,1-p]+[p,0,0,1-p]+K[2:]+K[:2])
    elif kind=='firewall':
        score,defect,bound=x
        for z in x:integer(z,0,1000000)
        gate=int(defect==0);eq(r,[score,defect,bound,gate,score+1,gate])
    else:raise ValueError('G1_SCHEMA:unknown_resource_operation')
def check(request,candidate,task,config,root):
    _,c,p=audit_bound(request,candidate,task,config)
    require(set(c['data'])=={'records'} and len(c['data']['records'])==len(p['cases']),'G1_SCHEMA:coverage')
    for record,values in zip(c['data']['records'],p['cases']):
        require(record['input']==values,'G5_SCOPE:public_input_identity');verify(p['kind'],values,record['output'])
    return {'records_checked':len(p['cases']),'scope':'Exact retained cases plus separately named Lean signatures; original imports and formal transports stay explicit.'}
