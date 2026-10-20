//! Exact rational Hubbard determinants: 4x4 plaquette, attractive Hubbard square-root symmetry,
//! and palindromic spectra over Q.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};

fn find_nonzero_pivot_row(a: &[Vec<BigRational>], col: usize, n: usize) -> Option<usize> {
    (col..n).find(|&row| !a[row][col].is_zero())
}

fn eliminate_below_pivot(
    a: &mut [Vec<BigRational>],
    col: usize,
    n: usize,
    p_val: &BigRational,
) {
    let pivot_row_vals = a[col].clone();
    for row_vals in a.iter_mut().take(n).skip(col + 1) {
        if !row_vals[col].is_zero() {
            let factor = &row_vals[col] / p_val;
            for c in col..n {
                let term = &factor * &pivot_row_vals[c];
                row_vals[c] = &row_vals[c] - term;
            }
        }
    }
}

/// Exact rational matrix determinant via Gaussian elimination over Q.
pub fn exact_determinant(mat: &[Vec<BigRational>]) -> Result<BigRational, &'static str> {
    let n = mat.len();
    if n == 0 {
        return Ok(BigRational::one());
    }
    if mat.iter().any(|row| row.len() != n) {
        return Err("matrix must be square for determinant");
    }
    let mut a: Vec<Vec<BigRational>> = mat.to_vec();
    let mut det = BigRational::one();
    let mut sign_flips = 0;

    for col in 0..n {
        let Some(pivot_row) = find_nonzero_pivot_row(&a, col, n) else {
            return Ok(BigRational::zero());
        };
        if pivot_row != col {
            a.swap(col, pivot_row);
            sign_flips ^= 1;
        }
        let p_val = a[col][col].clone();
        det = det * &p_val;
        eliminate_below_pivot(&mut a, col, n, &p_val);
    }

    if sign_flips == 1 {
        det = -det;
    }
    Ok(det)
}

/// Multiply two square matrices over Q.
pub fn exact_matrix_mul(
    a: &[Vec<BigRational>],
    b: &[Vec<BigRational>],
) -> Result<Vec<Vec<BigRational>>, &'static str> {
    let n = a.len();
    if n == 0 || b.len() != n {
        return Err("matrix dimension mismatch in multiplication");
    }
    for row in a {
        if row.len() != n {
            return Err("matrix A is not square");
        }
    }
    for row in b {
        if row.len() != n {
            return Err("matrix B is not square");
        }
    }
    let mut c = vec![vec![BigRational::zero(); n]; n];
    for i in 0..n {
        for k in 0..n {
            if a[i][k].is_zero() {
                continue;
            }
            for j in 0..n {
                let term = &a[i][k] * &b[k][j];
                c[i][j] = &c[i][j] + term;
            }
        }
    }
    Ok(c)
}

