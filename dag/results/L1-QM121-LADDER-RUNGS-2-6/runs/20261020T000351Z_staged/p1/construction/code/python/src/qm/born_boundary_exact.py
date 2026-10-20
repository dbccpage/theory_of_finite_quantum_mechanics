"""Exact scoped Born-boundary operations. Imported structures remain explicit."""
from fractions import Fraction as Q
from itertools import product
from math import isqrt

def mul(A,B):return [sum(A[2*i+k]*B[2*k+j] for k in range(2)) for i in range(2) for j in range(2)]
def act(A,v):return [A[2*i]*v[0]+A[2*i+1]*v[1] for i in range(2)]
def evaluate(kind,values):
 x=list(map(Q,values));o=[]
 def emit(*v):o.extend(v)
 if kind=='isometry':
  k=int(x[0]);a,b=x[1:];assert x[0]==k and 0<=k<4
  f=[k//2,k%2];T=[Q(int(f[j]==i)) for i in range(2) for j in range(2)];G=[sum(T[2*k+i]*T[2*k+j] for k in range(2)) for i in range(2) for j in range(2)];v=act(T,[a,b]);emit(*T,*G,T[0]*T[3]-T[1]*T[2],int(f[0]!=f[1]),*v,a*a+b*b,sum(z*z for z in v))
 elif kind=='orthogonal':
  a,b,c,d=x;assert a*a+b*b==1
  P=[a*a,a*b,a*b,b*b];R=[b*b,-a*b,-a*b,a*a];u=(a*c+b*d)**2;v=(-b*c+a*d)**2;emit(*P,*R,*(P[i]+R[i] for i in range(4)),u,v,u+v,c*c+d*d,u*u+v*v,c**4+d**4,u*u+v*v-c**4-d**4)
 elif kind=='sqrt':
  if min(x)<0:return ['-1']
  M=sum(x)
  if not M:return ['0']
  p=[v/M for v in x];roots=[];ok=[]
  for z in p:
   a,b=isqrt(z.numerator),isqrt(z.denominator);yes=a*a==z.numerator and b*b==z.denominator;ok.append(int(yes));roots.append(Q(a,b) if yes else Q(0))
  emit(1,M,*p,*ok,*roots,int(all(ok)))
 elif kind=='phases':
  a,b=x;emit(a*a,b*b,*[(a+b*u)**2+(b*v)**2 for u,v in [(1,0),(0,1),(-1,0),(0,-1)]],*[(Q(3,5)*(a+b))**2+(Q(4,5)*(a+b))**2 for _ in range(1)],(a+b)**2,(a-b)**2,2*a*b)
 elif kind=='trace':
  v=x[:3];s,has,M=x[3:];assert has in (0,1) and M>=0
  W=sum(abs(z) for z in v)
  if not W or not s:return ['0']
  p=[abs(z)/W for z in v];scaled=[abs(s*z) for z in v];out=[M*z for z in p] if has else [Q(0)]*3
  emit(1,*(v[i] if i==j else Q(0) for i in range(3) for j in range(3)),*(abs(z) for z in v),W,sum(scaled),*p,*(z/sum(scaled) for z in scaled),has,*out,int(bool(has) and out==[abs(z) for z in v]))
 elif kind=='factor':
  p,q,r,s,a,b=x;assert all(0<=z<=1 for z in (p,q,r,s)) and a>=0 and b>=0 and a+b==1
  P=[p,1-q,1-p,q];R=[r,1-s,1-r,s];C=mul(P,R);v=act(C,[a,b]);via=act(P,act(R,[a,b]));emit(*P,*R,*C,*v,*via,v[0],0,0,v[1],2,0,0,2,1,0,0,1)
 elif kind=='branch':
  a,b=x;N=a*a+b*b
  if not N:return ['0']
  A=[a*a/N,a*b/N,a*b/N,b*b/N];B=[a*a/N,-a*b/N,-a*b/N,b*b/N];D=[a*a/N,0,0,b*b/N];R=[Q(3,5),Q(-4,5),Q(4,5),Q(3,5)];v=act(R,[a,b]);w=act(R,[a,-b]);emit(1,*A,*B,*D,*D,*(z*z/N for z in v),*(z*z/N for z in w),4*Q(3,5)*Q(-4,5)*a*b/N)
 elif kind=='normalize':
  w=x[:3];c=x[3];M=sum(w)
  if not M:return ['0']
  p=[v/M for v in w];scaled=[c*v for v in w];S=sum(scaled);q=[v/S for v in scaled] if S else [Q(0)]*3;emit(1,M,S,*p,*(v/sum(p) for v in p),int(S!=0),*q,int(S!=0 and p==q),int(c>0),int(min(w)>=0 and M>0))
 elif kind=='defect':
  a,b=x;D=abs(a)+abs(b)-abs(a+b);U=[a,0];V=[0,b];dis=sum(abs(z) for z in U)+sum(abs(z) for z in V)-sum(abs(U[i]+V[i]) for i in range(2));emit(abs(a),abs(b),D,abs(a)+abs(b),dis,int(a*b>=0),int(D==0),int(a*b<0))
 elif kind=='minkowski':
  a,b,p=x;n=int(p);assert min(a,b)>=0 and p==n and 2<=n<=6
  A=a**n;B=b**n;C=(a+b)**n;emit(A,B,C,A+B,C-A-B,int(C>A+B),int(a>0 and b>0))
 elif kind=='sparse':
  a,b,c,d=x;plus=[(a+b)**2,(c+d)**2];minus=[(a-b)**2,(c-d)**2];rs=(a*b==0 and c*d==0);mono=sum(z!=0 for z in (a,b))==1 and sum(z!=0 for z in (c,d))==1 and sum(z!=0 for z in (a,c))==1 and sum(z!=0 for z in (b,d))==1;det=a*d-b*c;rank=2 if det else int(any(x));emit(*plus,*minus,*(plus[i]-minus[i] for i in range(2)),int(rs),det,int(mono),rank)
 elif kind=='redundancy':
  w=x[:3];a=x[3:];assert min(w)>=0
  z=[a[2*i]**2+a[2*i+1]**2 for i in range(3)];W=sum(w);N=sum(z)
  if not W or not N:return ['0']
  p=[v/W for v in w];q=[v/N for v in z];emit(1,*z,W,N,int(z==w),*p,*q,int(p==q))
 elif kind=='shadow':
  A=x[:9];u=x[9:];ph=[(1,0),(0,1),(-1,0),(0,-1)];means=[Q(0)]*18;values=[]
  for gs in product(ph,repeat=3):
   B=[]
   for i in range(3):
    for j in range(3):B.extend([A[3*i+j]*(gs[i][0]*gs[j][0]+gs[i][1]*gs[j][1]),A[3*i+j]*(gs[i][1]*gs[j][0]-gs[i][0]*gs[j][1])])
   means=[a+b for a,b in zip(means,B)];values.append(sum(u[i]*B[2*(3*i+j)]*u[j] for i in range(3) for j in range(3)))
  means=[v/64 for v in means];diag=[A[3*i+j] if i==j else Q(0) for i in range(3) for j in range(3)];coherent=sum(u[i]*A[3*i+j]*u[j] for i in range(3) for j in range(3));emit(64,*means,*diag,*values,coherent,sum(values)/64,sum(u[i]**2*A[4*i] for i in range(3)),coherent)
 elif kind=='scope':
  if min(x)<0:return ['-1']
  W=sum(x);S=sum(z*z for z in x)
  if not W:return ['0']
  p=[z/W for z in x];q=[z*z/S for z in x];emit(1,*p,*q,p[0]+p[1],p[2],q[0]+q[1],q[2],sum(p),sum(q),*(a-b for a,b in zip(p,q)))
 elif kind=='gleason':
  a,b,c,u,v=x;assert a+c==1 and min(a,c)>=0 and a*c>=b*b
  if u*u+v*v!=1:return ['-1']
  f=lambda s,t:a*s*s+2*b*s*t+c*t*t
  E=f(u,v);F=f(-v,u);z=f(Q(3,5),Q(4,5));rec=(z-Q(9,25)*a-Q(16,25)*c)/Q(24,25);emit(1,E,F,E+F,a,c,z,rec,a,b,b,c,a*c-b*b)
 elif kind=='capacity':
  a,b,c,s=x;assert c*c+s*s==1;N=a*a+b*b
  if not N:return ['0']
  R=[c,-s,s,c];T=[c,s,-s,c];v=act(R,[a,b]);w=act(R,[a,-b]);emit(1,*R,*mul(T,R),*(z*z/N for z in v),*(z*z/N for z in w),a*a/N,b*b/N,sum(z*z for z in v),sum(z*z for z in w),N,-4*c*s*a*b/N)
 elif kind=='ladder':
  p,q,a,b,k=x;n=int(k);assert k==n and 0<=n<=4 and 0<=p<=1 and 0<=q<=1;N=a*a+b*b
  if not N:return ['0']
  T=[p,1-q,1-p,q];power=[Q(1),Q(0),Q(0),Q(1)]
  for _ in range(n):power=mul(power,T)
  terms=[];P=[Q(0)]*4
  for start in range(2):
   for code in range(2**n):
    state=start;w=Q(1)
    for step in range(n):dest=(code>>step)&1;w*=T[2*dest+state];state=dest
    terms.append(w);P[2*state+start]+=w
  v=act(power,[a*a/N,b*b/N]);emit(1,*power,*P,*terms,*v,(a+b)**2/(2*N),(a-b)**2/(2*N),Q(1,2),Q(1,2),a*b/N)
 elif kind=='pairing':
  a,b,c,d=x;A=a*a+b*b;B=c*c+d*d;W=A+B;S=A*A+B*B
  if not W:return ['0']
  H=[(a+c)**2+(b+d)**2,(a-c)**2+(b-d)**2];R=[(a-d)**2+(b+c)**2,(a+d)**2+(b-c)**2];emit(1,A,B,A*A,B*B,B,A,A/W,B/W,A*A/S,B*B/S,W,S,*H,*R,sum(H),sum(R),sum(z*z for z in H),sum(z*z for z in R),sum(z*z for z in H)-sum(z*z for z in R))
 elif kind=='selector':
  n=int(x[0]);assert x[0]==n and n in (2,3,4);T=[Q(int(i==(j+1)%n)) for i in range(n) for j in range(n)];square=[sum(T[n*i+k]*T[n*k+j] for k in range(n)) for i in range(n) for j in range(n)];I=[Q(int(i==j)) for i in range(n) for j in range(n)];emit(*T,*square,*I,n,int(square==I),int(n>2))
 elif kind=='finish':
  a,b=x;N=a*a+b*b;E=[[Q(int(i==s and j==t)) for i in range(2) for j in range(2)] for s in range(2) for t in range(2)];products=[z for A in E for B in E for z in mul(A,B)];U=mul(E[1],E[2]);V=mul(E[2],E[1]);emit(N,int(N==1),int(N!=0),a/N if N else 0,-b/N if N else 0,*products,*(u-v for u,v in zip(U,V)))
 else:raise ValueError('Unknown declared operation')
 return [str(Q(v)) for v in o]
def certify(kind,cases):return {'records':[{'input':v,'output':evaluate(kind,v)} for v in cases]}
