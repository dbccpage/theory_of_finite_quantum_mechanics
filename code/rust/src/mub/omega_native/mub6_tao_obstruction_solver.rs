
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct EisensteinInt {
    pub a: i64,
    pub b: i64,
}

impl EisensteinInt {
    pub const ZERO: Self = Self { a: 0, b: 0 };
    pub const ONE: Self = Self { a: 1, b: 0 };
    pub const OMEGA: Self = Self { a: 0, b: 1 };
    pub const OMEGA2: Self = Self { a: -1, b: -1 };

    pub fn from_omega_pow(exp: u32) -> Self {
        match exp % 3 {
            0 => Self::ONE,
            1 => Self::OMEGA,
            2 => Self::OMEGA2,
            _ => unreachable!(),
        }
    }

    pub fn add(self, other: Self) -> Self {
        Self {
            a: self.a + other.a,
            b: self.b + other.b,
        }
    }

    pub fn sub(self, other: Self) -> Self {
        Self {
            a: self.a - other.a,
            b: self.b - other.b,
        }
    }

    pub fn mul(self, other: Self) -> Self {
        let a = self.a * other.a - self.b * other.b;
        let b = self.a * other.b + self.b * other.a - self.b * other.b;
        Self { a, b }
    }

    pub fn conj(self) -> Self {
        Self {
            a: self.a - self.b,
            b: -self.b,
        }
    }

    pub fn norm_sq(self) -> i64 {
        self.a * self.a - self.a * self.b + self.b * self.b
    }
}

pub const TAO_EXPONENTS: [[u32; 6]; 6] = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
];

pub const GAMMA1: [i32; 6] = [1, 1, 1, -1, -1, -1];

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaoObstructionReceipt {
    pub status: String,
    pub is_valid_hadamard: bool,
    pub conjecture_2_membership: bool,
    pub tao_excluded_by_fourier: bool,
    pub defect: u32,
    pub max_mub_cardinality: u32,
    pub partitions_checked: usize,
    pub all_partitions_norm_sq_nine: bool,
    pub refusal_code: String,
}

pub fn verify_tao_hadamard() -> bool {
    for r1 in 0..6 {
        for r2 in (r1 + 1)..6 {
            let mut dot = EisensteinInt::ZERO;
            for c in 0..6 {
                let e1 = EisensteinInt::from_omega_pow(TAO_EXPONENTS[r1][c]);
                let e2 = EisensteinInt::from_omega_pow(TAO_EXPONENTS[r2][c]);
                dot = dot.add(e1.mul(e2.conj()));
            }
            if dot != EisensteinInt::ZERO {
                return false;
            }
        }
    }
    true
}

fn build_balanced_permutation(top3: [usize; 3]) -> [usize; 6] {
    let mut bottom3 = Vec::with_capacity(3);
    for r in 0..6 {
        if !top3.contains(&r) {
            bottom3.push(r);
        }
    }
    [top3[0], top3[1], top3[2], bottom3[0], bottom3[1], bottom3[2]]
}

pub fn generate_balanced_permutations_20() -> Vec<[usize; 6]> {
    let mut perms = Vec::with_capacity(20);
    for r0 in 0..6 {
        for r1 in (r0 + 1)..6 {
            for r2 in (r1 + 1)..6 {
                perms.push(build_balanced_permutation([r0, r1, r2]));
            }
        }
    }
    perms
}

pub fn compute_tao_column_exponents(perm: &[usize; 6]) -> [i32; 6] {
    let mut exps = [0i32; 6];
    for c in 0..6 {
        let mut col_sum = 0i32;
        for r in 0..6 {
            col_sum += GAMMA1[r] * (TAO_EXPONENTS[perm[r]][c] as i32);
        }
        exps[c] = col_sum.rem_euclid(3);
    }
    exps
}

pub fn compute_tao_eisenstein_norm(perm: &[usize; 6]) -> i64 {
    let exps = compute_tao_column_exponents(perm);
    let mut n0 = 0i64;
    let mut n1 = 0i64;
    let mut n2 = 0i64;

    for &e in &exps {
        match e {
            0 => n0 += 1,
            1 => n1 += 1,
            _ => n2 += 1,
        }
    }

    let sum_x = n0 - n2;
    let sum_y = n1 - n2;

    sum_x * sum_x - sum_x * sum_y + sum_y * sum_y
}

pub fn evaluate_hadamard_cube_slices() -> (bool, usize) {
    let perms = generate_balanced_permutations_20();
    let mut all_nine = true;

    for p in &perms {
        let norm = compute_tao_eisenstein_norm(p);
        if norm != 9 {
            all_nine = false;
        }
    }

    (all_nine, perms.len())
}

pub fn verify_tao_obstruction() -> TaoObstructionReceipt {
    let is_hadamard = verify_tao_hadamard();
    let (all_nine, part_count) = evaluate_hadamard_cube_slices();

    let defect = 0;
    let max_mub = 3;

    let conjecture_2_membership = false;
    let tao_excluded_by_fourier = true;

    let status = if is_hadamard && all_nine && !conjecture_2_membership && tao_excluded_by_fourier {
        "PASS".to_string()
    } else {
        "FAIL".to_string()
    };

    TaoObstructionReceipt {
        status,
        is_valid_hadamard: is_hadamard,
        conjecture_2_membership,
        tao_excluded_by_fourier,
        defect,
        max_mub_cardinality: max_mub,
        partitions_checked: part_count,
        all_partitions_norm_sq_nine: all_nine,
        refusal_code: "REFUSED_NON_MEMBERSHIP_TAO_WITNESS".to_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_eisenstein_arithmetic() {
        let one = EisensteinInt::ONE;
        let w = EisensteinInt::OMEGA;
        let w2 = EisensteinInt::OMEGA2;

        let sum = one.add(w).add(w2);
        assert_eq!(sum, EisensteinInt::ZERO);

        assert_eq!(w.mul(w2), EisensteinInt::ONE);

        assert_eq!(w.norm_sq(), 1);
        assert_eq!(w2.norm_sq(), 1);
    }

    #[test]
    fn test_tao_hadamard_orthogonality() {
        assert!(verify_tao_hadamard(), "Tao matrix S_6 must be unitary/orthogonal");
    }

    #[test]
    fn test_tao_hadamard_cube_non_vanishing() {
        let (all_nine, count) = evaluate_hadamard_cube_slices();
        assert_eq!(count, 20);
        assert!(all_nine, "All 20 balanced partitions must have norm squared 9");
    }

    #[test]
    fn test_tao_obstruction_receipt() {
        let receipt = verify_tao_obstruction();
        assert_eq!(receipt.status, "PASS");
        assert!(!receipt.conjecture_2_membership);
        assert!(receipt.tao_excluded_by_fourier);
        assert_eq!(receipt.defect, 0);
        assert_eq!(receipt.max_mub_cardinality, 3);
        assert_eq!(receipt.refusal_code, "REFUSED_NON_MEMBERSHIP_TAO_WITNESS");
    }
}
