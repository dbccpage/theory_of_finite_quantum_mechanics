mod subject {
pub struct Inertia {
    pub positive: usize,
    pub negative: usize,
    pub zero: usize,
}

impl Inertia {
    /// `positive + negative + zero`.
    pub fn dimension(&self) -> usize {
        self.positive + self.negative + self.zero
    }

    /// `positive + negative`, the rank of the form.
    pub fn rank(&self) -> usize {
        self.positive + self.negative
    }

    /// No negative and no zero direction.
    pub fn is_positive_definite(&self) -> bool {
        self.negative == 0 && self.zero == 0
    }

    /// No negative direction.
    pub fn is_positive_semidefinite(&self) -> bool {
        self.negative == 0
    }

    /// No positive and no zero direction.
    pub fn is_negative_definite(&self) -> bool {
        self.positive == 0 && self.zero == 0
    }

    /// No positive direction.
    pub fn is_negative_semidefinite(&self) -> bool {
        self.positive == 0
    }
}
}
use subject::Inertia;

fn main() {
    let rank = std::panic::catch_unwind(|| Inertia { positive: usize::MAX, negative: 1, zero: 0 }.rank());
    let dimension = std::panic::catch_unwind(|| Inertia { positive: usize::MAX, negative: 0, zero: 1 }.dimension());
    assert!(rank.is_err(), "public rank overflow did not reproduce");
    assert!(dimension.is_err(), "public dimension overflow did not reproduce");
    println!("DEFECT_CONFIRMED:public_inertia_rank_and_dimension_overflow");
}
