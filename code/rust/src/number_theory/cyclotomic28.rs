
use num_rational::BigRational;
use num_traits::{One, Zero};

use crate::rational::ri;

const DEGREE: usize = 12;

const PHI28_LOW: [i64; DEGREE] = [1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Cyc28 {
    pub a: [BigRational; DEGREE],
}

impl Cyc28 {
    pub fn zero() -> Self {
        Cyc28 {
            a: std::array::from_fn(|_| BigRational::zero()),
        }
    }

    pub fn rat(x: BigRational) -> Self {
        let mut c = Cyc28::zero();
        c.a[0] = x;
        c
    }

    pub fn zeta(p: i32) -> Self {
        let p = p.rem_euclid(28) as usize;
        let mut dense = vec![BigRational::zero(); 28];
        dense[p] = BigRational::one();
        Cyc28 {
            a: reduce_dense(dense),
        }
    }

    pub fn add(&self, o: &Cyc28) -> Cyc28 {
        Cyc28 {
            a: std::array::from_fn(|i| &self.a[i] + &o.a[i]),
        }
    }

    pub fn sub(&self, o: &Cyc28) -> Cyc28 {
        Cyc28 {
            a: std::array::from_fn(|i| &self.a[i] - &o.a[i]),
        }
    }

    pub fn neg(&self) -> Cyc28 {
        Cyc28 {
            a: std::array::from_fn(|i| -&self.a[i]),
        }
    }

    pub fn mul(&self, o: &Cyc28) -> Cyc28 {
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
        Cyc28 {
            a: reduce_dense(prod),
        }
    }

    pub fn conj(&self) -> Cyc28 {
        let mut out = Cyc28::zero();
        for (k, x) in self.a.iter().enumerate() {
            if !x.is_zero() {
                let zk = Cyc28::zeta(-(k as i32));
                for i in 0..DEGREE {
                    out.a[i] += x * &zk.a[i];
                }
            }
        }
        out
    }

    pub fn inv(&self) -> Cyc28 {
        let cols: [[BigRational; DEGREE]; DEGREE] = std::array::from_fn(|k| {
            let mut e = Cyc28::zero();
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
                .expect("Cyc28::inv on a non-invertible element");
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
        Cyc28 {
            a: std::array::from_fn(|i| a[i][DEGREE].clone()),
        }
    }

    pub fn is_zero(&self) -> bool {
        self.a.iter().all(|x| x.is_zero())
    }
}

pub fn c1_28() -> Cyc28 {
    Cyc28::rat(ri(1))
}

pub fn icyc_28() -> Cyc28 {
    Cyc28::zeta(7)
}

pub fn sqrt7_28() -> Cyc28 {
    icyc_28().neg().mul(&gauss7_28())
}

fn gauss7_28() -> Cyc28 {
    let mut sum = Cyc28::zero();
    for x in 0_i32..7 {
        sum = sum.add(&Cyc28::zeta(4 * x * x));
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
                if PHI28_LOW[j] != 0 {
                    dense[k - DEGREE + j] -= &v * ri(PHI28_LOW[j]);
                }
            }
            dense[k] = BigRational::zero();
        }
    }
    std::array::from_fn(|i| dense[i].clone())
}

impl Cyc28 {
    pub fn scale_rat(&self, r: &BigRational) -> Self {
        Cyc28 {
            a: std::array::from_fn(|i| &self.a[i] * r),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn zeta28_reduces_by_declared_cyclotomic_polynomial() {
        assert_eq!(Cyc28::zeta(28), c1_28());
        assert_eq!(Cyc28::zeta(14), Cyc28::rat(ri(-1)));
        let phi = Cyc28::zeta(12)
            .sub(&Cyc28::zeta(10))
            .add(&Cyc28::zeta(8))
            .sub(&Cyc28::zeta(6))
            .add(&Cyc28::zeta(4))
            .sub(&Cyc28::zeta(2))
            .add(&c1_28());
        assert!(phi.is_zero());
    }

    #[test]
    fn sqrt7_and_i_identities_hold_in_q_zeta28() {
        assert_eq!(icyc_28().mul(&icyc_28()), Cyc28::rat(ri(-1)));
        assert_eq!(sqrt7_28().mul(&sqrt7_28()), Cyc28::rat(ri(7)));
        assert_eq!(sqrt7_28().mul(&sqrt7_28().inv()), c1_28());
    }
}
