
use crate::gf2_terminalizer::GF2Matrix;

pub const DEFAULT_BUDGET: u64 = 1 << 22;


#[derive(Debug, Clone, PartialEq, Eq)]
struct Bits {
    words: Vec<u64>,
}

impl Bits {
    fn zeros(len: usize) -> Self {
        Bits {
            words: vec![0u64; len.div_ceil(64).max(1)],
        }
    }

    fn from_slice(values: &[u8]) -> Self {
        let mut bits = Bits::zeros(values.len());
        for (index, &value) in values.iter().enumerate() {
            if value % 2 == 1 {
                bits.words[index / 64] |= 1u64 << (index % 64);
            }
        }
        bits
    }

    fn set(&mut self, index: usize) {
        self.words[index / 64] |= 1u64 << (index % 64);
    }

    fn get(&self, index: usize) -> u8 {
        ((self.words[index / 64] >> (index % 64)) & 1) as u8
    }

    fn xor_assign(&mut self, other: &Bits) {
        for (word, &rhs) in self.words.iter_mut().zip(other.words.iter()) {
            *word ^= rhs;
        }
    }

    fn is_zero(&self) -> bool {
        self.words.iter().all(|&word| word == 0)
    }

    fn high_bit(&self) -> Option<usize> {
        for (index, &word) in self.words.iter().enumerate().rev() {
            if word != 0 {
                return Some(index * 64 + (63 - word.leading_zeros() as usize));
            }
        }
        None
    }
}


struct Span {
    pivots: Vec<Option<(Bits, Bits)>>,
}

impl Span {
    fn new(width: usize) -> Self {
        Span {
            pivots: vec![None; width.max(1)],
        }
    }

    fn reduce(&self, mask: &Bits, tag_len: usize) -> (Bits, Bits) {
        let mut residue = mask.clone();
        let mut tag = Bits::zeros(tag_len);
        while let Some(high) = residue.high_bit() {
            match self.pivots.get(high).and_then(|slot| slot.as_ref()) {
                Some((pivot_mask, pivot_tag)) => {
                    residue.xor_assign(pivot_mask);
                    tag.xor_assign(pivot_tag);
                }
                None => break,
            }
        }
        (residue, tag)
    }

