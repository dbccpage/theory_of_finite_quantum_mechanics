"""Independent domain equations; imports neither Python nor Rust producer."""
from fractions import Fraction as Q
from itertools import product
from math import isqrt
from exact_json import require,rational
from review_exact_json import audit_bound

def eq(a,b):require(a==b,'G3_WITNESS:independent_equations')
def verify(kind,values,raw):
 x=list(map(rational,values));y=list(map(rational,raw))
 if kind=='isometry':
  k=int(x[0]);require(x[0]==k and k in range(4),'G1_SCHEMA:map_code');a,b=x[1:];f=(k//2,k%2);T=[int(f[j]==i) for i,j in product(range(2),repeat=2)];G=[int(f[i]==f[j]) for i,j in product(range(2),repeat=2)];v=[sum((a,b)[j] for j in range(2) if f[j]==i) for i in range(2)];eq(y,T+G+[T[0]*T[3]-T[1]*T[2],int(len(set(f))==2)]+v+[a*a+b*b,sum(z*z for z in v)])
 elif kind=='orthogonal':
  a,b,c,d=x;eq(a*a+b*b,1);P=[a*a,a*b,a*b,b*b];R=[b*b,-a*b,-a*b,a*a];A=(a*c+b*d)**2;B=(a*d-b*c)**2;eq(y,P+R+[1,0,0,1]+[A,B,c*c+d*d,c*c+d*d,A*A+B*B,c**4+d**4,A*A+B*B-c**4-d**4]);eq(A+B,c*c+d*d)
 elif kind=='sqrt':
  if any(v<0 for v in x):eq(y,[-1]);return
  W=sum(x)
  if not W:eq(y,[0]);return
  p=[z/W for z in x];flags=[];roots=[]
  for z in p:
   u=isqrt(z.numerator);v=isqrt(z.denominator);ok=Q(u*u,v*v)==z;flags.append(int(ok));roots.append(Q(u,v) if ok else 0)
  eq(y,[1,W]+p+flags+roots+[int(all(flags))])
 elif kind=='phases':
  a,b=x;E=a*a+b*b;eq(y,[a*a,b*b,E+2*a*b,E,E-2*a*b,E,E+2*a*b,E+2*a*b,E-2*a*b,2*a*b])
 elif kind=='trace':
  v=x[:3];s,tag,M=x[3:];require(tag in (0,1) and M>=0,'G1_SCHEMA:mass_tag');W=sum(abs(z) for z in v)
  if not W or not s:eq(y,[0]);return
  p=[abs(z)/W for z in v];D=[v[i] if i==j else 0 for i,j in product(range(3),repeat=2)];out=[M*z for z in p] if tag else [0]*3;eq(y,[1]+D+[abs(z) for z in v]+[W,abs(s)*W]+p+p+[tag]+out+[int(bool(tag) and M==W)])
 elif kind=='factor':
  p,q,r,s,a,b=x;require(all(0<=z<=1 for z in (p,q,r,s)) and min(a,b)>=0 and a+b==1,'G1_SCHEMA:stochastic_packet');P=[p,1-q,1-p,q];R=[r,1-s,1-r,s];C=[p*r+(1-q)*(1-r),p*(1-s)+(1-q)*s,(1-p)*r+q*(1-r),(1-p)*(1-s)+q*s];v=[C[0]*a+C[1]*b,C[2]*a+C[3]*b];eq(y,P+R+C+v+v+[v[0],0,0,v[1],2,0,0,2,1,0,0,1]);eq(v[0]+v[1],1)
 elif kind=='branch':
  a,b=x;N=a*a+b*b
  if not N:eq(y,[0]);return
  D=[a*a/N,0,0,b*b/N];A=[a*a/N,a*b/N,a*b/N,b*b/N];B=[a*a/N,-a*b/N,-a*b/N,b*b/N];c=Q(3,5);s=Q(4,5);v=[(c*a-s*b)**2/N,(s*a+c*b)**2/N];w=[(c*a+s*b)**2/N,(s*a-c*b)**2/N];eq(y,[1]+A+B+D+D+v+w+[-4*c*s*a*b/N]);eq(v[0]-w[0],-4*c*s*a*b/N)
 elif kind=='normalize':
  w=x[:3];c=x[3];M=sum(w)
  if not M:eq(y,[0]);return
  p=[z/M for z in w];S=c*M;q=p if S else [0]*3;eq(y,[1,M,S]+p+p+[int(S!=0)]+q+[int(S!=0),int(c>0),int(min(w)>=0 and M>0)])
 elif kind=='defect':
  a,b=x;D=abs(a)+abs(b)-abs(a+b);eq(y,[abs(a),abs(b),D,abs(a)+abs(b),0,int(a*b>=0),int(a*b>=0),int(a*b<0)]);eq(D==0,a*b>=0)
 elif kind=='minkowski':
  a,b,p=x;k=int(p);require(p==k and 2<=k<=6 and min(a,b)>=0,'G1_SCHEMA:positive_natural_power');A=a**k;B=b**k;C=(a+b)**k;eq(y,[A,B,C,A+B,C-A-B,int(a*b>0),int(a*b>0)]);eq(C>A+B,a*b>0)
 elif kind=='sparse':
  a,b,c,d=x;det=a*d-b*c;rs=(a==0 or b==0) and (c==0 or d==0);mono=(a!=0 and d!=0 and b==c==0) or (b!=0 and c!=0 and a==d==0);rank=2 if det else int(any(x));eq(y,[(a+b)**2,(c+d)**2,(a-b)**2,(c-d)**2,4*a*b,4*c*d,int(rs),det,int(mono),rank])
 elif kind=='redundancy':
  w=x[:3];g=x[3:];require(min(w)>=0,'G1_SCHEMA:weights');z=[g[2*i]**2+g[2*i+1]**2 for i in range(3)];W=sum(w);N=sum(z)
  if not W or not N:eq(y,[0]);return
  p=[v/W for v in w];q=[v/N for v in z];eq(y,[1]+z+[W,N,int(w==z)]+p+q+[int(all(z[i]*W==w[i]*N for i in range(3)))])
 elif kind=='shadow':
  A=x[:9];u=x[9:];ph=[(1,0),(0,1),(-1,0),(0,-1)];diag=[A[3*i+j] if i==j else 0 for i,j in product(range(3),repeat=2)];mean=[z for i,j in product(range(3),repeat=2) for z in (A[3*i+j] if i==j else Q(0),Q(0))];vals=[]
  # Pairwise cosine dot products independently expand the scalar readout.
  for codes in product(range(4),repeat=3):
   vals.append(sum(u[i]*u[j]*A[3*i+j]*(ph[codes[i]][0]*ph[codes[j]][0]+ph[codes[i]][1]*ph[codes[j]][1]) for i,j in product(range(3),repeat=2)))
  coherent=sum(u[i]*A[3*i+j]*u[j] for i,j in product(range(3),repeat=2));pair=sum(u[i]*u[i]*A[4*i] for i in range(3));eq(sum(vals)/64,pair);eq(y,[64]+mean+diag+vals+[coherent,pair,pair,coherent])
 elif kind=='scope':
  if min(x)<0:eq(y,[-1]);return
  W=sum(x);S=sum(z*z for z in x)
  if not W:eq(y,[0]);return
  p=[z/W for z in x];q=[z*z/S for z in x];eq(y,[1]+p+q+[p[0]+p[1],p[2],q[0]+q[1],q[2],1,1]+[p[i]-q[i] for i in range(3)])
 elif kind=='gleason':
  a,b,c,u,v=x;require(a+c==1 and min(a,c)>=0 and a*c>=b*b,'G1_SCHEMA:quadratic_density_ansatz')
  if u*u+v*v!=1:eq(y,[-1]);return
  E=a*u*u+2*b*u*v+c*v*v;F=1-E;z=(9*a+24*b+16*c)/25;eq(y,[1,E,F,1,a,c,z,b,a,b,b,c,a*c-b*b]);eq((-v)**2*a+2*b*(-v)*u+c*u*u,F)
 elif kind=='capacity':
  a,b,c,s=x;eq(c*c+s*s,1);N=a*a+b*b
  if not N:eq(y,[0]);return
  plus=[(c*a-s*b)**2/N,(s*a+c*b)**2/N];minus=[(c*a+s*b)**2/N,(s*a-c*b)**2/N];eq(y,[1,c,-s,s,c,1,0,0,1]+plus+minus+[a*a/N,b*b/N,N,N,N,-4*c*s*a*b/N])
 elif kind=='ladder':
  p,q,a,b,k=x;n=int(k);require(k==n and 0<=n<=4 and 0<=p<=1 and 0<=q<=1,'G1_SCHEMA:stochastic_path_bound');N=a*a+b*b
  if not N:eq(y,[0]);return
  T=[[p,1-q],[1-p,q]];P=[[Q(1),Q(0)],[Q(0),Q(1)]]
  for _ in range(n):P=[[sum(T[i][s]*P[s][j] for s in range(2)) for j in range(2)] for i in range(2)]
  terms=[];sums=[[Q(0)]*2 for _ in range(2)]
  for start in range(2):
   for code in range(2**n):
    path=[start]+[(code>>j)&1 for j in range(n)];weight=Q(1)
    for z in range(n):weight*=T[path[z+1]][path[z]]
    terms.append(weight);sums[path[-1]][start]+=weight
  eq(P,sums);out=[sum(P[i][j]*[a*a/N,b*b/N][j] for j in range(2)) for i in range(2)];flat=[v for row in P for v in row];eq(y,[1]+flat+flat+terms+out+[(a+b)**2/(2*N),(a-b)**2/(2*N),Q(1,2),Q(1,2),a*b/N])
 elif kind=='pairing':
  a,b,c,d=x;A=a*a+b*b;B=c*c+d*d;W=A+B;S=A*A+B*B
  if not W:eq(y,[0]);return
  cross_real=a*c+b*d;cross_im=b*c-a*d;H=[W+2*cross_real,W-2*cross_real];R=[W+2*cross_im,W-2*cross_im];eq(y,[1,A,B,A*A,B*B,B,A,A/W,B/W,A*A/S,B*B/S,W,S]+H+R+[2*W,2*W,H[0]**2+H[1]**2,R[0]**2+R[1]**2,8*(cross_real**2-cross_im**2)])
 elif kind=='selector':
  n=int(x[0]);require(x[0]==n and n in (2,3,4),'G1_SCHEMA:regular_representation');T=[int((i-j)%n==1) for i,j in product(range(n),repeat=2)];S=[int((i-j)%n==2%n) for i,j in product(range(n),repeat=2)];I=[int(i==j) for i,j in product(range(n),repeat=2)];eq(y,T+S+I+[n,int(n==2),int(n!=2)])
 elif kind=='finish':
  a,b=x;N=a*a+b*b;table=[]
  for i,j,k,l in product(range(2),repeat=4):table += [int(j==k and s==i and t==l) for s,t in product(range(2),repeat=2)]
  eq(y,[N,int(N==1),int(N>0),a/N if N else 0,-b/N if N else 0]+table+[1,0,0,-1])
 else:raise ValueError('G1_SCHEMA:unknown_kind')

def check(request,candidate,task,config,root):
 _,c,p=audit_bound(request,candidate,task,config);require(set(c['data'])=={'records'} and len(c['data']['records'])==len(p['cases']),'G1_SCHEMA:coverage')
 for rec,v in zip(c['data']['records'],p['cases']):require(rec['input']==v,'G5_SCOPE:input_identity');verify(p['kind'],v,rec['output'])
 return {'records_checked':len(p['cases']),'scope':'Exact finite arrays and separately scoped literal Lean signatures; no historical labels, imported theorems or full operad coherence admitted.'}