/// Compute palindromic kinetic matrix over Q:
/// Product of bond exponentials in forward then reverse order:
/// K = \prod_{e} B_e \prod_{e^rev} B_e
/// where r = exp(dtau * t / 2) is exact rational parameter.
pub fn exact_kinetic_matrix(
    sites: usize,
    bonds: &[(usize, usize)],
    r: &BigRational,
) -> Result<Vec<Vec<BigRational>>, &'static str> {
    if sites == 0 {
        return Err("sites must be positive");
    }
    if r <= &BigRational::zero() {
        return Err("r parameter must be strictly positive");
    }
    let r_inv = BigRational::one() / r;
    let two = BigRational::from(BigInt::from(2));
    let cosh_val = (r + &r_inv) / &two;
    let sinh_val = (r - &r_inv) / &two;

    let mut k_mat = vec![vec![BigRational::zero(); sites]; sites];
    for i in 0..sites {
        k_mat[i][i] = BigRational::one();
    }

    // Schedule: bonds forward, then bonds reverse
    let mut schedule = bonds.to_vec();
    let mut rev = bonds.to_vec();
    rev.reverse();
    schedule.extend(rev);

    for &(u, v) in &schedule {
        if u >= sites || v >= sites || u == v {
            return Err("invalid bond endpoint");
        }
        let mut b = vec![vec![BigRational::zero(); sites]; sites];
        for i in 0..sites {
            b[i][i] = BigRational::one();
        }
        b[u][u] = cosh_val.clone();
        b[v][v] = cosh_val.clone();
        b[u][v] = sinh_val.clone();
        b[v][u] = sinh_val.clone();

        k_mat = exact_matrix_mul(&b, &k_mat)?;
    }

    Ok(k_mat)
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct HubbardDeterminantReceipt {
    pub mask: usize,
    pub det_up: BigRational,
    pub det_down: BigRational,
    pub total_weight: BigRational,
    pub is_strictly_positive: bool,
    pub attractive_symmetry_holds: bool,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct HubbardEnsembleSummary {
    pub sites: usize,
    pub slices: usize,
    pub total_fields: usize,
    pub negative_fields_count: usize,
    pub zero_fields_count: usize,
    pub total_determinant_sum: BigRational,
    pub absolute_determinant_sum: BigRational,
    pub average_sign: BigRational,
    pub attractive_square_root_protected: bool,
}

fn build_slice_potentials(
    sites: usize,
    time: usize,
    mask: usize,
    hs: &BigRational,
    hs_inv: &BigRational,
    fugacity: &BigRational,
    attractive: bool,
) -> (Vec<Vec<BigRational>>, Vec<Vec<BigRational>>) {
    let mut v_up = vec![vec![BigRational::zero(); sites]; sites];
    let mut v_down = vec![vec![BigRational::zero(); sites]; sites];
    for j in 0..sites {
        let shift = (time * sites + j) as u32;
        let bit = mask.checked_shr(shift).unwrap_or(0) & 1;
        let s_val = if bit == 1 { 1 } else { -1 };
        let exp_down = if attractive { s_val } else { -s_val };
        let hs_up = if s_val == 1 { hs } else { hs_inv };
        let hs_down = if exp_down == 1 { hs } else { hs_inv };
        v_up[j][j] = fugacity * hs_up;
        v_down[j][j] = fugacity * hs_down;
    }
    (v_up, v_down)
}

fn evaluate_single_field_mask(
    sites: usize,
    slices: usize,
    k_mat: &[Vec<BigRational>],
    hs: &BigRational,
    hs_inv: &BigRational,
    fugacity: &BigRational,
    attractive: bool,
    mask: usize,
) -> Result<HubbardDeterminantReceipt, &'static str> {
    let mut b_up = vec![vec![BigRational::zero(); sites]; sites];
    let mut b_down = vec![vec![BigRational::zero(); sites]; sites];
    for i in 0..sites {
        b_up[i][i] = BigRational::one();
        b_down[i][i] = BigRational::one();
    }
    for time in 0..slices {
        let (v_up, v_down) =
            build_slice_potentials(sites, time, mask, hs, hs_inv, fugacity, attractive);
        let slice_up = exact_matrix_mul(k_mat, &v_up)?;
        let slice_down = exact_matrix_mul(k_mat, &v_down)?;
        b_up = exact_matrix_mul(&slice_up, &b_up)?;
        b_down = exact_matrix_mul(&slice_down, &b_down)?;
    }
    for i in 0..sites {
        b_up[i][i] = &b_up[i][i] + BigRational::one();
        b_down[i][i] = &b_down[i][i] + BigRational::one();
    }
    let det_up = exact_determinant(&b_up)?;
    let det_down = exact_determinant(&b_down)?;
    let symmetry_holds = if attractive { det_up == det_down } else { true };
    let weight = &det_up * &det_down;
    Ok(HubbardDeterminantReceipt {
        mask,
        det_up,
        det_down,
        total_weight: weight.clone(),
        is_strictly_positive: weight > BigRational::zero(),
        attractive_symmetry_holds: symmetry_holds,
    })
}

