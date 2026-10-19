"""Finite mathematical audit of the consumer's determinant/component oracles.

AuthorityEffect: None. Standard-library exact Fractions and independent
transitive closure/row reduction, not a replay of Rust or a general graph proof.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[4]

def rank(rows, columns):
    a=[[Fraction(x) for x in row] for row in rows]
    pivot=0
    for col in range(columns):
        selected=next((r for r in range(pivot,len(a)) if a[r][col]),None)
        if selected is None:continue
        a[pivot],a[selected]=a[selected],a[pivot]
        scale=a[pivot][col]
        a[pivot]=[x/scale for x in a[pivot]]
        for r in range(len(a)):
            if r!=pivot:
                scale=a[r][col]
                a[r]=[x-scale*y for x,y in zip(a[r],a[pivot])]
        pivot+=1
    return pivot

def main():
    source=ROOT/'code/rust/src/homology/l5a_challenges.rs'
    text=source.read_text(encoding='utf-8')
    assert 'for code in 0..81usize' in text and 'for bits in 0..64' in text
    assert '[(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]' in text
    matrices=[]
    for code in range(81):
        a,b,c,d=[(code//3**i)%3-1 for i in range(4)]
        expected=2 if a*d-b*c else int(any([a,b,c,d]))
        actual=rank([[a,b],[c,d]],2)
        assert expected==actual
        matrices.append({'code':code,'entries':[a,b,c,d],'expected':expected,'fraction_rank':actual})
    possible=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    graphs=[]
    for bits in range(64):
        edges=[edge for i,edge in enumerate(possible) if bits&(1<<i)]
        reach=[[a==b for b in range(4)] for a in range(4)]
        for a,b in edges:reach[a][b]=reach[b][a]=True
        for via in range(4):
            for a in range(4):
                for b in range(4):reach[a][b]|=reach[a][via] and reach[via][b]
        components=len({min(b for b in range(4) if reach[a][b]) for a in range(4)})
        # Explicit translation of the reviewed Rust label helper, compared to
        # a different closure algorithm. No claim this executes the Rust body.
        labels=list(range(4))
        for a,b in edges:
            old,new=labels[b],labels[a]
            labels=[new if label==old else label for label in labels]
        assert len(set(labels))==components
        incidence=[[int(v==b)-int(v==a) for v in range(4)] for a,b in edges]
        actual_rank=rank(incidence,4)
        assert actual_rank==4-components
        expected=len(edges)+components-4
        assert expected==len(edges)-actual_rank>=0
        graphs.append({'bits':bits,'components':components,'fraction_incidence_rank':actual_rank,'expected_h1':expected})
    out=ROOT/sys.argv[1]
    out.write_text(json.dumps({'AuthorityEffect':'None','source':source.relative_to(ROOT).as_posix(),
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Finite mathematical oracle audit and reviewed algorithm translation; not native Rust replay or an arbitrary graph/determinant theorem.',
        'ternary_matrices':matrices,'four_vertex_graphs':graphs,'checks_passed':True},indent=2)+'\n',encoding='utf-8',newline='\n')
    print('81 determinant-oracle cases and 64 graph-oracle cases verified by exact Fraction rank and transitive closure.')

if __name__=='__main__':main()
