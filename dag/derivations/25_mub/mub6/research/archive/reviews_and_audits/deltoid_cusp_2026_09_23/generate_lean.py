"""Regenerate LiteralCuspCertificate.lean from the replayed rational certificate.

AuthorityEffect: None.
stated region only; mints no authority

Uses the Python standard library and the repository's exact rational verifier.
Lean subsequently checks the emitted polynomial identity in its kernel.
"""
import argparse,json,math,sys
from fractions import Fraction as Q
from pathlib import Path

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=root/'lean4'/'012_mutually_unbiased_bases'/'MUB'/'LiteralCuspCertificate.lean')
options=parser.parse_args()
sys.path.insert(0,str(root/'code'))
from mub_verify.deltoid_cusp_input import audit_receipt, verify_certificate
receipt_dir=root/'research'/'deltoid_cusp_2026_09_23'
certificate=json.loads((receipt_dir/'literal_certificate.json').read_text(encoding='utf-8'))
inputs=json.loads((receipt_dir/'input_audit.json').read_text(encoding='utf-8'))
verify_certificate(certificate)
if inputs['sources'] != json.loads(json.dumps(audit_receipt()['sources'])):
    raise ValueError('input audit differs from the canonical exact source polynomials')
variables=certificate['variable_order']; args=' '.join(variables)
denominator=math.lcm(*(term['coefficient'][1] for p in certificate['multipliers'] for term in p['terms']))
def poly(terms,scale=1):
    chunks=[]
    for term in terms:
        c=Q(*term['coefficient'])*scale
        if not c: continue
        if c.denominator != 1:
            raise ValueError('Lean coefficient emission requires an integer after denominator clearing')
        factors=[]
        if c.numerator != 1 or not any(term['powers']):
            factors.append(f'({c.numerator} : ℝ)' if c<0 else str(c.numerator))
        factors += [v if n==1 else f'{v}^{n}' for v,n in zip(variables,term['powers']) if n]
        chunks.append(' * '.join(factors))
    return '\n    + '.join(chunks) or '0'

parts=['import Mathlib.Data.Real.Basic','import Mathlib.Data.Fin.VecNotation','import Mathlib.Tactic.Ring','import Mathlib.Tactic.NormNum',
'''/-!
# Exact degree-four refutation for the literal input equations

AuthorityEffect: None.
stated region only; mints no authority

The matrix supplied in the prompt fails Hadamard orthogonality. These declarations
refer only to its literal seventeen equations, not a corrected cusp matrix.
The rational source and multiplier data are in
`research/deltoid_cusp_2026_09_23/{input_audit,literal_certificate}.json`.
Coordinates are ordered x2,t2,...,x6,t6 with y_k = sqrt(3)*t_k.
All multipliers have degree at most two. Their common denominator is cleared.
-/''',
'namespace MUB6.LiteralCuspCertificate',
'set_option maxRecDepth 100000',
'set_option maxHeartbeats 8000000',
'set_option linter.unusedVariables false']
for i,p in enumerate(inputs['sources']):
    parts.append(f'/-- Literal canonical residue `{p["id"]}`. -/\ndef source{i} ({args} : ℝ) : ℝ :=\n    {poly(p["terms"])}')
parts.append(f'def sources ({args} : ℝ) : Fin 17 → ℝ :=\n  !['+',\n    '.join(f'source{i} {args}' for i in range(17))+']')
for i,p in enumerate(certificate['multipliers']):
    parts.append(f'/-- Denominator-cleared exact multiplier for `{p["id"]}`. -/\ndef multiplier{i} ({args} : ℝ) : ℝ :=\n    {poly(p["terms"],denominator)}')
identity='\n    + '.join(f'multiplier{i} {args} * source{i} {args}' for i in range(17))
parts.append(f'''/-- Kernel-checked, denominator-cleared literal Nullstellensatz identity. -/
theorem identity ({args} : ℝ) :
    {identity} = -({denominator} : ℝ) := by
  unfold {' '.join('source'+str(i) for i in range(17))} {' '.join('multiplier'+str(i) for i in range(17))}
  ring''')
parts.append(f'''/-- The seventeen literal canonical residues cannot all vanish over ℝ. -/
theorem no_common_zero ({args} : ℝ)
    '''+'\n    '.join(f'(h{i} : source{i} {args} = 0)' for i in range(17))+f''' : False := by
  have hid := identity {args}
  rw [{', '.join('h'+str(i) for i in range(17))}] at hid
  norm_num at hid''')
parts.append(f'''/-- Vector-indexed form of the literal no-common-zero theorem. -/
theorem no_common_zero_sources ({args} : ℝ)
    (h : ∀ i, sources {args} i = 0) : False := by
  apply no_common_zero {args}
'''+'\n'.join(f'  · exact h {i}' for i in range(17)))
parts.append('#print axioms identity\n#print axioms no_common_zero\n#print axioms no_common_zero_sources\n\nend MUB6.LiteralCuspCertificate\n')
dest=options.output
dest.write_text('\n\n'.join(parts),encoding='utf-8',newline='\n')
print(json.dumps({'output':str(dest),'denominator':denominator,'bytes':dest.stat().st_size}))
