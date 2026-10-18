

use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::rational::{r_half, ri, Rational};


#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct GaussianRat {
    pub re: Rational,
    pub im: Rational,
}

impl GaussianRat {
    pub fn zero() -> Self {
        Self {
            re: Rational::zero(),
            im: Rational::zero(),
        }
    }

    pub fn one() -> Self {
        Self {
            re: Rational::one(),
            im: Rational::zero(),
        }
    }

    pub fn i() -> Self {
        Self {
            re: Rational::zero(),
            im: Rational::one(),
        }
    }

    pub fn from_rational(r: Rational) -> Self {
        Self {
            re: r,
            im: Rational::zero(),
        }
    }

    pub fn from_ints(re: i64, im: i64) -> Self {
        Self {
            re: ri(re),
            im: ri(im),
        }
    }

    pub fn is_integer_ring_element(&self) -> bool {
        self.re.is_integer() && self.im.is_integer()
    }

    pub fn is_zero(&self) -> bool {
        self.re.is_zero() && self.im.is_zero()
    }

    pub fn is_real(&self) -> bool {
        self.im.is_zero()
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            re: &self.re + &other.re,
            im: &self.im + &other.im,
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            re: &self.re - &other.re,
            im: &self.im - &other.im,
        }
    }

    pub fn neg(&self) -> Self {
        Self {
            re: -&self.re,
            im: -&self.im,
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        Self {
            re: &self.re * &other.re - &self.im * &other.im,
            im: &self.re * &other.im + &self.im * &other.re,
        }
    }

    pub fn conj(&self) -> Self {
        Self {
            re: self.re.clone(),
            im: -&self.im,
        }
    }

    pub fn norm_sq(&self) -> Rational {
        &self.re * &self.re + &self.im * &self.im
    }

    pub fn inv(&self) -> Self {
        let n = self.norm_sq();
        if n.is_zero() {
            panic!("Division by zero in Q(i)");
        }
        Self {
            re: &self.re / &n,
            im: -&self.im / &n,
        }
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct EisensteinRat {
    pub a: Rational,
    pub b: Rational,
}

impl EisensteinRat {
    pub fn zero() -> Self {
        Self {
            a: Rational::zero(),
            b: Rational::zero(),
        }
    }

    pub fn one() -> Self {
        Self {
            a: Rational::one(),
            b: Rational::zero(),
        }
    }

    pub fn zeta3() -> Self {
        Self {
            a: Rational::zero(),
            b: Rational::one(),
        }
    }

    pub fn zeta3_sq() -> Self {
        Self {
            a: -Rational::one(),
            b: -Rational::one(),
        }
    }

    pub fn from_rational(r: Rational) -> Self {
        Self {
            a: r,
            b: Rational::zero(),
        }
    }

    pub fn from_ints(a: i64, b: i64) -> Self {
        Self { a: ri(a), b: ri(b) }
    }

    pub fn is_integer_ring_element(&self) -> bool {
        self.a.is_integer() && self.b.is_integer()
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            a: &self.a + &other.a,
            b: &self.b + &other.b,
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            a: &self.a - &other.a,
            b: &self.b - &other.b,
        }
    }

    pub fn neg(&self) -> Self {
        Self {
            a: -&self.a,
            b: -&self.b,
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let ac = &self.a * &other.a;
        let bd = &self.b * &other.b;
        let ad = &self.a * &other.d_coeff();
        let bc = &self.b * &other.a;
        Self {
            a: &ac - &bd,
            b: &ad + &bc - &bd,
        }
    }

    fn d_coeff(&self) -> Rational {
        self.b.clone()
    }

    pub fn conj(&self) -> Self {
        Self {
            a: &self.a - &self.b,
            b: -&self.b,
        }
    }

    pub fn norm_sq(&self) -> Rational {
        &self.a * &self.a - &self.a * &self.b + &self.b * &self.b
    }

    pub fn inv(&self) -> Self {
        let n = self.norm_sq();
        if n.is_zero() {
            panic!("Division by zero in Q(zeta_3)");
        }
        let c = self.conj();
        Self {
            a: &c.a / &n,
            b: &c.b / &n,
        }
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Cyc8 {
    pub a: [Rational; 4],
}

impl Cyc8 {
    pub fn zero() -> Self {
        Self {
            a: std::array::from_fn(|_| Rational::zero()),
        }
    }

    pub fn one() -> Self {
        let mut c = Self::zero();
        c.a[0] = Rational::one();
        c
    }

    pub fn zeta8(pow: i32) -> Self {
        let p = pow.rem_euclid(8) as usize;
        let mut c = Self::zero();
        if p < 4 {
            c.a[p] = Rational::one();
        } else {
            c.a[p - 4] = -Rational::one();
        }
        c
    }

    pub fn i() -> Self {
        Self::zeta8(2)
    }

    pub fn sqrt2() -> Self {
        Self::zeta8(1).sub(&Self::zeta8(3))
    }

    pub fn inv_sqrt2() -> Self {
        Self::sqrt2().mul(&Self {
            a: [
                r_half(),
                Rational::zero(),
                Rational::zero(),
                Rational::zero(),
            ],
        })
    }

    pub fn sqrt2_inv() -> Self {
        Self::inv_sqrt2()
    }

    pub fn is_integer_ring_element(&self) -> bool {
        self.a.iter().all(|x| x.is_integer())
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] + &other.a[i]),
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] - &other.a[i]),
        }
    }

    pub fn neg(&self) -> Self {
        Self {
            a: std::array::from_fn(|i| -&self.a[i]),
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut full = vec![Rational::zero(); 7];
        for i in 0..4 {
            if !self.a[i].is_zero() {
                for j in 0..4 {
                    if !other.a[j].is_zero() {
                        full[i + j] += &self.a[i] * &other.a[j];
                    }
                }
            }
        }
        let mut res = std::array::from_fn(|k| full[k].clone());
        for k in 4..7 {
            if !full[k].is_zero() {
                res[k - 4] -= &full[k];
            }
        }
        Self { a: res }
    }

    pub fn conj(&self) -> Self {
        Self {
            a: [
                self.a[0].clone(),
                -self.a[3].clone(),
                -self.a[2].clone(),
                -self.a[1].clone(),
            ],
        }
    }

    pub fn inv(&self) -> Self {
        let coeffs = crate::power_basis::invert_by_multiplication_matrix(4, |j| {
            let mut unit = Self::zero();
            unit.a[j] = Rational::one();
            self.mul(&unit).a.to_vec()
        })
        .expect("Cyc8::inv on a non-invertible element");
        Self {
            a: std::array::from_fn(|i| coeffs[i].clone()),
        }
    }

    pub fn as_rational(&self) -> Option<Rational> {
        if self.a[1].is_zero() && self.a[2].is_zero() && self.a[3].is_zero() {
            Some(self.a[0].clone())
        } else {
            None
        }
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Cyc12 {
    pub a: [Rational; 4],
}

impl Cyc12 {
    pub fn zero() -> Self {
        Self {
            a: std::array::from_fn(|_| Rational::zero()),
        }
    }

    pub fn one() -> Self {
        let mut c = Self::zero();
        c.a[0] = Rational::one();
        c
    }

    pub fn zeta12(pow: i32) -> Self {
        let p = pow.rem_euclid(12) as usize;
        let mut dense = vec![Rational::zero(); 12];
        dense[p] = Rational::one();
        Self {
            a: reduce_dense_12(dense),
        }
    }

    pub fn i() -> Self {
        Self::zeta12(3)
    }

    pub fn zeta3() -> Self {
        Self::zeta12(4)
    }

    pub fn is_integer_ring_element(&self) -> bool {
        self.a.iter().all(|x| x.is_integer())
    }

    pub fn is_zero(&self) -> bool {
        self.a.iter().all(|x| x == &Rational::zero())
    }

    pub fn is_rational(&self) -> bool {
        self.a[1..].iter().all(|x| x == &Rational::zero())
    }

    pub fn as_rational(&self) -> Option<Rational> {
        if self.is_rational() {
            Some(self.a[0].clone())
        } else {
            None
        }
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] + &other.a[i]),
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] - &other.a[i]),
        }
    }

    pub fn neg(&self) -> Self {
        Self {
            a: std::array::from_fn(|i| -&self.a[i]),
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut prod = vec![Rational::zero(); 7];
        for i in 0..4 {
            if !self.a[i].is_zero() {
                for j in 0..4 {
                    if !other.a[j].is_zero() {
                        prod[i + j] += &self.a[i] * &other.a[j];
                    }
                }
            }
        }
        Self {
            a: reduce_dense_12(prod),
        }
    }

    pub fn inv(&self) -> Self {
        let coeffs = crate::power_basis::invert_by_multiplication_matrix(4, |j| {
            let mut unit = Self::zero();
            unit.a[j] = Rational::one();
            self.mul(&unit).a.to_vec()
        })
        .expect("Cyc12::inv on a non-invertible element");
        Self {
            a: std::array::from_fn(|i| coeffs[i].clone()),
        }
    }

    pub fn conj(&self) -> Self {
        let mut out = Self::zero();
        for (k, coeff) in self.a.iter().enumerate() {
            if !coeff.is_zero() {
                let zk = Self::zeta12(-(k as i32));
                for i in 0..4 {
                    out.a[i] += coeff * &zk.a[i];
                }
            }
        }
        out
    }
}

