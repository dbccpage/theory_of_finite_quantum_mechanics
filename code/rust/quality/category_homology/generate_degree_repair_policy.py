"""Pin the explicitly reviewed degree-repair subjects and designated faults.

AuthorityEffect: None. This constructs a challenge policy, never a grade.
"""
import json
from pathlib import Path
import re

from run_audit import ROOT, digest, write_json


def main():
    quality=Path(__file__).resolve().parent
    records=[]
    for name in ('errors','chain_complex','cochain_complex','simplicial'):
        path=ROOT/'code/rust/src/homology'/(name+'.rs')
        source=path.read_text(encoding='utf-8')
        faults=[]
        if name=='errors':
            for match in re.finditer(r'#\[error\((.*?)\)\]',source.split('#[cfg(test)]')[0],re.S):
                needle=match.group(0)
                # Signed and full-index errors intentionally share a message.
                # Bind the variant declaration so each valid fault is unique.
                if source.count(needle)>1:
                    needle+=source[match.end():source.index('\n',match.end()+1)]
                quote=needle.index('"')+1
                faults.append([needle,needle[:quote]+'BROKEN '+needle[quote:]])
            faults.extend([
                ['Err(_) => Self::InvalidDegreeIndex(degree)','Err(_) => Self::InvalidDegree(0)'],
                ['Ok(value) => Self::InvalidDegree(value)','Ok(value) => Self::InvalidDegree(0)']])
        elif name in ('chain_complex','cochain_complex'):
            faults.extend([
                ['HomologicalError::invalid_degree_index(degree)','HomologicalError::InvalidDegree(degree as i32)'],
                ['0 => Ok(self.c0_dim)','0 => Ok(self.c1_dim)'],
                ['1 => Ok(self.c1_dim)','1 => Ok(self.c2_dim)'],
                ['2 => Ok(self.c2_dim)','2 => Ok(self.c0_dim)'],
                ['super::exact_scalar::admit_zero_product(','(|_,_,_| Ok::<(),HomologicalError>(()))(']])
            matrices=('d1_matrix','d2_matrix') if name=='chain_complex' else ('d0_matrix','d1_matrix')
            for matrix in matrices:
                match=re.search(r'super::exact_scalar::admit_shaped_matrix\(&'+matrix+r', \([^\n]+\)\)',source)
                if match is None:raise ValueError('Missing explicit shape gate')
                needle=match.group(0)
                faults.append([needle,needle.replace('super::exact_scalar::admit_shaped_matrix','(|_,_| Ok::<(),HomologicalError>(()))',1)])
            if name=='chain_complex':
                faults.append(['vec![d1_matrix.clone(), d2_matrix.clone()]','vec![d2_matrix.clone(), d1_matrix.clone()]'])
            else:
                faults.extend([
                    ['verification_source.trim().is_empty()','verification_source.is_empty()'],
                    ['        &self.verification_source','        "wrong"'],
                    ['hash_provenance(&self.verification_source)','hash_provenance("wrong")']])
        else:
            faults=[
                ['HomologicalError::invalid_degree_index(removed_index)','HomologicalError::InvalidDegree(removed_index as i32)'],
                ['removed_index >= self.vertices.len()','removed_index > self.vertices.len()'],
                ['removed_index.is_multiple_of(2)','removed_index.is_multiple_of(3)'],
                ['prior ^ (left > right)','prior | (left > right)'],
                ['prior ^ (left > right)','prior ^ (left < right)'],
                ['Ok(if odd { -1 } else { 1 })','Ok(if odd { 1 } else { -1 })'],
                ['self.vertices.len() - 1','self.vertices.len()'],
                ['value.orientation != 1 && value.orientation != -1','value.orientation != 1 || value.orientation != -1'],
                ['if n >= MAX_SIMPLEX_VERTICES','if n > MAX_SIMPLEX_VERTICES'],
                ['simplices.len() > MAX_SIMPLICES','simplices.len() > MAX_SIMPLICES + 1'],
                ['q(sign as i64)','q(-(sign as i64))'],
                ['matrix.set(col, row, boundary.get(row, col)?)?','matrix.set(row, col, boundary.get(row, col)?)?'],
                ['if k % 2 == 0','if k % 2 != 0'],
                ['let rank_dk_plus_1 = if k == max_dim { 0 } else { rank(k + 1)? };','let rank_dk_plus_1 = 0;'],
                ['.checked_add(1)\n                    .ok_or(HomologicalError::ResourceLimit("vertex label overflow"))?',
                 '.checked_add(0)\n                    .ok_or(HomologicalError::ResourceLimit("vertex label overflow"))?'],
                ['if pair[1] <= pair[0]','if pair[1] < pair[0]']]
        for needle,replacement in faults:
            if source.count(needle)!=1 or needle==replacement:
                raise ValueError('Ambiguous or ineffective fault: '+name+' '+needle)
        records.append({'path':path.relative_to(ROOT).as_posix(),'sha256':digest(path),'family':'',
            'parent_aliases':['exact_scalar'] if name in ('chain_complex','cochain_complex') else [],'faults':faults})
    write_json(quality/'degree_repair_boundaries.json',{'AuthorityEffect':'None','records':records})
    print(len(records),'subjects,',sum(len(row['faults']) for row in records),'designated faults')


if __name__=='__main__':
    main()