    fn insert(&mut self, mask: &Bits, tag: &Bits, tag_len: usize) -> bool {
        let (residue, accumulated) = self.reduce(mask, tag_len);
        let independent = !residue.is_zero();
        if let Some(high) = residue.high_bit() {
            let mut combined = tag.clone();
            combined.xor_assign(&accumulated);
            self.pivots[high] = Some((residue, combined));
        }
        independent
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct L1HarmonicProjection {
    pub weight: usize,
    pub representative: Vec<u8>,
    pub alpha: Vec<u8>,
    pub exact: bool,
    pub searched: u64,
    pub coset_size: u64,
    pub authority_effect: &'static str,
}

fn image_basis(d0: &GF2Matrix) -> Vec<(Bits, Bits)> {
    let mut span = Span::new(d0.rows.max(1));
    let mut basis = Vec::new();
    for column in 0..d0.cols {
        let mut mask = Bits::zeros(d0.rows);
        for row in 0..d0.rows {
            if d0.data[row][column] % 2 == 1 {
                mask.set(row);
            }
        }
        let (residue, accumulated) = span.reduce(&mask, d0.cols);
        if let Some(high) = residue.high_bit() {
            let mut alpha = Bits::zeros(d0.cols);
            alpha.set(column);
            alpha.xor_assign(&accumulated);
            span.pivots[high] = Some((residue.clone(), alpha.clone()));
            basis.push((residue, alpha));
        }
    }
    basis
}

pub fn l1_harmonic_projection(
    d0: &GF2Matrix,
    residual: &[u8],
    budget: u64,
) -> Result<L1HarmonicProjection, String> {
    let measured = tfqm_functional::Phi1Functional::binary_coset_projection(
        &d0.data, d0.cols, residual, budget,
    )?;
    Ok(L1HarmonicProjection {
        weight: measured.weight,
        representative: measured.representative,
        alpha: measured.alpha,
        exact: measured.exact,
        searched: measured.searched,
        coset_size: measured.coset_size,
        authority_effect: "None",
    })
}


pub struct H1Basis {
    pub dim: usize,
    pub generators: Vec<Vec<u8>>,
    pub num_channels: usize,
    span: Span,
}

fn kernel_basis(d1: &GF2Matrix, num_channels: usize) -> Vec<Vec<u8>> {
    if d1.rows == 0 {
        return (0..num_channels)
            .map(|index| {
                let mut vector = vec![0u8; num_channels];
                vector[index] = 1;
                vector
            })
            .collect();
    }
    let (_, reduced) = d1.rref();
    let mut pivot_of_row = Vec::new();
    let mut pivot_columns = Vec::new();
    for row in 0..reduced.rows {
        if let Some(column) = (0..reduced.cols).find(|&c| reduced.data[row][c] == 1) {
            pivot_of_row.push((row, column));
            pivot_columns.push(column);
        }
    }
    (0..num_channels)
        .filter(|column| !pivot_columns.contains(column))
        .map(|free| {
            let mut vector = vec![0u8; num_channels];
            vector[free] = 1;
            for &(row, column) in &pivot_of_row {
                vector[column] = reduced.data[row][free];
            }
            vector
        })
        .collect()
}

pub fn h1_basis(d0: &GF2Matrix, d1: &GF2Matrix) -> H1Basis {
    let num_channels = d0.rows;
    let mut span = Span::new(num_channels.max(1));
    let mut generators: Vec<Vec<u8>> = Vec::new();

    let tag_len = num_channels.max(1);
    for (channel_mask, _alpha) in image_basis(d0) {
        span.insert(&channel_mask, &Bits::zeros(tag_len), tag_len);
    }
    for vector in kernel_basis(d1, num_channels) {
        let mask = Bits::from_slice(&vector);
        let mut tag = Bits::zeros(tag_len);
        tag.set(generators.len());
        if span.insert(&mask, &tag, tag_len) {
            generators.push(vector);
        }
    }

    H1Basis {
        dim: generators.len(),
        generators,
        num_channels,
        span,
    }
}

impl H1Basis {
    pub fn class_coordinates(&self, residual: &[u8]) -> Option<Vec<u8>> {
        if residual.len() != self.num_channels {
            return None;
        }
        let tag_len = self.num_channels.max(1);
        let (remainder, tag) = self.span.reduce(&Bits::from_slice(residual), tag_len);
        if !remainder.is_zero() {
            return None;
        }
        Some((0..self.dim).map(|index| tag.get(index)).collect())
    }

    pub fn class_representative(&self, coordinates: &[u8]) -> Vec<u8> {
        let mut vector = vec![0u8; self.num_channels];
        for (index, &bit) in coordinates.iter().enumerate().take(self.dim) {
            if bit % 2 == 1 {
                for (slot, &value) in vector.iter_mut().zip(self.generators[index].iter()) {
                    *slot ^= value;
                }
            }
        }
        vector
    }

    pub fn class_id(coordinates: &[u8]) -> String {
        let mut label = String::from("h1:");
        for &bit in coordinates {
            label.push(if bit % 2 == 1 { '1' } else { '0' });
        }
        label
    }
}

pub fn code_distance(
    d0: &GF2Matrix,
    d1: &GF2Matrix,
    budget: u64,
) -> Result<(Option<usize>, bool), String> {
    let basis = h1_basis(d0, d1);
    if basis.dim == 0 {
        return Ok((None, true));
    }
    if basis.dim >= 64 {
        return Err(
            "code distance refused: dim H^1 >= 64 does not fit an exact class enumeration".into(),
        );
    }
    let mut best: Option<usize> = None;
    let mut all_exact = true;
    for code in 1u64..(1u64 << basis.dim) {
        let coordinates: Vec<u8> = (0..basis.dim)
            .map(|index| ((code >> index) & 1) as u8)
            .collect();
        let representative = basis.class_representative(&coordinates);
        let projection = l1_harmonic_projection(d0, &representative, budget)?;
        all_exact = all_exact && projection.exact;
        best = Some(match best {
            None => projection.weight,
            Some(current) => current.min(projection.weight),
        });
    }
    Ok((best, all_exact))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::repair_limit::{apply_d0, gf2_add};
    use crate::tetron::{build_tetron_array, logical_class_representative, Axis, Topology};

    fn brute_force_min_weight(d0: &GF2Matrix, residual: &[u8]) -> usize {
        let mut best = residual.iter().filter(|&&b| b == 1).count();
        for bits in 0u64..(1u64 << d0.cols) {
            let alpha: Vec<u8> = (0..d0.cols)
                .map(|index| ((bits >> index) & 1) as u8)
                .collect();
            let image = apply_d0(d0, &alpha).unwrap();
            let combined = gf2_add(residual, &image).unwrap();
            best = best.min(combined.iter().filter(|&&b| b == 1).count());
        }
        best
    }

    #[test]
    fn matches_brute_force_over_all_alpha() {
        for topology in [Topology::Disk, Topology::Cylinder, Topology::Torus] {
            let (complex, report) = build_tetron_array(2, 2, topology).unwrap();
            let mut state: u64 = 0x2026_0805;
            for _ in 0..8 {
                let residual: Vec<u8> = (0..report.num_channels)
                    .map(|_| {
                        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                        ((state >> 33) & 1) as u8
                    })
                    .collect();
                let projection =
                    l1_harmonic_projection(&complex.d0, &residual, DEFAULT_BUDGET).unwrap();
                assert!(projection.exact);
                assert_eq!(
                    projection.weight,
                    brute_force_min_weight(&complex.d0, &residual),
                    "{topology:?}"
                );
            }
        }
    }

    #[test]
    fn representative_lies_in_the_coset_with_the_reported_alpha() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let residual = logical_class_representative(&report, Axis::Column, 0);
        let projection = l1_harmonic_projection(&complex.d0, &residual, DEFAULT_BUDGET).unwrap();
        let image = apply_d0(&complex.d0, &projection.alpha).unwrap();
        assert_eq!(
            gf2_add(&residual, &image).unwrap(),
            projection.representative
        );
        assert_eq!(
            projection.weight,
            projection
                .representative
                .iter()
                .filter(|&&b| b == 1)
                .count()
        );
    }

    #[test]
    fn phi1_is_constant_on_a_cohomology_class() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let residual = logical_class_representative(&report, Axis::Column, 0);
        let baseline = l1_harmonic_projection(&complex.d0, &residual, DEFAULT_BUDGET).unwrap();
        let mut state: u64 = 99;
        for _ in 0..6 {
            let alpha: Vec<u8> = (0..report.num_mzm)
                .map(|_| {
                    state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                    ((state >> 33) & 1) as u8
                })
                .collect();
            let shifted = gf2_add(&residual, &apply_d0(&complex.d0, &alpha).unwrap()).unwrap();
            let moved = l1_harmonic_projection(&complex.d0, &shifted, DEFAULT_BUDGET).unwrap();
            assert_eq!(moved.weight, baseline.weight);
            assert_eq!(moved.representative, baseline.representative);
        }
    }

