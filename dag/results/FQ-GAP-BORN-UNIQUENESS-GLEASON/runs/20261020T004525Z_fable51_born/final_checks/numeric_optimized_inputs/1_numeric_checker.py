"""Independent exact rational predicates for the public 2x2 symmetric controls."""
from fractions import Fraction as Q
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent
def require(v,m):
 if not v:raise ValueError(m)
def pairs(items):
 d={}
 for k,v in items:require(k not in d,'duplicate key');d[k]=v
 return d
def forbidden(v):raise ValueError('nonexact JSON')
def load(p):return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_float=forbidden,parse_constant=forbidden)
def rat(s):
 require(type(s) is str,'rational must be string');q=Q(s);require(str(q)==s,'noncanonical rational');return q
def matrix(v):require(type(v) is list and len(v)==3,'symmetric matrix wire');return tuple(map(rat,v))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def psd(a):return a[0]>=0 and a[2]>=0 and a[0]*a[2]-a[1]**2>=0
def effect(a):return psd(a) and psd(sub((Q(1),Q(0),Q(1)),a))
def trace(a,r):return a[0]*r[0]+2*a[1]*r[1]+a[2]*r[2]
def binary(ray):
 x,y=map(rat,ray);require(x!=0 or y!=0,'zero ray')
 return Q(1 if x*y>0 else 0 if x*y<0 else 1 if y==0 else 0)
def evaluate(c):
 a,b=matrix(c['a']),matrix(c['b']);e=rat(c['epsilon']);require(0<=e<=1,'epsilon domain')
 d=sub(a,b);u=(e,Q(0),e);v=c['valuation']
 if v['kind']=='binary_ray_restriction':va,vb=binary(v['a_ray']),binary(v['b_ray'])
 else:
  require(v['kind']=='trace','unknown valuation');rho=matrix(v['rho']);va,vb=trace(a,rho),trace(b,rho)
 return dict(id=c['id'],a_effect=effect(a),b_effect=effect(b),lower_psd=psd(add(d,u)),upper_psd=psd(sub(u,d)),v_a=str(va),v_b=str(vb),value_bound=-e<=va-vb<=e)
def expected():return [evaluate(c) for c in load(R/'public_input.json')['cases']]
def check(records):
 e=expected();require(type(records) is list and len(records)==len(e),'record count')
 for a,b in zip(records,e):
  require(type(a) is dict and set(a)==set(b),'record keys')
  for k in b:require(type(a[k]) is type(b[k]) and a[k]==b[k],'wrong field '+k)
 return {'records_checked':len(e),'scope':'Exact supplied symmetric rational matrices and declared valuation controls only.'}
def self_test():
 require(psd((Q(0),Q(0),Q(1))) and psd((Q(1),Q(1),Q(1))),'valid PSD controls')
 require(not psd((Q(1),Q(2),Q(1))) and not psd((Q(0),Q(1),Q(1))),'indefinite controls')
 controls=expected();rejected=0
 import copy
 for i,row in enumerate(controls):
  for k,v in row.items():
   m=copy.deepcopy(controls);m[i][k]=not v if type(v) is bool else str(rat(v)+1) if k in ('v_a','v_b') else v+'_wrong'
   try:check(m)
   except ValueError:rejected+=1
   else:raise ValueError('mutant accepted')
  for k,v in row.items():
   if type(v) is bool:
    m=copy.deepcopy(controls);m[i][k]=int(v)
    try:check(m)
    except ValueError:rejected+=1
    else:raise ValueError('bool/int alias accepted')
 return {'positive_and_indefinite_psd_controls':'passed','field_and_primitive_mutants_rejected':rejected}
if __name__=='__main__':
 if len(sys.argv)>1:print(json.dumps(check(load(sys.argv[1])['candidate_certificate']['numeric_records'])))
 else:print(json.dumps({'controls':expected(),'guards':self_test()},indent=2))