fn reduce_dense_12(mut poly: Vec<Rational>) -> [Rational; 4] {
    while poly.len() > 4 {
        let deg = poly.len() - 1;
        let c = poly.pop().unwrap();
        if !c.is_zero() {
            poly[deg - 4 + 2] += &c;
            poly[deg - 4] -= &c;
        }
    }
    let mut out = std::array::from_fn(|_| Rational::zero());
    for (i, c) in poly.into_iter().enumerate() {
        if i < 4 {
            out[i] = c;
        }
    }
    out
}


#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Cyc5 {
    pub a: [Rational; 4],
}

impl Cyc5 {
    pub fn zero() -> Self {
        Self {
            a: std::array::from_fn(|_| Rational::zero()),
        }
    }

    pub fn one() -> Self {
        let mut c = Self::zero();
        c.a[0] = Rational::one();
        c
    }

    pub fn rat(r: Rational) -> Self {
        let mut c = Self::zero();
        c.a[0] = r;
        c
    }

    pub fn zeta5(pow: i32) -> Self {
        let p = pow.rem_euclid(5) as usize;
        let mut dense = vec![Rational::zero(); 5];
        dense[p] = Rational::one();
        Self {
            a: reduce_dense_5(dense),
        }
    }

    pub fn is_integer_ring_element(&self) -> bool {
        self.a.iter().all(|x| x.is_integer())
    }

