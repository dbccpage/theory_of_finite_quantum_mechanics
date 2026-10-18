
use num_rational::BigRational;
use num_traits::{One, Zero};

use crate::rational::ri;

const DEGREE: usize = 20;

const PHI44_LOW: [i64; DEGREE] = [
    1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0,
];

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Cyc44 {
    pub a: [BigRational; DEGREE],
}

impl Cyc44 {
    pub fn zero() -> Self {
        Cyc44 {
            a: std::array::from_fn(|_| BigRational::zero()),
        }
    }

    pub fn rat(x: BigRational) -> Self {
        let mut c = Cyc44::zero();
        c.a[0] = x;
        c
    }

    pub fn zeta(p: i32) -> Self {
        let p = p.rem_euclid(44) as usize;
        let mut dense = vec![BigRational::zero(); 44];
        dense[p] = BigRational::one();
        Cyc44 {
            a: reduce_dense(dense),
        }
    }

    pub fn add(&self, o: &Cyc44) -> Cyc44 {
        Cyc44 {
            a: std::array::from_fn(|i| &self.a[i] + &o.a[i]),
        }
    }

    pub fn sub(&self, o: &Cyc44) -> Cyc44 {
        Cyc44 {
            a: std::array::from_fn(|i| &self.a[i] - &o.a[i]),
        }
    }

    pub fn neg(&self) -> Cyc44 {
        Cyc44 {
            a: std::array::from_fn(|i| -&self.a[i]),
        }
    }

    pub fn mul(&self, o: &Cyc44) -> Cyc44 {
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
        Cyc44 {
            a: reduce_dense(prod),
        }
    }

    pub fn conj(&self) -> Cyc44 {
        let mut out = Cyc44::zero();
        for (k, x) in self.a.iter().enumerate() {
            if !x.is_zero() {
                let zk = Cyc44::zeta(-(k as i32));
                for i in 0..DEGREE {
                    out.a[i] += x * &zk.a[i];
                }
            }
        }
        out
    }

    pub fn inv(&self) -> Cyc44 {
        let cols: [[BigRational; DEGREE]; DEGREE] = std::array::from_fn(|k| {
            let mut e = Cyc44::zero();
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
                .expect("Cyc44::inv on a non-invertible element");
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
        Cyc44 {
            a: std::array::from_fn(|i| a[i][DEGREE].clone()),
        }
    }

    pub fn is_zero(&self) -> bool {
        self.a.iter().all(|x| x.is_zero())
    }
}

pub fn c1_44() -> Cyc44 {
    Cyc44::rat(ri(1))
}

pub fn icyc_44() -> Cyc44 {
    Cyc44::zeta(11)
}

pub fn sqrt11_44() -> Cyc44 {
    icyc_44().neg().mul(&gauss11_44())
}

fn gauss11_44() -> Cyc44 {
    let mut sum = Cyc44::zero();
    for x in 0_i32..11 {
        sum = sum.add(&Cyc44::zeta(4 * x * x));
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
                if PHI44_LOW[j] != 0 {
                    dense[k - DEGREE + j] -= &v * ri(PHI44_LOW[j]);
                }
            }
            dense[k] = BigRational::zero();
        }
    }
    std::array::from_fn(|i| dense[i].clone())
}

impl Cyc44 {
    pub fn scale_rat(&self, r: &BigRational) -> Self {
        Cyc44 {
            a: std::array::from_fn(|i| &self.a[i] * r),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn zeta44_reduces_by_declared_cyclotomic_polynomial() {
        assert_eq!(Cyc44::zeta(44), c1_44());
        assert_eq!(Cyc44::zeta(22), Cyc44::rat(ri(-1)));
        let mut phi = Cyc44::zero();
        for k in (0_i32..=20).step_by(2) {
            let sign = if (k / 2) % 2 == 0 { 1 } else { -1 };
            let term = Cyc44::zeta(k);
            phi = if sign == 1 {
                phi.add(&term)
            } else {
                phi.sub(&term)
            };
        }
        assert!(phi.is_zero());
    }

    #[test]
    fn sqrt11_and_i_identities_hold_in_q_zeta44() {
        assert_eq!(icyc_44().mul(&icyc_44()), Cyc44::rat(ri(-1)));
        assert_eq!(sqrt11_44().mul(&sqrt11_44()), Cyc44::rat(ri(11)));
        assert_eq!(sqrt11_44().mul(&sqrt11_44().inv()), c1_44());
    }
}