/// Compute exact auxiliary-field Hubbard determinants for declared field masks.
pub fn evaluate_hubbard_determinants(
    sites: usize,
    bonds: &[(usize, usize)],
    slices: usize,
    r: &BigRational,
    hs: &BigRational,
    fugacity: &BigRational,
    attractive: bool,
    field_masks: &[usize],
) -> Result<HubbardEnsembleSummary, &'static str> {
    if sites == 0 || slices == 0 {
        return Err("sites and slices must be positive");
    }
    if hs.is_zero() {
        return Err("hs coupling parameter must be non-zero");
    }
    let Some(total_bits) = sites.checked_mul(slices) else {
        return Err("sites * slices overflow");
    };
    if total_bits >= usize::BITS as usize {
        return Err("sites * slices exceeds usize bit width");
    }
    if field_masks.is_empty() {
        return Err("at least one field mask required");
    }

    let k_mat = exact_kinetic_matrix(sites, bonds, r)?;
    let hs_inv = BigRational::one() / hs;
    let mut total_sum = BigRational::zero();
    let mut abs_sum = BigRational::zero();
    let mut neg_count = 0;
    let mut zero_count = 0;
    let mut all_attractive_protected = true;

    for &mask in field_masks {
        let receipt = evaluate_single_field_mask(
            sites, slices, &k_mat, hs, &hs_inv, fugacity, attractive, mask,
        )?;
        if attractive && !receipt.attractive_symmetry_holds {
            all_attractive_protected = false;
        }
        if receipt.total_weight.is_zero() {
            zero_count += 1;
        } else if receipt.total_weight < BigRational::zero() {
            neg_count += 1;
        }
        total_sum = total_sum + &receipt.total_weight;
        abs_sum = abs_sum + receipt.total_weight.abs();
    }

    let avg_sign = if abs_sum.is_zero() {
        BigRational::zero()
    } else {
        &total_sum / &abs_sum
    };

    Ok(HubbardEnsembleSummary {
        sites,
        slices,
        total_fields: field_masks.len(),
        negative_fields_count: neg_count,
        zero_fields_count: zero_count,
        total_determinant_sum: total_sum,
        absolute_determinant_sum: abs_sum,
        average_sign: avg_sign,
        attractive_square_root_protected: all_attractive_protected && attractive,
    })
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct HubbardLatticeScalingRow {
    pub label: String,
    pub sites: usize,
    pub num_bonds: usize,
    pub slices: usize,
    pub attractive: bool,
    pub evaluated_fields: usize,
    pub negative_fields_count: usize,
    pub zero_fields_count: usize,
    #[serde(with = "crate::fock::rational_str_serde")]
    pub average_sign: BigRational,
    pub attractive_square_root_protected: bool,
}

/// Serialize `HubbardLatticeScalingRow` slice to canonical 2-space pretty JSON with LF line endings.
pub fn hubbard_scaling_to_canonical_json(rows: &[HubbardLatticeScalingRow]) -> Result<String, String> {
    serde_json::to_string_pretty(rows).map_err(|e| e.to_string())
}

/// Deserialize `HubbardLatticeScalingRow` vector from canonical JSON string.
pub fn hubbard_scaling_from_canonical_json(
    json_str: &str,
) -> Result<Vec<HubbardLatticeScalingRow>, String> {
    serde_json::from_str(json_str).map_err(|e| e.to_string())
}

/// Construct 2D rectangular grid bonds (`rows x cols` sites) with optional periodic wrapping.
pub fn hubbard_rectangular_bonds(
    rows: usize,
    cols: usize,
    periodic: bool,
) -> Result<(usize, Vec<(usize, usize)>), &'static str> {
    if rows == 0 || cols == 0 {
        return Err("rows and cols must be positive");
    }
    let sites = rows * cols;
    let idx = |r: usize, c: usize| r * cols + c;
    let mut bonds = Vec::new();
    for r in 0..rows {
        for c in 0..cols {
            if c + 1 < cols {
                bonds.push((idx(r, c), idx(r, c + 1)));
            } else if periodic && cols > 2 {
                bonds.push((idx(r, c), idx(r, 0)));
            }
            if r + 1 < rows {
                bonds.push((idx(r, c), idx(r + 1, c)));
            } else if periodic && rows > 2 {
                bonds.push((idx(r, c), idx(0, c)));
            }
        }
    }
    Ok((sites, bonds))
}