    pub fn is_zero(&self) -> bool {
        self.a.iter().all(|x| x.is_zero())
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] + &other.a[i]),
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] - &other.a[i]),
        }
    }

    pub fn neg(&self) -> Self {
        Self {
            a: std::array::from_fn(|i| -&self.a[i]),
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut prod = vec![Rational::zero(); 7];
        for i in 0..4 {
            if !self.a[i].is_zero() {
                for j in 0..4 {
                    if !other.a[j].is_zero() {
                        prod[i + j] += &self.a[i] * &other.a[j];
                    }
                }
            }
        }
        Self {
            a: reduce_dense_5(prod),
        }
    }

    pub fn conj(&self) -> Self {
        let mut out = Self::zero();
        for (k, coeff) in self.a.iter().enumerate() {
            if !coeff.is_zero() {
                let zk = Self::zeta5(-(k as i32));
                for i in 0..4 {
                    out.a[i] += coeff * &zk.a[i];
                }
            }
        }
        out
    }

    pub fn trace(&self) -> Rational {
        &self.a[0] * ri(4) - &self.a[1] - &self.a[2] - &self.a[3]
    }

    pub fn inv(&self) -> Self {
        let cols: [[Rational; 4]; 4] = std::array::from_fn(|k| {
            let zk = Self::zeta5(k as i32);
            let p = self.mul(&zk);
            p.a
        });
        let target = [
            Rational::one(),
            Rational::zero(),
            Rational::zero(),
            Rational::zero(),
        ];
        let sol =
            solve_linear_4(&cols, &target).expect("Non-zero element in Q(zeta_5) is invertible");
        Self { a: sol }
    }
}

