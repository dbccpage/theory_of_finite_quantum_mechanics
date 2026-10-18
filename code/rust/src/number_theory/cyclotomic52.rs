
use num_rational::BigRational;
use num_traits::{One, Zero};

use crate::rational::ri;

const DEGREE: usize = 24;

const PHI52_LOW: [i64; DEGREE] = [
    1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0,
];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Cyc52 {
    pub a: [BigRational; DEGREE],
}

impl Cyc52 {
    pub fn zero() -> Self {
        Cyc52 {
            a: std::array::from_fn(|_| BigRational::zero()),
        }
    }

    pub fn rat(x: BigRational) -> Self {
        let mut c = Cyc52::zero();
        c.a[0] = x;
        c
    }

    pub fn zeta(p: i32) -> Self {
        let p = p.rem_euclid(52) as usize;
        let mut dense = vec![BigRational::zero(); 52];
        dense[p] = BigRational::one();
        Cyc52 {
            a: reduce_dense(dense),
        }
    }

    pub fn add(&self, o: &Cyc52) -> Cyc52 {
        Cyc52 {
            a: std::array::from_fn(|i| &self.a[i] + &o.a[i]),
        }
    }

    pub fn sub(&self, o: &Cyc52) -> Cyc52 {
        Cyc52 {
            a: std::array::from_fn(|i| &self.a[i] - &o.a[i]),
        }
    }

    pub fn mul(&self, o: &Cyc52) -> Cyc52 {
        let mut prod = vec![BigRational::zero(); 2 * DEGREE - 1];
        for (i, x) in self.a.iter().enumerate() {
            if !x.is_zero() {
                for (j, y) in o.a.iter().enumerate() {
                    if !y.is_zero() {
                        prod[i + j] += x * y;
                    }
                }
            }
        }
        Cyc52 {
            a: reduce_dense(prod),
        }
    }

    pub fn conj(&self) -> Cyc52 {
        let mut out = Cyc52::zero();
        for (k, x) in self.a.iter().enumerate() {
            if !x.is_zero() {
                let zk = Cyc52::zeta(-(k as i32));
                for i in 0..DEGREE {
                    out.a[i] += x * &zk.a[i];
                }
            }
        }
        out
    }

    pub fn inv(&self) -> Cyc52 {
        let cols: [[BigRational; DEGREE]; DEGREE] = std::array::from_fn(|k| {
            let mut e = Cyc52::zero();
            e.a[k] = BigRational::one();
            self.mul(&e).a
        });
        let mut a: [[BigRational; DEGREE + 1]; DEGREE] = std::array::from_fn(|i| {
            std::array::from_fn(|j| {
                if j < DEGREE {
                    cols[j][i].clone()
                } else if i == 0 {
                    BigRational::one()
                } else {
                    BigRational::zero()
                }
            })
        });
        for col in 0..DEGREE {
            let piv = (col..DEGREE)
                .find(|&r| !a[r][col].is_zero())
                .expect("Cyc52::inv on a non-invertible element");
            a.swap(col, piv);
            let pv = a[col][col].clone();
            for x in a[col].iter_mut() {
                *x /= &pv;
            }
            for r in 0..DEGREE {
                if r != col && !a[r][col].is_zero() {
                    let f = a[r][col].clone();
                    for c in 0..=DEGREE {
                        let t = &f * &a[col][c];
                        a[r][c] -= t;
                    }
                }
            }
        }
        Cyc52 {
            a: std::array::from_fn(|i| a[i][DEGREE].clone()),
        }
    }

    pub fn is_zero(&self) -> bool {
        self.a.iter().all(|x| x.is_zero())
    }
}

pub fn c1_52() -> Cyc52 {
    Cyc52::rat(ri(1))
}

pub fn icyc_52() -> Cyc52 {
    Cyc52::zeta(13)
}

pub fn sqrt13_52() -> Cyc52 {
    gauss13_52()
}

fn gauss13_52() -> Cyc52 {
    let mut sum = Cyc52::zero();
    for x in 0_i32..13 {
        sum = sum.add(&Cyc52::zeta(4 * x * x));
    }
    sum
}

fn reduce_dense(mut dense: Vec<BigRational>) -> [BigRational; DEGREE] {
    if dense.len() < DEGREE {
        dense.resize(DEGREE, BigRational::zero());
    }
    for k in (DEGREE..dense.len()).rev() {
        if !dense[k].is_zero() {
            let v = dense[k].clone();
            for j in 0..DEGREE {
                if PHI52_LOW[j] != 0 {
                    dense[k - DEGREE + j] -= &v * ri(PHI52_LOW[j]);
                }
            }
            dense[k] = BigRational::zero();
        }
    }
    std::array::from_fn(|i| dense[i].clone())
}

impl Cyc52 {
    pub fn scale_rat(&self, r: &BigRational) -> Self {
        Cyc52 {
            a: std::array::from_fn(|i| &self.a[i] * r),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn zeta52_reduces_by_declared_cyclotomic_polynomial() {
        assert_eq!(Cyc52::zeta(52), c1_52());
        assert_eq!(Cyc52::zeta(26), Cyc52::rat(ri(-1)));
        let mut phi = Cyc52::zero();
        for k in (0_i32..=24).step_by(2) {
            let sign = if (k / 2) % 2 == 0 { 1 } else { -1 };
            let term = Cyc52::zeta(k);
            phi = if sign == 1 {
                phi.add(&term)
            } else {
                phi.sub(&term)
            };
        }
        assert!(phi.is_zero());
    }

    #[test]
    fn sqrt13_and_i_identities_hold_in_q_zeta52() {
        assert_eq!(icyc_52().mul(&icyc_52()), Cyc52::rat(ri(-1)));
        assert_eq!(sqrt13_52().mul(&sqrt13_52()), Cyc52::rat(ri(13)));
        assert_eq!(sqrt13_52().mul(&sqrt13_52().inv()), c1_52());
    }
}