/// Finite lattice scaling benchmark for exact rational Hubbard auxiliary-field determinants
/// across 1D rings and 2D grids up to 3x4 (12 sites) and multiple Trotter slices.
pub fn benchmark_hubbard_lattice_scaling() -> Result<Vec<HubbardLatticeScalingRow>, &'static str> {
    let r = BigRational::new(BigInt::from(3), BigInt::from(2));
    let hs = BigRational::from(BigInt::from(2));
    let unit_fugacity = BigRational::one();
    let doped_fugacity = BigRational::new(BigInt::from(3), BigInt::from(5));

    let (_, bonds_2x2) = hubbard_rectangular_bonds(2, 2, false)?;
    let (_, bonds_2x3) = hubbard_rectangular_bonds(2, 3, false)?;
    let (_, bonds_2x4) = hubbard_rectangular_bonds(2, 4, false)?;
    let (_, bonds_3x3) = hubbard_rectangular_bonds(3, 3, false)?;
    let (_, bonds_3x4) = hubbard_rectangular_bonds(3, 4, false)?;
    let (_, bonds_1x10) = hubbard_rectangular_bonds(1, 10, true)?;

    // Frustrated 2x3 and 3x3 lattices with next-nearest-neighbor diagonal bonds
    let mut frust_2x3 = bonds_2x3.clone();
    frust_2x3.extend([(0, 4), (1, 5)]);
    let mut frust_3x3 = bonds_3x3.clone();
    frust_3x3.extend([(0, 4), (4, 8)]);

    // Deterministic diverse field masks spanning low-, mid-, and alternating-bit configurations
    let sample_masks = |sites: usize, slices: usize| -> Vec<usize> {
        let total_bits = (sites * slices).min(usize::BITS as usize - 2);
        let all_ones = (1usize << total_bits) - 1;
        let alt_a = 0x5555_5555usize & all_ones;
        let alt_b = 0xAAAA_AAAAusize & all_ones;
        vec![
            0,
            1,
            (1usize << sites.min(total_bits)) - 1,
            alt_a,
            alt_b,
            all_ones,
        ]
    };

    let configs: Vec<(&str, usize, Vec<(usize, usize)>, usize, BigRational, bool)> = vec![
        ("plaquette_2x2_attractive", 4, bonds_2x2, 2, unit_fugacity.clone(), true),
        ("grid_2x3_attractive", 6, bonds_2x3, 2, unit_fugacity.clone(), true),
        ("grid_2x4_attractive", 8, bonds_2x4, 2, unit_fugacity.clone(), true),
        ("grid_3x3_attractive", 9, bonds_3x3, 1, unit_fugacity.clone(), true),
        ("ring_10_attractive", 10, bonds_1x10, 1, unit_fugacity.clone(), true),
        ("grid_3x4_attractive", 12, bonds_3x4, 1, unit_fugacity, true),
        ("frustrated_2x3_repulsive_doped", 6, frust_2x3, 2, doped_fugacity.clone(), false),
        ("frustrated_3x3_repulsive_doped", 9, frust_3x3, 1, doped_fugacity, false),
    ];

    let mut rows = Vec::with_capacity(configs.len());
    for (label, sites, bonds, slices, fugacity, attractive) in configs {
        let masks = sample_masks(sites, slices);
        let summary = evaluate_hubbard_determinants(
            sites,
            &bonds,
            slices,
            &r,
            &hs,
            &fugacity,
            attractive,
            &masks,
        )?;
        rows.push(HubbardLatticeScalingRow {
            label: label.to_string(),
            sites,
            num_bonds: bonds.len(),
            slices,
            attractive,
            evaluated_fields: summary.total_fields,
            negative_fields_count: summary.negative_fields_count,
            zero_fields_count: summary.zero_fields_count,
            average_sign: summary.average_sign,
            attractive_square_root_protected: summary.attractive_square_root_protected,
        });
    }

    Ok(rows)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exact_determinant_2x2_and_3x3() {
        // [ [1, 2], [3, 4] ] -> 4 - 6 = -2
        let m2 = vec![
            vec![BigRational::from(BigInt::from(1)), BigRational::from(BigInt::from(2))],
            vec![BigRational::from(BigInt::from(3)), BigRational::from(BigInt::from(4))],
        ];
        assert_eq!(exact_determinant(&m2).unwrap(), -BigRational::from(BigInt::from(2)));

        // Identity 3x3
        let mut m3 = vec![vec![BigRational::zero(); 3]; 3];
        for i in 0..3 {
            m3[i][i] = BigRational::one();
        }
        assert_eq!(exact_determinant(&m3).unwrap(), BigRational::one());
    }

    #[test]
    fn attractive_hubbard_square_root_symmetry_on_square_plaquette() {
        // 4 sites, square plaquette
        let bonds = vec![(0, 1), (1, 2), (2, 3), (3, 0)];
        let r = BigRational::new(BigInt::from(3), BigInt::from(2));
        let hs = BigRational::from(BigInt::from(2));
        let fugacity = BigRational::one();
        let masks = vec![0, 1, 5, 15]; // Sample fields

        let summary = evaluate_hubbard_determinants(
            4,
            &bonds,
            1,
            &r,
            &hs,
            &fugacity,
            true, // attractive Hubbard
            &masks,
        )
        .unwrap();

        assert_eq!(summary.negative_fields_count, 0);
        assert!(summary.attractive_square_root_protected);
        assert_eq!(summary.average_sign, BigRational::one());
    }

    #[test]
    fn hubbard_lattice_scaling_up_to_12_sites() {
        let rows = benchmark_hubbard_lattice_scaling().unwrap();
        assert_eq!(rows.len(), 8);

        let expected_sites = [4usize, 6, 8, 9, 10, 12, 6, 9];
        for (i, row) in rows.iter().enumerate() {
            assert_eq!(row.sites, expected_sites[i], "label={}", row.label);
            assert_eq!(row.evaluated_fields, 6, "label={}", row.label);
            if row.attractive {
                assert_eq!(
                    row.negative_fields_count, 0,
                    "attractive model {} had negative fields",
                    row.label
                );
                assert!(
                    row.attractive_square_root_protected,
                    "attractive model {} lost square-root protection",
                    row.label
                );
                assert_eq!(
                    row.average_sign,
                    BigRational::one(),
                    "attractive model {} had average_sign != 1",
                    row.label
                );
            } else {
                assert!(!row.attractive_square_root_protected);
                assert!(
                    row.average_sign <= BigRational::one(),
                    "repulsive model {} had average_sign > 1",
                    row.label
                );
            }
        }
    }

    #[test]
    fn hubbard_lattice_scaling_matches_cross_language_json_fixture_bit_for_bit() {
        let rows = benchmark_hubbard_lattice_scaling().unwrap();
        let serialized = hubbard_scaling_to_canonical_json(&rows).unwrap();
        let fixture = include_str!("fixtures/hubbard_lattice_scaling.json").replace("\r\n", "\n");
        assert_eq!(
            serialized.as_bytes(),
            fixture.as_bytes(),
            "Rust benchmark_hubbard_lattice_scaling JSON output drifted from cross-language fixture"
        );
        let round_trip = hubbard_scaling_from_canonical_json(&fixture).unwrap();
        assert_eq!(round_trip, rows);
    }

    #[test]
    fn exact_determinant_row_swap_and_hubbard_boundary_refusals() {
        // 2x2 permutation matrix [[0, 1], [1, 0]] requires a pivot row swap and has det = -1
        let swap2 = vec![
            vec![BigRational::zero(), BigRational::one()],
            vec![BigRational::one(), BigRational::zero()],
        ];
        assert_eq!(exact_determinant(&swap2).unwrap(), -BigRational::one());

        // 3x3 single row-swap permutation [[0, 1, 0], [1, 0, 0], [0, 0, 1]] -> det = -1
        let swap3 = vec![
            vec![BigRational::zero(), BigRational::one(), BigRational::zero()],
            vec![BigRational::one(), BigRational::zero(), BigRational::zero()],
            vec![BigRational::zero(), BigRational::zero(), BigRational::one()],
        ];
        assert_eq!(exact_determinant(&swap3).unwrap(), -BigRational::one());

        // 3x3 double row-swap cyclic permutation [[0, 1, 0], [0, 0, 1], [1, 0, 0]] -> det = +1
        let cyc3 = vec![
            vec![BigRational::zero(), BigRational::one(), BigRational::zero()],
            vec![BigRational::zero(), BigRational::zero(), BigRational::one()],
            vec![BigRational::one(), BigRational::zero(), BigRational::zero()],
        ];
        assert_eq!(exact_determinant(&cyc3).unwrap(), BigRational::one());

        // Boundary refusals: non-square determinant, zero hs, bit-width overflow, empty masks
        let ragged = vec![vec![BigRational::one(), BigRational::zero()]];
        assert!(exact_determinant(&ragged).is_err());

        let bonds = vec![(0, 1)];
        let r = BigRational::new(BigInt::from(3), BigInt::from(2));
        let hs = BigRational::from(BigInt::from(2));
        let fugacity = BigRational::one();
        assert!(evaluate_hubbard_determinants(
            2,
            &bonds,
            1,
            &r,
            &BigRational::zero(),
            &fugacity,
            true,
            &[0]
        )
        .is_err());
        assert!(evaluate_hubbard_determinants(
            8,
            &bonds,
            8,
            &r,
            &hs,
            &fugacity,
            true,
            &[0]
        )
        .is_err());
        assert!(evaluate_hubbard_determinants(
            2,
            &bonds,
            1,
            &r,
            &hs,
            &fugacity,
            true,
            &[]
        )
        .is_err());
    }
}
