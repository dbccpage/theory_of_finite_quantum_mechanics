"""Exact finite resource witnesses. Supplied carriers and readouts stay supplied."""
from fractions import Fraction as Q
from itertools import product

def domain(ok):
    if not ok: raise ValueError('outside declared exact domain')
def unit(x): domain(0 <= x <= 1)
def integer(x,lo,hi):
    domain(x.denominator==1 and lo<=x<=hi);return int(x)
def mm(a,b):return [[sum(u*v for u,v in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a):return list(map(list,zip(*a)))
def flat(a):return [x for row in a for x in row]
def cm(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def sq(z):return sum(x*x for x in z)
def rotation(t):return ((1-t*t)/(1+t*t),2*t/(1+t*t))
def contexts(t):
    unit(t)
    return [(1+t*((-1)**(a+b+x*y)))/4 for x,y,a,b in product(range(2),repeat=4)]
def table_stats(v):
    domain(len(v)==16 and all(z>=0 for z in v))
    p=lambda x,y,a,b:v[8*x+4*y+2*a+b]
    norms=[sum(p(x,y,a,b) for a,b in product(range(2),repeat=2)) for x,y in product(range(2),repeat=2)]
    domain(norms==[1]*4)
    am=[sum(p(x,y,a,b) for b in range(2)) for x,y,a in product(range(2),repeat=3)]
    bm=[sum(p(x,y,a,b) for a in range(2)) for x,y,b in product(range(2),repeat=3)]
    dev=[am[4*x+a]-am[4*x+2+a] for x,a in product(range(2),repeat=2)]+[bm[2*y+b]-bm[4+2*y+b] for y,b in product(range(2),repeat=2)]
    cor=[sum((-1)**(a+b)*p(x,y,a,b) for a,b in product(range(2),repeat=2)) for x,y in product(range(2),repeat=2)]
    defects=[p(x,y,a,b)-am[4*x+2*y+a]*bm[4*x+2*y+b] for x,y,a,b in product(range(2),repeat=4)]
    return norms+am+bm+dev+cor+[cor[0]+cor[1]+cor[2]-cor[3]]+defects
def evaluate(kind,values):
    x=list(map(Q,values))
    if kind=='projection':
        a,b,e,f=x;domain(a>=0 and b>=0 and a+b>0);unit(e);unit(f)
        v=[e*a,f*b];vv=[e*v[0],f*v[1]]
        out=v+vv+[e*e-e,f*f-f,a/(a+b),a*a/(a*a+b*b)]
    elif kind in ('fiber','interference'):
        a,b,c,d=x;z,w=(a,b),(c,d);iz=cm((0,1),z);iw=cm((0,1),w)
        plus=sq((a+c,b+d));minus=sq((a-c,b-d));cross=2*(a*c+b*d)
        out=[sq(z),sq(w),sq(iz),sq(iw),plus,minus,plus-sq(z)-sq(w),cross,minus-sq(z)-sq(w),4*(a*c+b*d)]
    elif kind=='buildability':
        la,mu,eps,floor,reach,adv=x;domain(all(z>=0 for z in (la,mu,eps)));integer(reach,0,1);integer(adv,0,1)
        bits=[int(la-mu-eps<=0),int(floor>0),int(reach),int(adv)];out=[la-mu-eps]+bits+[int(all(bits))]
    elif kind=='torsion':
        k=integer(x[0],0,32);J=[[Q(0),Q(-1)],[Q(1),Q(0)]];m=[[Q(1),Q(0)],[Q(0),Q(1)]]
        for _ in range(k):m=mm(m,J)
        out=flat(m)+[k%4,(k+4)%4,k+4]
    elif kind=='selector':
        a,b,c,d=x;A=[[a,-b],[b,a]];B=[[c,-d],[d,c]];C=mm(A,B);out=flat(C)+[a*c-b*d,a*d+b*c]+flat(mm(tr(A),A))
    elif kind=='holonomy':
        a,b,c,d,t=x;g=rotation(t);z,w=(a,b),(c,d);gz,gw=cm(g,z),cm(g,w);h=cm((a,-b),w);hh=cm((gz[0],-gz[1]),gw)
        out=list(g)+list(gz)+list(gw)+list(h)+list(hh)+[sq(z),sq(w),sq((a+c,b+d)),sq((gz[0]+gw[0],gz[1]+gw[1])),2*h[0]]
    elif kind=='annex':
        a,b,c,f,g,h,p,q,u,v,t=x;unit(p);unit(q);K=[[p,q],[1-p,1-q]];y=flat(mm(K,[[u],[v]]));out=[g-f,h-g,f-h,(g-f)+(h-g)+(f-h),a+b+c,(a+g-f)+(b+h-g)+(c+f-h)]+y+[abs(u)+abs(v),sum(map(abs,y))]+table_stats(contexts(t))
    elif kind=='product':
        domain(len(x)==4 and all(z>=0 for z in x) and sum(x)>0);W=sum(x);rows=[x[0]+x[1],x[2]+x[3]];cols=[x[0]+x[2],x[1]+x[3]]
        residual=[W*x[2*i+j]-rows[i]*cols[j] for i,j in product(range(2),repeat=2)]
        out=[W]+rows+cols+[r/W for r in rows]+[c/W for c in cols]+[rows[i]*cols[j]/(W*W) for i,j in product(range(2),repeat=2)]+[v/W for v in x]+residual+[sum(z*z for z in residual),x[0]*x[3]-x[1]*x[2]]
    elif kind=='witness':
        a,b,c,d=x;domain(a*a+b*b==1 and c*c+d*d==1);v=[a*c,a*d,b*c,b*d];rho=[[u*w for w in v] for u in v];f=(rho[0][0]+rho[0][3]+rho[3][0]+rho[3][3])/2
        out=v+flat(rho)+[sum(z*z for z in v),f,Q(1,2)-f,(a*d-b*c)**2/2,Q(1),Q(1,2)]
    elif kind=='qubit':
        a,b=x;N=a*a+b*b;domain(N>0);p=a*a/N;c=a*b/N;rho=[[p,c],[c,1-p]];minus=[[p,-c],[-c,1-p]];mixed=[[p,Q(0)],[Q(0),1-p]]
        out=flat(rho)+flat(minus)+flat(mixed)+[p,1-p,Q(1,2)+c,Q(1,2)-c,p*p+(1-p)**2+2*c*c,p*p+(1-p)**2]
    elif kind=='bell_import':
        out=contexts(x[0]);out+=table_stats(out)
    elif kind=='chsh':
        domain(len(x)==16 and all(z>=0 for z in x) and sum(x)==1);signs=list(product((-1,1),repeat=4));coef=[a0*(b0+b1)+a1*(b0-b1) for a0,a1,b0,b1 in signs];corr=[sum(w*s[i]*s[2+j] for w,s in zip(x,signs)) for i,j in product(range(2),repeat=2)]
        value=sum(w*z for w,z in zip(x,coef));out=coef+corr+[value,sum(w*abs(z) for w,z in zip(x,coef)),Q(2)]+contexts(Q(1))
    elif kind=='nosignal':out=table_stats(x)
    elif kind=='trace_select':
        p,q,c=x;unit(p);unit(q);domain(c>=0);d=[p-q,q-p];out=d+[abs(z) for z in d]+[sum(map(abs,d))/2,abs(p-q),c*abs(p-q),2*abs(p-q)]
    elif kind=='dual':
        r,s,t,k=x;domain(abs(s)<=1 and abs(t)<=1);sg=Q(1 if r>=0 else -1);pair=r*s-r*t;out=[pair,r*(s+k)-r*(t+k),2*abs(r),r*sg-r*(-sg),sg,-sg,abs(r)]
    elif kind=='monotone':
        p,q,u,v=x;unit(p);unit(q);y=flat(mm([[p,q],[1-p,1-q]],[[u],[v]]));a=abs(u)+abs(v);b=sum(map(abs,y));out=y+[a,b,2*a,2*b,a-b,2*(a-b)]
    elif kind=='stochastic':
        domain(len(x)==12);K=[x[i*3:i*3+3] for i in range(3)];v=x[9:];domain(all(z>=0 for z in x[:9]) and [sum(K[i][j] for i in range(3)) for j in range(3)]==[1]*3);y=flat(mm(K,[[z] for z in v]));out=[sum(K[i][j] for i in range(3)) for j in range(3)]+y+[sum(map(abs,v)),sum(map(abs,y))]+[sum(abs(K[i][j]*v[j]) for j in range(3)) for i in range(3)]
    elif kind=='channel':
        t,u,p,c=x;unit(p);domain(c*c<=p*(1-p));r,s=rotation(t);v,w=rotation(u);ks=[[[r,0],[0,0]],[[0,0],[s,0]],[[0,v],[0,0]],[[0,0],[0,w]]];rho=[[p,c],[c,1-p]]
        complete=[[sum(mm(tr(k),k)[i][j] for k in ks) for j in range(2)] for i in range(2)];res=[[sum(mm(mm(k,rho),tr(k))[i][j] for k in ks) for j in range(2)] for i in range(2)];K=[[r*r,v*v],[s*s,w*w]]
        out=flat(K)+[z for k in ks for z in flat(k)]+flat(complete)+flat(res)+flat(rho)+[p,0,0,1-p]+flat(mm([[0,1],[1,0]],K))
    elif kind=='firewall':
        score,defect,bound=x
        for z in x:integer(z,0,1000000)
        out=[score,defect,bound,int(defect==0),score+1,int(defect==0)]
    else:raise ValueError('unknown resource operation')
    return [str(Q(v)) for v in out]
def certify(kind,cases):return {'records':[{'input':v,'output':evaluate(kind,v)} for v in cases]}
