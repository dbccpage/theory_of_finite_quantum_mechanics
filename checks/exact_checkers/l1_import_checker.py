"""Independent equations and exhaustive finite predicates; imports neither producer."""
from fractions import Fraction as Q
from itertools import product, permutations
from exact_json import require, rational
from review_exact_json import audit_bound

def eq(a,b):require(a==b,'G3_WITNESS:independent_equations')
def verify(kind,values,raw):
 x=list(map(rational,values));y=list(map(rational,raw))
 if kind=='chain':
  a,b,c,f=x;B=[[-1,1,0],[0,-1,1],[1,0,-1]];v=[a,b,c];d=[sum(B[i][j]*v[j] for j in range(3)) for i in range(3)];q=[sum([1,1,1+f][i]*B[i][j] for i in range(3)) for j in range(3)];eq(y,q+d+[sum([1,1,1+f][i]*d[i] for i in range(3)),int(not any(q))])
 elif kind=='kkt':
  v,w,h,z=[x[k:k+3] for k in (0,3,6,9)];B=[[-1,1,0],[0,-1,1],[1,0,-1]];r=[v[i]-sum(B[i][j]*h[j] for j in range(3)) for i in range(3)];div=[sum(z[i]*B[i][j] for i in range(3)) for j in range(3)];cap=[w[i]-abs(z[i]) for i in range(3)];s=[w[i]*abs(r[i])-z[i]*r[i] for i in range(3)];p=sum(w[i]*abs(r[i]) for i in range(3));d=sum(z[i]*v[i] for i in range(3));ok=min(w)>0 and min(cap)>=0 and all(t==0 for t in div) and p==d;eq(y,r+div+cap+s+[p,d,p-d,int(ok)])
 elif kind in ('edge','gauge','observer'):
  a,b,p,q=x;require(min(p,q)>=0,'G1_SCHEMA:weights');F=lambda u,v:p*abs(u)+q*abs(v);base=F(a,b);swap=F(b,a)
  if kind=='edge':eq(y,[F(a,0),F(0,b),base,swap,swap-base,abs(a)+abs(b),max(abs(a),abs(b)),min(abs(a),abs(b))])
  elif kind=='gauge':
   orbit=[F((b if k else a)*s,(a if k else b)*t) for k in (0,1) for s in (-1,1) for t in (-1,1)];eq(y,orbit+[a*a+b*b,a*a+b*b,F(3,4),F(5,0),F(3,4)-F(5,0)])
  else:eq(y,[base,F(a,0)+F(0,b),min(abs(a),abs(b)),2*(a*a+b*b),swap-base,F(0,b),F(a,0)])
 elif kind in ('quotient','window'):
  v=x[:3];w=x[3:6];g=x[6:9];require(min(w)>0,'G1_SCHEMA:positive_weights')
  if kind=='window' and x[9]!=0:eq(y,[0]);return
  k=min(range(3),key=lambda j:(w[j],j));R=[sum(v) if j==k else Q(0) for j in range(3)];H=[Q(0),v[0]-R[0],-v[2]+R[2]];eq([v[0]-H[1],v[1]-H[2]+H[1],v[2]+H[2]],R);S=[v[j]+g[(j+1)%3]-g[j] for j in range(3)];P=min(w)*abs(sum(v));out=[1,k]+R+H+[P]+S+[min(w)*abs(sum(S))]
  if kind=='window':out += [abs(sum(v)),int(P>0),Q(1)/min(w) if P else Q(0)]
  eq(y,out)
 elif kind=='replica':
  a,b,k=x;require(k.denominator==1 and 0<=k<=8,'G1_SCHEMA:replicas');L=abs(a)+abs(b);E=a*a+b*b;eq(y,[k*L,k*E,k*L,k*E,k*k*E,k*k*E])
 elif kind=='mass':
  if any(v<0 for v in x):eq(y,[-1]);return
  m=sum(x)
  if m==0:eq(y,[0]);return
  p=[v/m for v in x];eq(y,[1,m]+p+[p[0]+p[1],p[2]+p[3],1]);eq(sum(p),1)
 elif kind=='circle':
  n=int(x[0]);require(x[0]==n and n in (2,3,4),'G1_SCHEMA:cyclic_group');table=[(i+j)%n for i,j in product(range(n),repeat=2)];e=[int(table[k*n+k]==0) for k in range(n)];eq(y,e+table+[int(sum(e)==n),4,0])
 elif kind=='gauss':
  a,b=x;require(all(v.denominator==1 for v in x),'G1_SCHEMA:gaussian_integer');N=a*a+b*b;out=[N,int(N==1),int(N>0),a/N if N else 0,-b/N if N else 0]+[k*k-2 for k in range(-3,4)];eq(y,out)
  if N: eq(a*out[3]-b*out[4],1);eq(a*out[4]+b*out[3],0)
 elif kind=='complex':
  a,b,c,d=x;N=a*a+b*b;M=c*c+d*d;u=a*c-b*d;v=a*d+b*c;eq(y,[N,M,u,v,u*u+v*v,N*M,int(N>0),a/N if N else 0,-b/N if N else 0]);eq(u*u+v*v,N*M)
 elif kind=='time':
  s=x[0];require(s in (-1,1),'G1_SCHEMA:branch');maps=list(product(range(2),repeat=2));eq(y[:9],[z for f in maps for z in (f[f[0]],f[f[1]])]+[0]);eq(len(y),33)
  U=[complex_pair for complex_pair in zip(y[9:17:2],y[10:17:2])];eq(U,[(Q(1,2),s/2),(Q(1,2),-s/2),(Q(1,2),-s/2),(Q(1,2),s/2)])
  eq(y[17:25],[0,0,1,0,1,0,0,0]);eq(y[25:],[1,0,0,0,0,0,1,0])
  for i,j in product(range(2),repeat=2):
   re=sum(U[2*i+k][0]*U[2*k+j][0]-U[2*i+k][1]*U[2*k+j][1] for k in range(2));im=sum(U[2*i+k][0]*U[2*k+j][1]+U[2*i+k][1]*U[2*k+j][0] for k in range(2));eq([re,im],y[17+4*i+2*j:19+4*i+2*j])
 elif kind=='hilbert':
  n=int(x[0]);require(x[0]==n and 0<=n<=8,'G1_SCHEMA:truncation');coords=[Q(1,2**k) for k in range(1,n+1)];norm=Q(1,3)-Q(1,3*4**n);eq(y,coords+[norm,Q(1,3*4**n),Q(1,4**(n+1)),Q(1,3),1]);eq(sum(v*v for v in coords),norm)
 elif kind=='dilation':
  a,b,d=x;require(a+d==1 and min(a,d)>=0 and a*d>=b*b,'G1_SCHEMA:density2');ps=[]
  for p in permutations(range(4)):
   # two initialized ancilla inputs must leave system zero, preserving distinct records.
   if set((p[0],p[2]))=={0,1}:ps.append(p)
  expected=[len(ps)]
  for p in ps:expected += list(p)+[p.index(i) for i in range(4)]
  J=[[int(i==j and i%2==0) for j in range(4)] for i in range(4)];partial=[sum(J[2*i+k][2*j+k] for k in range(2)) for i,j in product(range(2),repeat=2)];eq(y,expected+[z for r in J for z in r]+partial+[1,0,0,0])
 elif kind=='gleason':
  a,b=x;z=a*a+b*b;had=[(a+b)**2,(a-b)**2];rot=[z,z];eq(y,[a*a,b*b,z,z]+had+rot+[sum(had),sum(rot),sum(t*t for t in had),sum(t*t for t in rot),8*a*a*b*b]);eq(sum(had),sum(rot))
 elif kind=='tensor':
  a,b,c,d=x;t=[u*v for u in (a,b) for v in (c,d)];dump=[a*(c+d),0,b*(c+d),0];eq(y,t+dump+[t[i]-dump[i] for i in range(4)]+[(a*a+b*b)*(c*c+d*d),sum(z*z for z in t)])
 elif kind=='lift':
  a,b,c,d=x;N=a*a+b*b;M=c*c+d*d
  if N==0 or M==0:eq(y,[0]);return
  R=[u*v/N for u,v in product((a,b),repeat=2)];S=[u*v/M for u,v in product((c,d),repeat=2)];over=sum(R[2*i+j]*S[2*j+i] for i,j in product(range(2),repeat=2));r=[a*abs(a),b*abs(b)];z=[c*abs(c),d*abs(d)];slack=sum(abs(r[i]*z[i])-r[i]*z[i] for i in range(2));faith=all(r[i]==0 or z[i]!=0 for i in range(2));eq(y,[1,N,M]+R+S+[over,1-over,int(slack==0),int(faith),int(over>0)]);require(0<=over<=1,'G3_WITNESS:cauchy_gap')
  if slack==0 and faith:require(over>0,'G3_WITNESS:strictness_needs_positive_capacity')
 elif kind=='average':
  a,b=x;cross=[1,0,-1,0];vals=[a*a+b*b+2*a*b*cross[(i-j)%4] for i,j in product(range(4),repeat=2)];corr=[(a+b)**2]*4;eq(y,vals+corr+[a*a+b*b,(a+b)**2,a*a+b*b,2*a*b]);eq(sum(vals)/16,a*a+b*b)
 elif kind=='gram':
  a,b,c,d=x;eq(y,[a*c+b*d,a*c+2*b*d,2*a*c+3*b*d,a*a+b*b,a*a+2*b*b,2*a*a+3*b*b,b*d,b*b])
 else:raise ValueError('G1_SCHEMA:unknown_operation')

def check(request,candidate,task,config,root):
 _,c,p=audit_bound(request,candidate,task,config);require(set(c['data'])=={'records'} and len(c['data']['records'])==len(p['cases']),'G1_SCHEMA:coverage')
 for record,v in zip(c['data']['records'],p['cases']):require(record['input']==v,'G5_SCOPE:input_identity');verify(p['kind'],v,record['output'])
 return {'records_checked':len(p['cases']),'scope':'Exact declared finite controls and separately scoped named Lean statements; all original imports and bridges remain explicit.'}
