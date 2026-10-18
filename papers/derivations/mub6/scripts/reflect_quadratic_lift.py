"""Validate the quadratic-lift JSONL and format its rows and bounds as Lean literals.

This formatter does not prove polynomial equivalence or infeasibility. Compile
its generated module to check the literals against the defining coefficients.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--coefficients',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()

def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

raw=args.coefficients
records=[json.loads(line)for line in raw.read_text(encoding='utf-8-sig').splitlines()]
header,rows,tail=records[0],records[1:-1],records[-1]
require(header['schema']=='mub6.quadratic_lift.coefficients.v1','Wrong schema')
require(header['variable_count']==386 and header['equation_count']==648,'Wrong dimensions')
require(header['coordinate_codes']==list(range(386)) and header['equation_codes']==list(range(648)),'Wrong numbering')
expected_bounds=[['-1/1','1/1']]*170+[ ['-3/1','3/1'] ]*216
require(header['coordinate_bounds']==expected_bounds,'Wrong box')
require(header['determinant_inequality'] is None,'Wrong model')
require(len(rows)==648 and [r['id']for r in rows]==list(range(648)),'Rows missing or duplicated')
counts=[]
zeros=[]
for r in rows:
    require(r['kind']=='equation' and r['degree_bound']==2,'Wrong row header')
    ts=r['terms']; counts.append(len(ts))
    require(r['term_count']==len(ts),'Wrong row count')
    require(len(r['probe_values'])==4,'Missing probes')
    keys=[]
    for q,vs in ts:
        require(re.fullmatch(r'-?\d+/[1-9]\d*',q) is not None,'Bad rational')
        require(int(q.split('/')[0])!=0,'Zero coefficient')
        require(len(vs)<=2 and all(type(v)is int and 0<=v<386 for v in vs),'Bad variable or degree')
        require(vs==sorted(vs),'Unsorted factors')
        keys.append(vs)
    require(keys==sorted(keys) and len({tuple(k)for k in keys})==len(keys),'Duplicate or unordered monomial')
    if not ts:
        zeros.append(r['id'])
require(tail==dict(kind='complete',equations=648,total_terms=sum(counts),maximum_terms=max(counts)),'Wrong completion')
out=raw
summary=dict(source_sha256=sha(raw),bytes=raw.stat().st_size,equations=648,variables=386,
             total_terms=sum(counts),maximum_terms=max(counts),zero_rows=zeros)

def rat(q):
    n,d=q.split('/')
    return f'({n}/{d} : Rat)'
def terms(ts):
    return '['+', '.join('('+rat(q)+', ['+', '.join(map(str,vs))+'])'for q,vs in ts)+']'

source='''import MubQuadraticLiftCodedSystem

/-!
# Literal coefficient table for the quadratic lift

AuthorityEffect: None. Generated from the native JSON-lines coefficient table.
The kernel equality checks these literal rows against all defining polynomials.
JSON parsing and file custody are recorded separately in the receipt.
Source JSON SHA-256: '''+sha(out)+'''
-/
namespace MUB.QuadraticLiftTable
open QuadraticLiftIndices QuadraticLiftCoefficients QuadraticLiftCodedSystem
open BoundedTermCollection (Term listPolynomial)

set_option maxRecDepth 10000
set_option maxHeartbeats 20000000

'''
chunks=[]
for start in range(0,len(rows),18):
    name=f'rows_{start // 18}'
    chunks.append(name)
    source+=f'def {name} : List (Nat × List Term) := [\n'
    source+=',\n'.join('  ('+str(r['id'])+', '+terms(r['terms'])+')'for r in rows[start:start+18])+'\n]\n\n'
source+='def rows : List (Nat × List Term) := '+ ' ++ '.join(chunks)+'\n\n'
source+='''theorem rows_match : equations.map (fun e => (equationCode e,equationCoefficients e)) = rows := by
  decide +kernel

theorem row_ids : rows.map Prod.fst = List.range 648 := by
  rw [← rows_match, List.map_map]
  exact equation_codes

theorem row_count : rows.length = 648 := by
  have h := congrArg List.length row_ids
  simpa using h

noncomputable def TableSolution (x : Fin 386 → ℝ) : Prop :=
  ∀ row ∈ rows, codedRealEval x (listPolynomial row.2) = 0

theorem tableSolution_iff (x : Fin 386 → ℝ) : TableSolution x ↔ CodedSolution x := by
  rw [TableSolution, ← rows_match]
  simp only [List.forall_mem_map, CodedSolution]

theorem exists_quartet_iff_table :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ x, TableSolution x ∧ CodedBox x := by
  rw [exists_quartet_iff_coded]
  simp_rw [tableSolution_iff]

def bounds : List (Rat × Rat) := [
'''
source+=',\n'.join('  ('+rat(a)+', '+rat(b)+')'for a,b in expected_bounds)+'\n]\n\n'
source+='''theorem bounds_match : (List.range 386).map (fun i => (-codeRadius i,codeRadius i)) = bounds := by
  decide +kernel

#print axioms rows_match
#print axioms row_ids
#print axioms row_count
#print axioms tableSolution_iff
#print axioms exists_quartet_iff_table
#print axioms bounds_match
end MUB.QuadraticLiftTable
'''
p=args.output
p.write_text(source,encoding='utf-8',newline='\n')
print(json.dumps(summary))