fn reduce_dense_5(mut poly: Vec<Rational>) -> [Rational; 4] {
    while poly.len() > 4 {
        let deg = poly.len() - 1;
        let c = poly.pop().unwrap();
        if !c.is_zero() {
            for j in 0..4 {
                poly[deg - 4 + j] -= &c;
            }
        }
    }
    let mut out = std::array::from_fn(|_| Rational::zero());
    for (i, c) in poly.into_iter().enumerate() {
        if i < 4 {
            out[i] = c;
        }
    }
    out
}


const DEGREE_24: usize = 8;

#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct Cyc24 {
    pub a: [Rational; DEGREE_24],
}

impl Cyc24 {
    pub fn zero() -> Self {
        Self {
            a: std::array::from_fn(|_| Rational::zero()),
        }
    }

    pub fn one() -> Self {
        let mut c = Self::zero();
        c.a[0] = Rational::one();
        c
    }

    pub fn rat(r: Rational) -> Self {
        let mut c = Self::zero();
        c.a[0] = r;
        c
    }

    pub fn from_int(n: i64) -> Self {
        Self::rat(ri(n))
    }

    pub fn zeta24(pow: i32) -> Self {
        let p = pow.rem_euclid(24) as usize;
        let mut dense = vec![Rational::zero(); 24];
        dense[p] = Rational::one();
        Self {
            a: reduce_dense_24(dense),
        }
    }

    pub fn i() -> Self {
        Self::zeta24(6)
    }

    pub fn zeta3() -> Self {
        Self::zeta24(8)
    }

    pub fn zeta3_pow(k: i32) -> Self {
        Self::zeta24(8 * k)
    }

    pub fn zeta8() -> Self {
        Self::zeta24(3)
    }

    pub fn zeta12() -> Self {
        Self::zeta24(2)
    }

    pub fn sqrt2() -> Self {
        Self::zeta24(3).sub(&Self::zeta24(9))
    }

    pub fn sqrt3() -> Self {
        Self::zeta24(2).add(&Self::zeta24(-2))
    }

    pub fn inv_sqrt2() -> Self {
        Self::sqrt2().mul(&Self::rat(r_half()))
    }

    pub fn sqrt2_inv() -> Self {
        Self::inv_sqrt2()
    }

    pub fn embed_gaussian(g: &GaussianRat) -> Self {
        let mut c = Self::rat(g.re.clone());
        let imag = Self::i();
        for i in 0..DEGREE_24 {
            c.a[i] += &g.im * &imag.a[i];
        }
        c
    }

    pub fn embed_eisenstein(e: &EisensteinRat) -> Self {
        let mut c = Self::rat(e.a.clone());
        let w = Self::zeta3();
        for i in 0..DEGREE_24 {
            c.a[i] += &e.b * &w.a[i];
        }
        c
    }

    pub fn is_zero(&self) -> bool {
        self.a.iter().all(|x| x.is_zero())
    }

    pub fn is_rational(&self) -> bool {
        self.a[1..].iter().all(|x| x.is_zero())
    }

    pub fn as_rational(&self) -> Option<Rational> {
        if self.is_rational() {
            Some(self.a[0].clone())
        } else {
            None
        }
    }

    pub fn add(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] + &other.a[i]),
        }
    }

    pub fn sub(&self, other: &Self) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] - &other.a[i]),
        }
    }

    pub fn neg(&self) -> Self {
        Self {
            a: std::array::from_fn(|i| -&self.a[i]),
        }
    }

    pub fn mul(&self, other: &Self) -> Self {
        let mut prod = vec![Rational::zero(); 2 * DEGREE_24 - 1];
        for (i, x) in self.a.iter().enumerate() {
            if !x.is_zero() {
                for (j, y) in other.a.iter().enumerate() {
                    if !y.is_zero() {
                        prod[i + j] += x * y;
                    }
                }
            }
        }
        Self {
            a: reduce_dense_24(prod),
        }
    }

    pub fn conj(&self) -> Self {
        let mut out = Self::zero();
        for (k, x) in self.a.iter().enumerate() {
            if !x.is_zero() {
                let zk = Self::zeta24(-(k as i32));
                for i in 0..DEGREE_24 {
                    out.a[i] += x * &zk.a[i];
                }
            }
        }
        out
    }

    pub fn inv(&self) -> Self {
        let cols: [[Rational; DEGREE_24]; DEGREE_24] = std::array::from_fn(|k| {
            let zk = Self::zeta24(k as i32);
            let p = self.mul(&zk);
            p.a
        });
        let mut target: [Rational; DEGREE_24] = std::array::from_fn(|_| Rational::zero());
        target[0] = Rational::one();
        let sol =
            solve_linear_8(&cols, &target).expect("Non-zero element in Q(zeta_24) is invertible");
        Self { a: sol }
    }
}