    #[test]
    fn budget_exhaustion_reports_an_upper_bound_not_a_lie() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let residual = logical_class_representative(&report, Axis::Column, 0);
        let full = l1_harmonic_projection(&complex.d0, &residual, DEFAULT_BUDGET).unwrap();
        assert!(full.exact);
        let capped = l1_harmonic_projection(&complex.d0, &residual, 8).unwrap();
        assert!(!capped.exact);
        assert!(capped.searched <= 8);
        assert!(capped.weight >= full.weight);
    }

    #[test]
    fn class_coordinates_are_a_homomorphism() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let basis = h1_basis(&complex.d0, &complex.d1);
        let lam1 = logical_class_representative(&report, Axis::Column, 0);
        let lam2 = logical_class_representative(&report, Axis::Row, 0);
        let combined = gf2_add(&lam1, &lam2).unwrap();
        let c1 = basis.class_coordinates(&lam1).unwrap();
        let c2 = basis.class_coordinates(&lam2).unwrap();
        let c12 = basis.class_coordinates(&combined).unwrap();
        assert_eq!(c12, gf2_add(&c1, &c2).unwrap());
        assert_ne!(c1, c2);
        assert_ne!(c1, vec![0, 0]);
    }

    #[test]
    fn open_residual_has_no_class() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let basis = h1_basis(&complex.d0, &complex.d1);
        let mut residual = vec![0u8; report.num_channels];
        residual[0] = 1;
        assert!(basis.class_coordinates(&residual).is_none());
    }

    #[test]
    fn h1_generators_are_closed_and_not_exact() {
        use crate::repair_limit::{in_image_d0, is_closed};
        let (complex, _) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let basis = h1_basis(&complex.d0, &complex.d1);
        assert_eq!(basis.dim, 2);
        for generator in &basis.generators {
            assert!(is_closed(&complex.d1, generator).unwrap());
            assert!(!in_image_d0(&complex.d0, generator).unwrap());
        }
    }

    #[test]
    fn code_distance_is_the_topological_one() {
        for (rows, cols) in [(2usize, 3usize), (3, 3), (3, 4), (4, 3)] {
            let (complex, _) = build_tetron_array(rows, cols, Topology::Torus).unwrap();
            let (distance, exact) =
                code_distance(&complex.d0, &complex.d1, DEFAULT_BUDGET).unwrap();
            assert!(exact);
            assert_eq!(distance, Some(rows.min(cols)), "torus {rows}x{cols}");
        }
        for (rows, cols) in [(2usize, 3usize), (3, 3), (2, 4)] {
            let (complex, _) = build_tetron_array(rows, cols, Topology::Cylinder).unwrap();
            let (distance, exact) =
                code_distance(&complex.d0, &complex.d1, DEFAULT_BUDGET).unwrap();
            assert!(exact);
            assert_eq!(distance, Some(rows + 1), "cylinder {rows}x{cols}");
        }
        let d0 = GF2Matrix::zeros(64, 0);
        let d1 = GF2Matrix::zeros(0, 64);
        let err = code_distance(&d0, &d1, 1).unwrap_err();
        assert!(
            err.contains("dim H^1 >= 64"),
            "a 64-dimensional class space must be refused, got {err}"
        );

        let mut wide = GF2Matrix::zeros(64, 64);
        for index in 0..64 {
            wide.data[index][index] = 1;
        }
        let projection = l1_harmonic_projection(&wide, &vec![1u8; 64], 4).unwrap();
        assert!(!projection.exact);
        assert_eq!(projection.coset_size, u64::MAX);

        let (complex, _) = build_tetron_array(3, 3, Topology::Disk).unwrap();
        assert_eq!(
            code_distance(&complex.d0, &complex.d1, DEFAULT_BUDGET).unwrap(),
            (None, true),
            "H^1 = 0 leaves nothing to weigh"
        );
    }

    #[test]
    fn per_class_weights_match_the_python_face() {
        let (complex, _) = build_tetron_array(3, 4, Topology::Torus).unwrap();
        let basis = h1_basis(&complex.d0, &complex.d1);
        assert_eq!(basis.dim, 2);

        let mut observed: Vec<(String, usize)> = Vec::new();
        for code in 0u64..(1u64 << basis.dim) {
            let coordinates: Vec<u8> = (0..basis.dim)
                .map(|index| ((code >> index) & 1) as u8)
                .collect();
            let representative = basis.class_representative(&coordinates);
            let projection =
                l1_harmonic_projection(&complex.d0, &representative, DEFAULT_BUDGET).unwrap();
            assert!(projection.exact);
            observed.push((H1Basis::class_id(&coordinates), projection.weight));
        }
        observed.sort();

        assert_eq!(
            observed,
            vec![
                ("h1:00".to_string(), 0usize),
                ("h1:01".to_string(), 4),
                ("h1:10".to_string(), 3),
                ("h1:11".to_string(), 7),
            ]
        );
    }

    #[test]
    fn structure_matches_the_python_face() {
        let cases = [
            (
                Topology::Disk,
                3usize,
                3usize,
                16usize,
                24usize,
                9usize,
                15usize,
                9usize,
                0usize,
            ),
            (Topology::Cylinder, 3, 3, 12, 21, 9, 11, 9, 1),
            (Topology::Torus, 2, 2, 4, 8, 4, 3, 3, 2),
            (Topology::Torus, 3, 3, 9, 18, 9, 8, 8, 2),
            (Topology::Torus, 3, 4, 12, 24, 12, 11, 11, 2),
            (Topology::Torus, 4, 4, 16, 32, 16, 15, 15, 2),
            (Topology::Torus, 4, 5, 20, 40, 20, 19, 19, 2),
        ];
        for (topology, rows, cols, v, e, f, rank_d0, rank_d1, dim_h1) in cases {
            let (_, report) = build_tetron_array(rows, cols, topology).unwrap();
            assert_eq!(
                (
                    report.num_mzm,
                    report.num_channels,
                    report.num_islands,
                    report.rank_d0,
                    report.rank_d1,
                    report.dim_h1
                ),
                (v, e, f, rank_d0, rank_d1, dim_h1),
                "{topology:?} {rows}x{cols} drifted from the Python face"
            );
        }
    }

    #[test]
    fn harmonic_code_distance_and_h1_scaling_on_larger_lattices() {
        use crate::repair_limit::{in_image_d0, is_closed};

        // Exact code distance on 4x4 Torus (V=16, rank(d0)=15, coset_size=32768)
        let (torus_4x4, _) = build_tetron_array(4, 4, Topology::Torus).unwrap();
        let (dist_4x4, exact_4x4) =
            code_distance(&torus_4x4.d0, &torus_4x4.d1, DEFAULT_BUDGET).unwrap();
        assert!(exact_4x4);
        assert_eq!(dist_4x4, Some(4));

        // Exact code distance on 3x4 Cylinder (V=16, rank(d0)=15, coset_size=32768)
        let (cyl_3x4, _) = build_tetron_array(3, 4, Topology::Cylinder).unwrap();
        let (dist_cyl, exact_cyl) =
            code_distance(&cyl_3x4.d0, &cyl_3x4.d1, DEFAULT_BUDGET).unwrap();
        assert!(exact_cyl);
        assert_eq!(dist_cyl, Some(4));

        // H^1 basis construction and class homomorphism scaling on 5x5, 6x6, and 6x8 Tori
        for (rows, cols) in [(5usize, 5usize), (6, 6), (6, 8)] {
            let (complex, report) = build_tetron_array(rows, cols, Topology::Torus).unwrap();
            let basis = h1_basis(&complex.d0, &complex.d1);
            assert_eq!(basis.dim, 2, "torus {rows}x{cols}");
            for gen in &basis.generators {
                assert!(is_closed(&complex.d1, gen).unwrap());
                assert!(!in_image_d0(&complex.d0, gen).unwrap());
            }
            let col_rep = logical_class_representative(&report, Axis::Column, 0);
            let row_rep = logical_class_representative(&report, Axis::Row, 0);
            let c_col = basis.class_coordinates(&col_rep).unwrap();
            let c_row = basis.class_coordinates(&row_rep).unwrap();
            assert_ne!(c_col, vec![0, 0]);
            assert_ne!(c_row, vec![0, 0]);
            assert_ne!(c_col, c_row);
        }
    }
}
