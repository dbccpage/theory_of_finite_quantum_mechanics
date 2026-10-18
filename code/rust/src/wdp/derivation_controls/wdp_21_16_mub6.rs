
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Witness {
    pub tao_column_sums: [i64; 6],
    pub tao_column_residues_mod3: [i64; 6],
    pub tao_residue_counts: (i64, i64, i64),
    pub tao_eisenstein_norm_sq: i64,
    pub alpha_2_values: [i64; 4],
    pub parity_pair_sums: [i64; 4],
    pub synthetic_nerve_sum_012: i64,
    pub synthetic_coboundary_cycle_sum: i64,
    pub spectral_floor_frac: (i64, i64),
    pub lookup_haagerup_rows: i64,
    pub external_haagerup_minus_one_rows: i64,
}

const TAO_PHASE_TABLE: [[i64; 6]; 6] = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
];

const GAMMA_1: [i64; 6] = [1, 1, 1, -1, -1, -1];

pub fn witness() -> Witness {
    let mut col_sums = [0_i64; 6];
    let mut residues = [0_i64; 6];
    let (mut n0, mut n1, mut n2) = (0_i64, 0_i64, 0_i64);
    for c in 0..6 {
        let mut s = 0_i64;
        for r in 0..6 {
            s += GAMMA_1[r] * TAO_PHASE_TABLE[r][c];
        }
        col_sums[c] = s;
        let res = s.rem_euclid(3);
        residues[c] = res;
        match res {
            0 => n0 += 1,
            1 => n1 += 1,
            _ => n2 += 1,
        }
    }
    let x = n0 - n2;
    let y = n1 - n2;
    let norm_sq = x * x - x * y + y * y;
    let mut alpha_2 = [0_i64; 4];
    let mut parity_sums = [0_i64; 4];
    for m in 0..4 {
        let a = 6 * (m as i64) - 9;
        alpha_2[m] = a;
        let sign = if a.rem_euclid(2) == 0 { 1 } else { -1 };
        parity_sums[m] = 1 + sign;
    }
    let alpha_pot = [7_i64, -3, 11];
    let coboundary_sum =
        (alpha_pot[1] - alpha_pot[0]) + (alpha_pot[2] - alpha_pot[1]) + (alpha_pot[0] - alpha_pot[2]);
    Witness {
        tao_column_sums: col_sums,
        tao_column_residues_mod3: residues,
        tao_residue_counts: (n0, n1, n2),
        tao_eisenstein_norm_sq: norm_sq,
        alpha_2_values: alpha_2,
        parity_pair_sums: parity_sums,
        synthetic_nerve_sum_012: 4045 + 4044 + 4044,
        synthetic_coboundary_cycle_sum: coboundary_sum,
        spectral_floor_frac: (31, 800),
        lookup_haagerup_rows: 1,
        external_haagerup_minus_one_rows: 5,
    }
}

pub fn reject_moduli_phi1_coverage_claim(value: i64) -> Result<(), &'static str> {
    if value == 9 || value == 12133 || value == 0 {
        Err("labelled finite carrier values 9, 0, and 12133 do not certify WDP Phi_1 coverage on CHM(6)")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{reject_moduli_phi1_coverage_claim, witness};

    #[test]
    fn four_labelled_carriers_match_derivation() {
        let w = witness();
        assert_eq!(w.tao_column_sums, [0, -4, -4, 0, 2, 0]);
        assert_eq!(w.tao_column_residues_mod3, [0, 2, 2, 0, 2, 0]);
        assert_eq!(w.tao_residue_counts, (3, 0, 3));
        assert_eq!(w.tao_eisenstein_norm_sq, 9);
        assert_eq!(w.alpha_2_values, [-9, -3, 3, 9]);
        assert_eq!(w.parity_pair_sums, [0, 0, 0, 0]);
        assert_eq!(w.synthetic_nerve_sum_012, 12133);
        assert_eq!(w.synthetic_coboundary_cycle_sum, 0);
        assert_eq!(w.spectral_floor_frac, (31, 800));
        assert_ne!(w.lookup_haagerup_rows, w.external_haagerup_minus_one_rows);
    }

    #[test]
    fn moduli_coverage_promotion_is_refused() {
        assert!(reject_moduli_phi1_coverage_claim(9).is_err());
        assert!(reject_moduli_phi1_coverage_claim(12133).is_err());
    }
}