fn reduce_dense_24(mut poly: Vec<Rational>) -> [Rational; DEGREE_24] {
    while poly.len() > DEGREE_24 {
        let deg = poly.len() - 1;
        let c = poly.pop().unwrap();
        if !c.is_zero() {
            poly[deg - 8 + 4] += &c;
            poly[deg - 8] -= &c;
        }
    }
    let mut out = std::array::from_fn(|_| Rational::zero());
    for (i, c) in poly.into_iter().enumerate() {
        if i < DEGREE_24 {
            out[i] = c;
        }
    }
    out
}


fn solve_linear_4(cols: &[[Rational; 4]; 4], b: &[Rational; 4]) -> Option<[Rational; 4]> {
    let mut m: [[Rational; 5]; 4] =
        std::array::from_fn(|_| std::array::from_fn(|_| Rational::zero()));
    for r in 0..4 {
        for c in 0..4 {
            m[r][c] = cols[c][r].clone();
        }
        m[r][4] = b[r].clone();
    }
    gaussian_elimination_4(&mut m)?;
    Some(std::array::from_fn(|i| m[i][4].clone()))
}

fn gaussian_elimination_4(m: &mut [[Rational; 5]; 4]) -> Option<()> {
    for col in 0..4 {
        let pivot_row = (col..4).find(|&r| !m[r][col].is_zero())?;
        if pivot_row != col {
            m.swap(col, pivot_row);
        }
        let inv_piv = Rational::one() / &m[col][col];
        for k in col..5 {
            m[col][k] = &m[col][k] * &inv_piv;
        }
        for r in 0..4 {
            if r != col && !m[r][col].is_zero() {
                let factor = m[r][col].clone();
                for k in col..5 {
                    let sub = &factor * &m[col][k];
                    m[r][k] = &m[r][k] - &sub;
                }
            }
        }
    }
    Some(())
}

fn solve_linear_8(cols: &[[Rational; 8]; 8], b: &[Rational; 8]) -> Option<[Rational; 8]> {
    let mut m: [[Rational; 9]; 8] =
        std::array::from_fn(|_| std::array::from_fn(|_| Rational::zero()));
    for r in 0..8 {
        for c in 0..8 {
            m[r][c] = cols[c][r].clone();
        }
        m[r][8] = b[r].clone();
    }
    for col in 0..8 {
        let pivot_row = (col..8).find(|&r| !m[r][col].is_zero())?;
        if pivot_row != col {
            m.swap(col, pivot_row);
        }
        let inv_piv = Rational::one() / &m[col][col];
        for k in col..9 {
            m[col][k] = &m[col][k] * &inv_piv;
        }
        for r in 0..8 {
            if r != col && !m[r][col].is_zero() {
                let factor = m[r][col].clone();
                for k in col..9 {
                    let sub = &factor * &m[col][k];
                    m[r][k] = &m[r][k] - &sub;
                }
            }
        }
    }
    Some(std::array::from_fn(|i| m[i][8].clone()))
}

impl Cyc24 {
    pub fn scale_rat(&self, r: &Rational) -> Self {
        let mut out = self.clone();
        for i in 0..DEGREE_24 {
            out.a[i] = &out.a[i] * r;
        }
        out
    }
}

impl Cyc5 {
    pub fn scale_rat(&self, r: &Rational) -> Self {
        let mut out = self.clone();
        for i in 0..4 {
            out.a[i] = &out.a[i] * r;
        }
        out
    }
}

