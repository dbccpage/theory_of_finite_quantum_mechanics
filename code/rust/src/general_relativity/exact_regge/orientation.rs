
#![forbid(unsafe_code)]

pub fn triangle_boundary_of_tetra(tetra: [u32; 4]) -> [([u32; 3], i8); 4] {
    let [v0, v1, v2, v3] = tetra;
    [
        ([v1, v2, v3], 1),
        ([v0, v2, v3], -1),
        ([v0, v1, v3], 1),
        ([v0, v1, v2], -1),
    ]
}

pub fn tetra_boundary_of_pentatope(pentatope: [u32; 5]) -> [([u32; 4], i8); 5] {
    let [v0, v1, v2, v3, v4] = pentatope;
    [
        ([v1, v2, v3, v4], 1),
        ([v0, v2, v3, v4], -1),
        ([v0, v1, v3, v4], 1),
        ([v0, v1, v2, v4], -1),
        ([v0, v1, v2, v3], 1),
    ]
}

#[cfg(test)]
mod tests {
    use super::{tetra_boundary_of_pentatope, triangle_boundary_of_tetra};
    use std::collections::BTreeMap;

    #[test]
    fn tetra_triangle_signs_omit_each_vertex_once() {
        let tetra = [7, 1, 4, 9];
        let boundary = triangle_boundary_of_tetra(tetra);
        let signs = [1_i8, -1, 1, -1];
        let mut omitted = [0_u32; 4];
        let mut sign_sum = 0_i32;
        for (i, (face, sign)) in boundary.iter().enumerate() {
            assert_eq!(*sign, signs[i]);
            sign_sum += i32::from(*sign);
            let mut missing = None;
            for &vertex in &tetra {
                if !face.iter().any(|&other| other == vertex) {
                    assert!(missing.is_none());
                    missing = Some(vertex);
                }
            }
            omitted[i] = missing.expect("each triangle omits one vertex");
        }
        assert_eq!(sign_sum, 0);
        assert_eq!(signs, [1, -1, 1, -1]);
        let mut omitted_sorted = omitted;
        omitted_sorted.sort_unstable();
        let mut tetra_sorted = tetra;
        tetra_sorted.sort_unstable();
        assert_eq!(omitted_sorted, tetra_sorted);
        assert_eq!(
            boundary,
            [
                ([1, 4, 9], 1),
                ([7, 4, 9], -1),
                ([7, 1, 9], 1),
                ([7, 1, 4], -1),
            ]
        );
    }

    #[test]
    fn pentatope_tetra_signs_omit_each_vertex_once() {
        let pentatope = [7, 1, 4, 9, 2];
        let boundary = tetra_boundary_of_pentatope(pentatope);
        let signs = [1_i8, -1, 1, -1, 1];
        let mut omitted = [0_u32; 5];
        for (i, (face, sign)) in boundary.iter().enumerate() {
            assert_eq!(*sign, signs[i]);
            let mut missing = None;
            for &vertex in &pentatope {
                if !face.iter().any(|&other| other == vertex) {
                    assert!(missing.is_none());
                    missing = Some(vertex);
                }
            }
            omitted[i] = missing.expect("each tetrahedron omits one vertex");
        }
        let mut omitted_sorted = omitted;
        omitted_sorted.sort_unstable();
        let mut pentatope_sorted = pentatope;
        pentatope_sorted.sort_unstable();
        assert_eq!(omitted_sorted, pentatope_sorted);
        assert_eq!(
            boundary,
            [
                ([1, 4, 9, 2], 1),
                ([7, 4, 9, 2], -1),
                ([7, 1, 9, 2], 1),
                ([7, 1, 4, 2], -1),
                ([7, 1, 4, 9], 1),
            ]
        );
    }

    #[test]
    fn pentatope_boundary_of_boundary_cancels() {
        let pentatope = [0, 1, 2, 3, 4];
        let mut coeff: BTreeMap<[u32; 3], i32> = BTreeMap::new();
        for (tetra, tetra_sign) in tetra_boundary_of_pentatope(pentatope) {
            for (triangle, triangle_sign) in triangle_boundary_of_tetra(tetra) {
                *coeff.entry(triangle).or_insert(0) +=
                    i32::from(tetra_sign) * i32::from(triangle_sign);
            }
        }
        assert_eq!(coeff.len(), 10);
        assert!(coeff.values().all(|&c| c == 0));
    }
}
