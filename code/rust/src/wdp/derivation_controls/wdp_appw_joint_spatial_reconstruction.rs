
const SITES: i64 = 4;
const M_LABEL: i64 = 1;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Rat {
    num: i64,
    den: i64,
}

fn gcd(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let rest = a % b;
        a = b;
        b = rest;
    }
    if a == 0 { 1 } else { a }
}

impl Rat {
    fn new(num: i64, den: i64) -> Self {
        assert!(den != 0, "zero denominator");
        let mut num = num;
        let mut den = den;
        if den < 0 {
            num = num.checked_neg().expect("numerator sign");
            den = -den;
        }
        let g = gcd(num, den);
        Self { num: num / g, den: den / g }
    }
}

fn mod_one(num: i64, den: i64) -> Option<(i64, i64)> {
    if den == 0 {
        return None;
    }
    let reduced = Rat::new(num, den);
    Some((reduced.num.rem_euclid(reduced.den), reduced.den))
}

fn exp_two_pi_i(num: i64, den: i64) -> Option<(i64, i64)> {
    let (n, d) = mod_one(num, den)?;
    if n == 0 {
        Some((1, 0))
    } else if n.checked_mul(2)? == d {
        Some((-1, 0))
    } else {
        None
    }
}

fn half_steps(m: i64) -> i64 {
    assert!(m >= 1, "M is at least 1");
    m.checked_mul(2).expect("N=2M")
}

fn response_order(sites: i64, n: i64) -> i64 {
    sites.checked_mul(n).expect("LN")
}

fn prefactors(sites: i64, n: i64) -> (Rat, Rat) {
    let order = response_order(sites, n);
    let order_sq = order.checked_mul(order).expect("(LN)^2");
    let n_sq = n.checked_mul(n).expect("N^2");
    let quad_den = sites.checked_mul(n_sq).expect("L N^2");
    let left = (sites as i128)
        .checked_mul(sites as i128)
        .and_then(|value| value.checked_mul(n_sq as i128))
        .expect("cross term");
    assert_eq!(left, order_sq as i128, "L*(1/(LN))^2 is not 1/(L N^2)");
    (Rat::new(sites, order_sq), Rat::new(1, quad_den))
}

fn grid_sample() -> [(i64, i64); 4] {
    let mut sample = [(0i64, 0i64); 4];
    for x in 0..4 {
        let turns = SITES.checked_mul(x as i64).expect("L*x");
        sample[x] = exp_two_pi_i(turns, SITES).expect("integer turn on the four sites");
    }
    sample
}

fn constant_profile() -> [i64; 4] {
    let mut profile = [0i64; 4];
    for value in &mut profile {
        *value = 1;
    }
    profile
}

