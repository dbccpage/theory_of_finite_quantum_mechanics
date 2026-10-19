"""Native closure/boundary challenge, including the full admitted face budget.

AuthorityEffect: None. Bit-mask, cycle-parity and graph oracles are inherited
unchanged. Budget tests use explicit Boolean-lattice cardinalities and two
disjoint maximal faces, not production closure to construct expectations.
"""
from degree_repair import INDEX_TESTS, SIMPLICIAL

RESOURCE_CASES = r'''
#[test] fn complete_boolean_lattice_and_distinct_face_budget() {
 let n=16usize;
 let full=SimplicialComplex::standard_n_simplex(n-1).unwrap();
 assert_eq!(full.total_simplices(),(1usize<<n)-1);
 assert_eq!(full.max_dimension(),n-1);assert_eq!(full.num_vertices(),n);
 let mut counts=[0usize;16];for mask in 1usize..(1usize<<n){counts[mask.count_ones() as usize-1]+=1;}
 for (dimension,count) in counts.into_iter().enumerate(){assert_eq!(full.count(dimension),count);}
 assert_eq!(full.euler_characteristic(),1);
 let one=Simplex::new((0..n).collect()).unwrap();let two=Simplex::new((n..2*n).collect()).unwrap();
 assert_eq!(SimplicialComplex::from_simplices(vec![one,two]).unwrap_err(),HomologicalError::ResourceLimit("simplicial face closure"));
}
#[test] fn duplicate_inputs_and_overlapping_faces_have_exact_union() {
 let edge01=Simplex::new(vec![0,1]).unwrap();let edge02=Simplex::new(vec![0,2]).unwrap();
 let complex=SimplicialComplex::from_simplices(vec![edge01.clone(),edge02.clone(),edge01]).unwrap();
 assert_eq!(complex.total_simplices(),5);assert_eq!(complex.count(0),3);assert_eq!(complex.count(1),2);
 assert_eq!(complex.rational_betti_numbers().unwrap(),vec![1,0]);
 assert_eq!(complex.simplices(0).iter().map(|s|s.vertices().to_vec()).collect::<Vec<_>>(),vec![vec![0],vec![1],vec![2]]);
 assert_eq!(complex.simplices(1).iter().map(|s|s.vertices().to_vec()).collect::<Vec<_>>(),vec![vec![0,1],vec![0,2]]);
}
'''


def challenge(subject):
    return '\n#[cfg(test)] mod independent_simplicial_tests { use super::*;\n'+INDEX_TESTS+SIMPLICIAL+RESOURCE_CASES+'\n}\n'


def variants(subject,source):
    for index,(needle,replacement) in enumerate(subject['faults']):
        if source.count(needle)!=1:raise ValueError('Ambiguous simplicial fault: '+needle)
        yield str(index),source.replace(needle,replacement,1),needle,replacement


def test_filter(needle):
    """Run the smallest decisive negative fixture; controls still run all tests.

    In particular, removing set insertion makes the full lattice enumeration
    factorial. The overlapping-edge fixture detects that valid fault directly.
    """
    if needle in ('if all.contains(&simplex) {','        all.insert(simplex);'):
        name='duplicate_inputs_and_overlapping_faces_have_exact_union'
    elif needle=='if all.len() == MAX_SIMPLICES {':
        name='complete_boolean_lattice_and_distinct_face_budget'
    elif needle in ('HomologicalError::invalid_degree_index(removed_index)',
                    'removed_index >= self.vertices.len()',
                    'value.orientation != 1 && value.orientation != -1',
                    'if pair[1] <= pair[0]'):
        name='full_index_and_wire_admission'
    elif needle in ('removed_index.is_multiple_of(2)','prior ^ (left > right)',
                    'Ok(if odd { -1 } else { 1 })','self.vertices.len() - 1'):
        name='independent_cycle_orientation_and_faces'
    elif needle in ('if n >= MAX_SIMPLEX_VERTICES','simplices.len() > MAX_SIMPLICES'):
        name='bounded_closure_and_gapped_ambient_set'
    elif needle in ('certify_rank(&matrix)?.rank()', 'rank_dk = rank_dk_plus_1;', 'q(sign as i64)','matrix.set(col, row, boundary.get(row, col)?)?',
                    'if k % 2 == 0','let rank_dk_plus_1 = if k == max_dim { 0 } else { rank(k + 1)? };'):
        name='all_three_vertex_families_and_integer_boundaries'
    elif 'vertex label overflow' in needle:
        name='all_three_vertex_families_and_integer_boundaries'
    else:
        raise ValueError('No independently reviewed fault fixture: '+needle)
    return 'subject::independent_simplicial_tests::'+name