impl Cyc12 {
    pub fn scale_rat(&self, r: &Rational) -> Self {
        let mut out = self.clone();
        for i in 0..4 {
            out.a[i] = &out.a[i] * r;
        }
        out
    }
}

impl Cyc8 {
    pub fn scale_rat(&self, r: &Rational) -> Self {
        Self {
            a: std::array::from_fn(|i| &self.a[i] * r),
        }
    }
}

impl GaussianRat {
    pub fn scale_rat(&self, r: &Rational) -> Self {
        Self {
            re: &self.re * r,
            im: &self.im * r,
        }
    }
}

impl EisensteinRat {
    pub fn scale_rat(&self, r: &Rational) -> Self {
        Self {
            a: &self.a * r,
            b: &self.b * r,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::rational::rq;

    #[test]
    fn test_gaussian_rationals() {
        let i = GaussianRat::i();
        let i_sq = i.mul(&i);
        assert_eq!(i_sq, GaussianRat::from_ints(-1, 0));

        let g = GaussianRat::from_ints(3, 4);
        assert_eq!(g.norm_sq(), rq(25, 1));
        let g_inv = g.inv();
        let prod = g.mul(&g_inv);
        assert_eq!(prod, GaussianRat::one());
    }

    #[test]
    fn test_gaussian_rational_field_element() {
        let g = GaussianRat::from_ints(3, -4);
        assert!(GaussianRat::zero().is_zero());
        assert!(!g.is_zero());
        assert_eq!(
            linear_algebra::exact_field::involution::Involution::conjugate(&g),
            GaussianRat::from_ints(3, 4)
        );
        assert_eq!(g.scale_rat(&rq(1, 2)).re, rq(3, 2));
        assert_eq!(
            g.mul(&linear_algebra::exact_field::involution::Involution::conjugate(&g)),
            GaussianRat::from_ints(25, 0)
        );
        assert_eq!(g.add(&g).sub(&g), g);
        assert!(GaussianRat::from_ints(7, 0).is_real());
        assert!(!GaussianRat::i().is_real());
    }

    #[test]
    fn test_eisenstein_rationals() {
        let w = EisensteinRat::zeta3();
        let w_cubed = w.mul(&w).mul(&w);
        assert_eq!(w_cubed, EisensteinRat::one());

        let e = EisensteinRat::from_ints(1, 2);
        let e_inv = e.inv();
        assert_eq!(e.mul(&e_inv), EisensteinRat::one());
    }

    #[test]
    fn test_cyc8_sqrt2_identity() {
        let z = Cyc8::zeta8(1);
        let z7 = Cyc8::zeta8(7);
        let sqrt2 = z.add(&z7);
        let sqrt2_sq = sqrt2.mul(&sqrt2);
        assert_eq!(sqrt2_sq.a[0], rq(2, 1));
        assert_eq!(sqrt2_sq.a[1], rq(0, 1));
        assert_eq!(sqrt2_sq.a[2], rq(0, 1));
        assert_eq!(sqrt2_sq.a[3], rq(0, 1));
    }

    #[test]
    fn test_cyc12_identities() {
        let z = Cyc12::zeta12(1);
        let z12 = (0..12).fold(Cyc12::one(), |acc, _| acc.mul(&z));
        assert_eq!(z12, Cyc12::one());

        let i = Cyc12::i();
        assert_eq!(i.mul(&i), Cyc12::one().neg());
    }

    #[test]
    fn test_cyc5_identities() {
        let z = Cyc5::zeta5(1);
        let z5 = z.mul(&z).mul(&z).mul(&z).mul(&z);
        assert_eq!(z5, Cyc5::one());

        let sum = (0..5).fold(Cyc5::zero(), |acc, k| acc.add(&Cyc5::zeta5(k)));
        assert!(sum.is_zero());
    }

    #[test]
    fn test_cyc24_unification() {
        let i = Cyc24::i();
        assert_eq!(i.mul(&i), Cyc24::one().neg());

        let z3 = Cyc24::zeta3();
        let z3_cubed = z3.mul(&z3).mul(&z3);
        assert_eq!(z3_cubed, Cyc24::one());
    }
}
