

use num_bigint::BigUint;
use num_integer::Integer;
use num_traits::ToPrimitive;
use engine_number_theory::rational::Rational;
use serde::{Deserialize, Serialize};

pub fn is_directed_subfield(m: u32, n: u32) -> bool {
    if m == 0 || n == 0 {
        false
    } else {
        n % m == 0
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct TargetConductorRecord {
    pub target_id: u32,
    pub name: &'static str,
    pub conductor: u32,
    pub field_desc: &'static str,
    pub real_subfield_desc: &'static str,
}

pub const TARGET_CONDUCTORS: [TargetConductorRecord; 23] = [
    TargetConductorRecord {
        target_id: 1,
        name: "Primitive Difference",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 2,
        name: "Simplicial Diamond Complex",
        conductor: 12,
        field_desc: "Q(zeta_12)",
        real_subfield_desc: "Q(sqrt(3))",
    },
    TargetConductorRecord {
        target_id: 3,
        name: "Sorkin 3-Slit Vanishing",
        conductor: 12,
        field_desc: "Q(zeta_12)",
        real_subfield_desc: "Q(sqrt(3))",
    },
    TargetConductorRecord {
        target_id: 4,
        name: "Rational Cayley Transform",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 5,
        name: "Pentagon Associator",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 6,
        name: "Cabello 18-Ray Contextuality",
        conductor: 12,
        field_desc: "Q(zeta_12)",
        real_subfield_desc: "Q(sqrt(3))",
    },
    TargetConductorRecord {
        target_id: 7,
        name: "Monotone Layer Admission",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 8,
        name: "Pythagorean Bell-CHSH",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 9,
        name: "3-Qubit Bit-Flip Code",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 10,
        name: "Bell Quantum Teleportation",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 11,
        name: "Superdense Coding Z[i]",
        conductor: 4,
        field_desc: "Q(i) = Q(zeta_4)",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 12,
        name: "CSS [[4, 2, 2]] Surface Code",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 13,
        name: "Prime-5 Gross Wigner Phase Space",
        conductor: 5,
        field_desc: "Q(zeta_5)",
        real_subfield_desc: "Q(sqrt(5))",
    },
    TargetConductorRecord {
        target_id: 14,
        name: "Shor [[9, 1, 3]] Code",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 15,
        name: "Discrete Phase Estimation",
        conductor: 4,
        field_desc: "Q(i) = Q(zeta_4)",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 16,
        name: "Surface Code Toric Topology",
        conductor: 2,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 17,
        name: "Grover Search N=4",
        conductor: 12,
        field_desc: "Q(zeta_12)",
        real_subfield_desc: "Q(sqrt(3))",
    },
    TargetConductorRecord {
        target_id: 18,
        name: "Discrete Clifford Sp(2n, F_2)",
        conductor: 8,
        field_desc: "Q(zeta_8)",
        real_subfield_desc: "Q(sqrt(2))",
    },
    TargetConductorRecord {
        target_id: 19,
        name: "Stone-von Neumann Obstruction",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 20,
        name: "Richardson Error Mitigation",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 21,
        name: "Cayley Graph Quantum Walk",
        conductor: 1,
        field_desc: "Q",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 22,
        name: "MUB State Tomography d=3",
        conductor: 3,
        field_desc: "Q(zeta_3)",
        real_subfield_desc: "Q",
    },
    TargetConductorRecord {
        target_id: 23,
        name: "Target 22 Ext: MUB d=4 Galois Field",
        conductor: 4,
        field_desc: "Q(i) = Q(zeta_4)",
        real_subfield_desc: "Q",
    },
];

pub fn compute_target_conductor_lcm() -> u32 {
    let conductors: Vec<u32> = TARGET_CONDUCTORS.iter().map(|t| t.conductor).collect();
    conductors
        .iter()
        .fold(BigUint::from(1u8), |a, &b| a.lcm(&BigUint::from(b)))
        .to_u32()
        .expect("bounded declared conductor LCM")
}

pub fn verify_target_lcm_conductor_embedding() -> bool {
    let n_star = compute_target_conductor_lcm();
    assert_eq!(n_star, 120, "Target LCM conductor must be exactly 120");
    TARGET_CONDUCTORS
        .iter()
        .all(|t| is_directed_subfield(t.conductor, n_star))
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VerifiedBornWeight {
    pub weight: Rational,
    pub is_real: bool,
    pub is_non_negative: bool,
}

impl VerifiedBornWeight {
    pub fn from_rational_amplitude(re: Rational, im: Rational) -> Self {
        use num_traits::Zero;
        let amplitude = engine_number_theory::cyclotomic::GaussianRat { re, im };
        let norm = amplitude.mul(&amplitude.conj());
        let norm_sq = norm.re;
        let non_neg = norm_sq >= Rational::zero();
        Self {
            weight: norm_sq,
            is_real: norm.im.is_zero(),
            is_non_negative: non_neg,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use engine_number_theory::rational::rq;

    #[test]
    fn test_gcd_and_lcm() {
        assert_eq!(Integer::gcd(&12u32, &18u32), 6);
        assert_eq!(Integer::lcm(&12u32, &18u32), 36);
        assert_eq!(Integer::lcm(&24u32, &5u32), 120);
    }

    #[test]
    fn test_directed_subfield_inclusion() {
        assert!(is_directed_subfield(1, 12));
        assert!(is_directed_subfield(3, 12));
        assert!(is_directed_subfield(4, 12));
        assert!(is_directed_subfield(12, 120));
        assert!(is_directed_subfield(5, 120));
        assert!(is_directed_subfield(8, 120));
        assert!(!is_directed_subfield(5, 12));
        assert!(!is_directed_subfield(8, 12));
    }

    #[test]
    fn test_target_conductor_lcm_is_120() {
        let n_star = compute_target_conductor_lcm();
        assert_eq!(n_star, 120);
        assert!(verify_target_lcm_conductor_embedding());
    }

    #[test]
    fn test_born_weights_non_negative_and_real() {
        let bw = VerifiedBornWeight::from_rational_amplitude(rq(3, 5), rq(4, 5));
        assert!(bw.is_real);
        assert!(bw.is_non_negative);
        assert_eq!(bw.weight, rq(1, 1));
    }
}
