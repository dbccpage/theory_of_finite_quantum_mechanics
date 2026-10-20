use std::fmt;
pub trait Semiring: Clone + PartialEq + fmt::Debug {
    fn zero() -> Self;
    fn one() -> Self;
    fn add(&self, rhs: &Self) -> Self;
    fn mul(&self, rhs: &Self) -> Self;
    fn is_zero(&self) -> bool;
}

pub trait Ring: Semiring {
    fn neg(&self) -> Self;

    fn sub(&self, other: &Self) -> Self {
        self.add(&other.neg())
    }
}

pub trait ExactRing: Ring {}

impl Semiring for i64 {
    fn zero() -> Self {
        0
    }
    fn one() -> Self {
        1
    }
    fn add(&self, rhs: &Self) -> Self {
        *self + *rhs
    }
    fn mul(&self, rhs: &Self) -> Self {
        *self * *rhs
    }
    fn is_zero(&self) -> bool {
        *self == 0
    }
}

impl Ring for i64 {
    fn neg(&self) -> Self {
        -*self
    }
}

impl ExactRing for i64 {}
fn exact_ring<T:ExactRing>(){}
fn main(){
    exact_ring::<i64>();
    let observed=std::panic::catch_unwind(||Semiring::add(&i64::MAX,&1)).is_err();
    assert!(observed,"the source-grounded overflow witness did not reproduce");
    println!("DEFECT_CONFIRMED:provider_marks_overflowing_i64_as_exact");
}
