
use num_rational::BigRational;
use num_traits::{One, Zero};

use crate::rational::ri;

const DEGREE: usize = 32;

const PHI120_LOW: [i64; DEGREE] = [
    1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
    0,
];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Cyc120 {
    pub a: [BigRational; DEGREE],
}

impl Cyc120 {
    pub fn zero() -> Self {
        Cyc120 {
            a: std::array::from_fn(|_| BigRational::zero()),
        }
    }

    pub fn rat(x: BigRational) -> Self {
        let mut c = Cyc120::zero();
        c.a[0] = x;
        c
    }

    pub fn zeta(p: i32) -> Self {
        let p = p.rem_euclid(120) as usize;
        let mut dense = vec![BigRational::zero(); 120];
        dense[p] = BigRational::one();
        Cyc120 {
            a: reduce_dense(dense),
        }
    }

    pub fn add(&self, o: &Cyc120) -> Cyc120 {
        Cyc120 {
            a: std::array::from_fn(|i| &self.a[i] + &o.a[i]),
        }
    }

    pub fn sub(&self, o: &Cyc120) -> Cyc120 {
        Cyc120 {
            a: std::array::from_fn(|i| &self.a[i] - &o.a[i]),
        }
    }

    pub fn neg(&self) -> Cyc120 {
        Cyc120 {
            a: std::array::from_fn(|i| -&self.a[i]),
        }
    }

    pub fn mul(&self, o: &Cyc120) -> Cyc120 {
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
        Cyc120 {
            a: reduce_dense(prod),
        }
    }

    pub fn conj(&self) -> Cyc120 {
        let mut out = Cyc120::zero();
        for (k, x) in self.a.iter().enumerate() {
            if !x.is_zero() {
                let zk = Cyc120::zeta(-(k as i32));
                for i in 0..DEGREE {
                    out.a[i] += x * &zk.a[i];
                }
            }
        }
        out
    }

    pub fn inv(&self) -> Cyc120 {
        let cols: [[BigRational; DEGREE]; DEGREE] = std::array::from_fn(|k| {
            let mut e = Cyc120::zero();
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
                .expect("Cyc120::inv on a non-invertible element");
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
        Cyc120 {
            a: std::array::from_fn(|i| a[i][DEGREE].clone()),
        }
    }

    pub fn is_zero(&self) -> bool {
        self.a.iter().all(|x| x.is_zero())
    }

    pub fn mul_rat(&self, r: &BigRational) -> Cyc120 {
        Cyc120 {
            a: std::array::from_fn(|i| &self.a[i] * r),
        }
    }
}

pub fn c1_120() -> Cyc120 {
    Cyc120::rat(ri(1))
}

pub fn icyc_120() -> Cyc120 {
    Cyc120::zeta(30)
}

pub fn sqrt2_120() -> Cyc120 {
    Cyc120::zeta(15).add(&Cyc120::zeta(-15))
}

pub fn sqrt5_120() -> Cyc120 {
    c1_120().add(&Cyc120::zeta(24).add(&Cyc120::zeta(-24)).mul_rat(&ri(2)))
}

fn reduce_dense(mut dense: Vec<BigRational>) -> [BigRational; DEGREE] {
    if dense.len() < DEGREE {
        dense.resize(DEGREE, BigRational::zero());
    }
    for k in (DEGREE..dense.len()).rev() {
        if !dense[k].is_zero() {
            let v = dense[k].clone();
            for j in 0..DEGREE {
                if PHI120_LOW[j] != 0 {
                    dense[k - DEGREE + j] -= &v * ri(PHI120_LOW[j]);
                }
            }
            dense[k] = BigRational::zero();
        }
    }
    std::array::from_fn(|i| dense[i].clone())
}

impl Cyc120 {
    pub fn scale_rat(&self, r: &BigRational) -> Self {
        Cyc120 {
            a: std::array::from_fn(|i| &self.a[i] * r),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn zeta120_reduces_by_declared_cyclotomic_polynomial() {
        assert_eq!(Cyc120::zeta(120), c1_120());
        assert_eq!(Cyc120::zeta(60), Cyc120::rat(ri(-1)));
        let phi = Cyc120::zeta(32)
            .add(&Cyc120::zeta(28))
            .sub(&Cyc120::zeta(20))
            .sub(&Cyc120::zeta(16))
            .sub(&Cyc120::zeta(12))
            .add(&Cyc120::zeta(4))
            .add(&c1_120());
        assert!(phi.is_zero());
    }

    #[test]
    fn sqrt_identities_hold_in_q_zeta120() {
        assert_eq!(sqrt2_120().mul(&sqrt2_120()), Cyc120::rat(ri(2)));
        assert_eq!(sqrt5_120().mul(&sqrt5_120()), Cyc120::rat(ri(5)));
        assert_eq!(icyc_120().mul(&icyc_120()), Cyc120::rat(ri(-1)));
    }

    #[test]
    fn inv_times_self_is_one() {
        let x = Cyc120::rat(ri(3)).add(&sqrt5_120());
        assert_eq!(x.mul(&x.inv()), c1_120());
    }
}