fn off_grid_sample() -> (i64, i64) {
    let turns = SITES.checked_mul(1).expect("L*xi");
    exp_two_pi_i(turns, 8).expect("half-integer turn")
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Witness {
    pub sites: i64,
    pub fock_dimension: i64,
    pub m: i64,
    pub n: i64,
    pub response_order: i64,
    pub cell_prefactor_num: i64,
    pub cell_prefactor_den: i64,
    pub quadratic_prefactor_num: i64,
    pub quadratic_prefactor_den: i64,
    pub grid_real: [i64; 4],
    pub grid_imag: [i64; 4],
    pub constant_real: [i64; 4],
    pub off_grid_real: i64,
    pub off_grid_imag: i64,
    pub samples_collide: bool,
    pub reconstruction_defined: bool,
    pub joint_limit: bool,
    pub variable_l: bool,
    pub kernel_reconstructed: bool,
    pub continuum_limit: bool,
}

pub fn witness() -> Witness {
    assert_eq!(SITES, 4, "carrier fixes four periodic sites");
    assert_eq!(M_LABEL, 1, "labelled point is M=1");
    let n = half_steps(M_LABEL);
    let order = response_order(SITES, n);
    assert_eq!(n, 2, "N=2M at M=1");
    assert_eq!(order, 8, "response order is LN=8 at M=1");
    assert_eq!(order, 8 * M_LABEL, "response order is 8M");
    let fock_dimension = 1i64 << SITES;
    assert_eq!(fock_dimension, 16, "CAR Fock space has dimension 2^4");

    let (cell, quad) = prefactors(SITES, n);
    let sixteen_m2 = 16i64
        .checked_mul(M_LABEL)
        .and_then(|value| value.checked_mul(M_LABEL))
        .expect("16 M^2");
    assert_eq!(cell, quad, "cell prefactor differs from 1/(L N^2)");
    assert_eq!(cell, Rat::new(1, sixteen_m2), "prefactor is not 1/(16 M^2)");
    assert_eq!(cell, Rat::new(4, order * order), "4/(LN)^2 differs from the cell prefactor");
    assert_eq!(cell, Rat::new(1, 16), "M=1 prefactor is not 1/16");

    let grid = grid_sample();
    let constant_real = constant_profile();
    let mut grid_real = [0i64; 4];
    let mut grid_imag = [0i64; 4];
    for index in 0..4 {
        grid_real[index] = grid[index].0;
        grid_imag[index] = grid[index].1;
        assert_eq!(grid_imag[index], 0, "grid sample is not real");
    }
    let samples_collide = grid_real == constant_real;
    assert!(samples_collide, "grid sample did not collide with the constant profile");

    let (off_grid_real, off_grid_imag) = off_grid_sample();
    assert_eq!((off_grid_real, off_grid_imag), (-1, 0), "cos(pi) is not -1");
    assert_ne!(off_grid_real, constant_real[0], "off-grid value collapsed onto the constant");

    Witness {
        sites: SITES,
        fock_dimension,
        m: M_LABEL,
        n,
        response_order: order,
        cell_prefactor_num: cell.num,
        cell_prefactor_den: cell.den,
        quadratic_prefactor_num: quad.num,
        quadratic_prefactor_den: quad.den,
        grid_real,
        grid_imag,
        constant_real,
        off_grid_real,
        off_grid_imag,
        samples_collide,
        reconstruction_defined: false,
        joint_limit: false,
        variable_l: false,
        kernel_reconstructed: false,
        continuum_limit: false,
    }
}

pub fn refuse_joint_spatial_reconstruction() -> Result<(), &'static str> {
    let report = witness();
    let fixed_carrier = report.sites == 4
        && report.fock_dimension == 16
        && report.m == 1
        && report.n == 2
        && report.response_order == 8
        && !report.variable_l;
    let prefactor = report.cell_prefactor_num == 1
        && report.cell_prefactor_den == 16
        && report.quadratic_prefactor_num == 1
        && report.quadratic_prefactor_den == 16;
    let alias = report.samples_collide
        && report.grid_real == [1, 1, 1, 1]
        && report.grid_imag == [0, 0, 0, 0]
        && report.constant_real == [1, 1, 1, 1]
        && report.off_grid_real == -1
        && report.off_grid_imag == 0;
    let closed = report.reconstruction_defined
        || report.joint_limit
        || report.kernel_reconstructed
        || report.continuum_limit;
    if fixed_carrier && prefactor && alias && !closed {
        return Err("L=4 and M=1 do not reconstruct K or close a joint (L,M) limit");
    }
    Err("selected carrier identities were not met")
}

#[cfg(test)]
mod tests {
    use super::{refuse_joint_spatial_reconstruction, witness};

    #[test]
    fn exact_prefactor_and_grid_collision() {
        let report = witness();
        assert_eq!(report.sites, 4);
        assert_eq!(report.fock_dimension, 16);
        assert_eq!(report.m, 1);
        assert_eq!(report.n, 2);
        assert_eq!(report.response_order, 8);
        assert_eq!((report.cell_prefactor_num, report.cell_prefactor_den), (1, 16));
        assert_eq!(
            (report.quadratic_prefactor_num, report.quadratic_prefactor_den),
            (1, 16)
        );
        assert_eq!(report.grid_real, [1, 1, 1, 1]);
        assert_eq!(report.grid_imag, [0, 0, 0, 0]);
        assert_eq!(report.constant_real, [1, 1, 1, 1]);
        assert!(report.samples_collide);
        assert_eq!((report.off_grid_real, report.off_grid_imag), (-1, 0));
        assert!(!report.reconstruction_defined);
        assert!(!report.joint_limit);
        assert!(!report.variable_l);
        assert!(!report.kernel_reconstructed);
        assert!(!report.continuum_limit);
    }

    #[test]
    fn joint_spatial_reconstruction_is_refused() {
        assert_eq!(
            refuse_joint_spatial_reconstruction(),
            Err("L=4 and M=1 do not reconstruct K or close a joint (L,M) limit")
        );
    }
}
