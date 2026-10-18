
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Witness {
    pub triangles_k5: i64,
    pub triangles_k6: i64,
    pub cayley_menger_det: i64,
    pub signed_volume_factor: i64,
    pub triangle_area_sq: (i64, i64),
    pub star_area_sq_k5: (i64, i64),
    pub apex_cosine: (i64, i64),
    pub apex_sin_sq: (i64, i64),
    pub turn_sum_k5: (i64, i64),
    pub turn_deficit_k5: (i64, i64),
    pub turn_deficit_k6: (i64, i64),
    pub radian_deficit_lo: (i64, i64),
    pub radian_deficit_hi: (i64, i64),
}

pub fn cayley_menger_det_2simplex(s1: i64, s2: i64, b: i64) -> i64 {
    let m: [[i64; 4]; 4] = [
        [0, 1, 1, 1],
        [1, 0, s1, s2],
        [1, s1, 0, b],
        [1, s2, b, 0],
    ];
    det4(m)
}

fn det3(m: [[i64; 3]; 3]) -> i64 {
    m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
}

fn det4(m: [[i64; 4]; 4]) -> i64 {
    let mut total = 0;
    for col in 0..4 {
        let mut sub = [[0_i64; 3]; 3];
        for r in 1..4 {
            let mut c_idx = 0;
            for c in 0..4 {
                if c != col {
                    sub[r - 1][c_idx] = m[r][c];
                    c_idx += 1;
                }
            }
        }
        let sign = if col % 2 == 0 { 1 } else { -1 };
        total += sign * m[0][col] * det3(sub);
    }
    total
}

fn reduce(num: i64, den: i64) -> (i64, i64) {
    let g = gcd(num, den);
    (num / g, den / g)
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

pub fn witness() -> Witness {
    let cm_det = cayley_menger_det_2simplex(1, 1, 1);
    let signed_vol = -cm_det;
    assert_eq!(cm_det, -3);
    assert_eq!(signed_vol, 3);
    Witness {
        triangles_k5: 5,
        triangles_k6: 6,
        cayley_menger_det: cm_det,
        signed_volume_factor: signed_vol,
        triangle_area_sq: reduce(signed_vol, 16),
        star_area_sq_k5: reduce(25 * signed_vol, 16),
        apex_cosine: reduce(1 + 1 - 1, 2),
        apex_sin_sq: reduce(signed_vol, 4),
        turn_sum_k5: reduce(5, 6),
        turn_deficit_k5: reduce(1, 6),
        turn_deficit_k6: (0, 1),
        radian_deficit_lo: reduce(1_047_197_551, 1_000_000_000),
        radian_deficit_hi: reduce(1_047_197_552, 1_000_000_000),
    }
}

pub fn reject_pinned_cm_determinant(det_value: i64) -> Result<(), &'static str> {
    if det_value == 3 {
        Err("unit equilateral 2-simplex 4x4 Cayley-Menger determinant is -3, not +3")
    } else {
        Ok(())
    }
}

pub fn reject_unproved_continuum_bound(claim: &str) -> Result<(), &'static str> {
    if claim.contains("|E(a)| <= (1/6) * a^2") || claim.contains("Ricci") {
        Err("a single five-triangle star does not establish a continuum Ricci error bound")
    } else {
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::{
        cayley_menger_det_2simplex, reject_pinned_cm_determinant,
        reject_unproved_continuum_bound, witness,
    };

    #[test]
    fn cayley_menger_sign_and_degeneracy_are_exact() {
        assert_eq!(cayley_menger_det_2simplex(1, 1, 1), -3);
        assert_eq!(cayley_menger_det_2simplex(1, 1, 4), 0);
        assert_eq!(cayley_menger_det_2simplex(1, 1, 9), 45);
    }

    #[test]
    fn five_triangle_star_witness_is_exact() {
        let w = witness();
        assert_eq!(w.cayley_menger_det, -3);
        assert_eq!(w.signed_volume_factor, 3);
        assert_eq!(w.triangle_area_sq, (3, 16));
        assert_eq!(w.star_area_sq_k5, (75, 16));
        assert_eq!(w.apex_cosine, (1, 2));
        assert_eq!(w.apex_sin_sq, (3, 4));
        assert_eq!(w.turn_sum_k5, (5, 6));
        assert_eq!(w.turn_deficit_k5, (1, 6));
        assert_eq!(w.turn_deficit_k6, (0, 1));
    }

    #[test]
    fn pinned_determinant_and_continuum_string_are_refused() {
        assert!(reject_pinned_cm_determinant(3).is_err());
        assert!(reject_pinned_cm_determinant(-3).is_ok());
        assert!(reject_unproved_continuum_bound("|E(a)| <= (1/6) * a^2").is_err());
    }
}
