
use core::sync::atomic::{AtomicU64, Ordering};

static CARRIER_COUNTER: AtomicU64 = AtomicU64::new(0);

pub trait PrimitiveDifference {
    type Carrier;
    type Diff: PartialEq;

    fn delta(&self, x: &Self::Carrier, y: &Self::Carrier) -> Self::Diff;

    fn zero(&self, d: &Self::Diff) -> bool;

    fn zero_rel(&self, x: &Self::Carrier, y: &Self::Carrier) -> bool {
        self.zero(&self.delta(x, y))
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct QuotientClass {
    carrier_id: u64,
    index: usize,
}

impl QuotientClass {
    pub fn index(self) -> usize {
        self.index
    }

    pub fn carrier_id(self) -> u64 {
        self.carrier_id
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum PrimitiveDifferenceError {
    ZeroReflexivityFailure { x: usize },
    ZeroSymmetryFailure { x: usize, y: usize },
    ZeroTransitivityFailure { x: usize, y: usize, z: usize },
    DeltaCongruenceFailure {
        x: usize,
        x_prime: usize,
        y: usize,
        y_prime: usize,
    },
    PairCongruenceFailure { x: usize, y: usize },
    DomainScaleOverflow { n: usize },
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ZeroLawWitness {
    pub domain_len: usize,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct DeltaCongruenceWitness {
    pub domain_len: usize,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct PairDescentWitness {
    pub domain_len: usize,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct PairObstructionWitness {
    pub x: usize,
    pub y: usize,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct LocalGlobalPairObstruction {
    pub left_descends: bool,
    pub right_descends: bool,
    pub pair_descends: bool,
    pub counterexample: Option<PairObstructionWitness>,
}

pub struct FiniteCarrier<'a, P: PrimitiveDifference> {
    diff: &'a P,
    domain: Vec<P::Carrier>,
}

impl<'a, P: PrimitiveDifference> FiniteCarrier<'a, P> {
    pub fn new(diff: &'a P, domain: Vec<P::Carrier>) -> Self {
        Self { diff, domain }
    }

    pub fn domain_len(&self) -> usize {
        self.domain.len()
    }

    pub fn validate_zero_laws(&self) -> Result<ZeroLawWitness, PrimitiveDifferenceError> {
        self.validate_zero_partition().map(|_| ZeroLawWitness {
            domain_len: self.domain.len(),
        })
    }

    pub fn try_validate(self) -> Result<ValidatedFiniteCarrier<'a, P>, PrimitiveDifferenceError> {
        let partition = self.validate_zero_partition()?;
        let carrier_id = CARRIER_COUNTER.fetch_add(1, Ordering::Relaxed);
        Ok(ValidatedFiniteCarrier {
            diff: self.diff,
            domain: self.domain,
            reps: partition.reps,
            class_of: partition.class_of,
            carrier_id,
        })
    }

    fn validate_zero_partition(&self) -> Result<ZeroPartition, PrimitiveDifferenceError> {
        let domain = &self.domain;
        let n = domain.len();
        let relation_len = n
            .checked_mul(n)
            .ok_or(PrimitiveDifferenceError::DomainScaleOverflow { n })?;
        let mut relation = vec![false; relation_len];

        for (x, value) in domain.iter().enumerate() {
            if !self.diff.zero_rel(value, value) {
                return Err(PrimitiveDifferenceError::ZeroReflexivityFailure { x });
            }
            relation[x * n + x] = true;
        }

        for x in 0..n {
            for y in (x + 1)..n {
                let xy = self.diff.zero_rel(&domain[x], &domain[y]);
                let yx = self.diff.zero_rel(&domain[y], &domain[x]);
                if xy != yx {
                    return Err(if xy {
                        PrimitiveDifferenceError::ZeroSymmetryFailure { x, y }
                    } else {
                        PrimitiveDifferenceError::ZeroSymmetryFailure { x: y, y: x }
                    });
                }
                relation[x * n + y] = xy;
                relation[y * n + x] = xy;
            }
        }

        let mut reps = Vec::new();
        let mut class_of = vec![usize::MAX; n];
        for candidate in 0..n {
            if class_of[candidate] != usize::MAX {
                continue;
            }

            let class = reps.len();
            reps.push(candidate);
            for member in candidate..n {
                if class_of[member] == usize::MAX && relation[candidate * n + member] {
                    class_of[member] = class;
                }
            }
        }

        for x in 0..n {
            for z in (x + 1)..n {
                let same_class = class_of[x] == class_of[z];
                let related = relation[x * n + z];
                if same_class == related {
                    continue;
                }

                if same_class {
                    let y = reps[class_of[x]];
                    return Err(PrimitiveDifferenceError::ZeroTransitivityFailure { x, y, z });
                }

                let (x0, y0, z0) = if class_of[x] < class_of[z] {
                    (reps[class_of[x]], x, z)
                } else {
                    (reps[class_of[z]], z, x)
                };
                return Err(PrimitiveDifferenceError::ZeroTransitivityFailure {
                    x: x0,
                    y: y0,
                    z: z0,
                });
            }
        }

        Ok(ZeroPartition { reps, class_of })
    }
}

struct ZeroPartition {
    reps: Vec<usize>,
    class_of: Vec<usize>,
}

pub struct ValidatedFiniteCarrier<'a, P: PrimitiveDifference> {
    diff: &'a P,
    domain: Vec<P::Carrier>,
    reps: Vec<usize>,
    class_of: Vec<usize>,
    carrier_id: u64,
}

impl<'a, P: PrimitiveDifference> ValidatedFiniteCarrier<'a, P> {
    pub fn try_new(diff: &'a P, domain: Vec<P::Carrier>) -> Result<Self, PrimitiveDifferenceError> {
        FiniteCarrier::new(diff, domain).try_validate()
    }

    pub fn num_classes(&self) -> usize {
        self.reps.len()
    }

    pub fn domain_len(&self) -> usize {
        self.domain.len()
    }

    pub fn carrier_id(&self) -> u64 {
        self.carrier_id
    }

    fn brand(&self, index: usize) -> QuotientClass {
        QuotientClass {
            carrier_id: self.carrier_id,
            index,
        }
    }

    pub fn residual_quotient(&self) -> Vec<QuotientClass> {
        (0..self.reps.len()).map(|ci| self.brand(ci)).collect()
    }

    pub fn class_of_index(&self, i: usize) -> Option<QuotientClass> {
        self.class_of.get(i).copied().map(|class| self.brand(class))
    }

    pub fn class_of_value_diagnostic(&self, x: &P::Carrier) -> Option<QuotientClass> {
        self.reps
            .iter()
            .position(|&r| self.diff.zero_rel(&self.domain[r], x))
            .map(|ci| self.brand(ci))
    }

    pub fn validate_delta_congruence(
        &self,
    ) -> Result<DeltaCongruenceWitness, PrimitiveDifferenceError> {
        let n = self.domain.len();
        let class_count = self.reps.len();
        let capacity = class_count
            .checked_mul(class_count)
            .ok_or(PrimitiveDifferenceError::DomainScaleOverflow { n: class_count })?;
        let mut class_deltas = Vec::with_capacity(capacity);
        for &x in &self.reps {
            for &y in &self.reps {
                class_deltas.push(self.diff.delta(&self.domain[x], &self.domain[y]));
            }
        }

        for (x, &x_class) in self.class_of.iter().enumerate() {
            for (y, &y_class) in self.class_of.iter().enumerate() {
                let observed = self.diff.delta(&self.domain[x], &self.domain[y]);
                if observed != class_deltas[x_class * class_count + y_class] {
                    return Err(PrimitiveDifferenceError::DeltaCongruenceFailure {
                        x,
                        x_prime: self.reps[x_class],
                        y,
                        y_prime: self.reps[y_class],
                    });
                }
            }
        }
        Ok(DeltaCongruenceWitness { domain_len: n })
    }

    pub fn delta_congruent_on_domain(&self) -> bool {
        self.validate_delta_congruence().is_ok()
    }

    pub fn delta_factors_through_quotient_on_domain(&self) -> bool {
        self.delta_congruent_on_domain()
    }

    pub fn try_delta_factor(&self) -> Result<DeltaFactor<'_, 'a, P>, PrimitiveDifferenceError> {
        let _ = self.validate_delta_congruence()?;
        Ok(DeltaFactor { carrier: self })
    }

    pub fn observable_descends_on_domain<G, F>(&self, phi: F) -> bool
    where
        G: PartialEq,
        F: Fn(&P::Carrier) -> G,
    {
        let values: Vec<_> = self.domain.iter().map(phi).collect();
        values
            .iter()
            .enumerate()
            .all(|(i, value)| value == &values[self.reps[self.class_of[i]]])
    }

    pub fn validate_pair_descent_on_domain<G, H, FP, FQ>(
        &self,
        phi: FP,
        psi: FQ,
    ) -> Result<PairDescentWitness, PrimitiveDifferenceError>
    where
        G: PartialEq,
        H: PartialEq,
        FP: Fn(&P::Carrier) -> G,
        FQ: Fn(&P::Carrier) -> H,
    {
        let phi_values: Vec<_> = self.domain.iter().map(phi).collect();
        let psi_values: Vec<_> = self.domain.iter().map(psi).collect();
        for (i, &class) in self.class_of.iter().enumerate() {
            let representative = self.reps[class];
            if phi_values[i] != phi_values[representative]
                || psi_values[i] != psi_values[representative]
            {
                return Err(PrimitiveDifferenceError::PairCongruenceFailure {
                    x: representative,
                    y: i,
                });
            }
        }
        Ok(PairDescentWitness {
            domain_len: self.domain.len(),
        })
    }

    pub fn local_green_global_red<G, H, FP, FQ>(
        &self,
        phi: FP,
        psi: FQ,
    ) -> LocalGlobalPairObstruction
    where
        G: PartialEq,
        H: PartialEq,
        FP: Fn(&P::Carrier) -> G,
        FQ: Fn(&P::Carrier) -> H,
    {
        let phi_values: Vec<_> = self.domain.iter().map(phi).collect();
        let psi_values: Vec<_> = self.domain.iter().map(psi).collect();
        let mut left_descends = true;
        let mut right_descends = true;
        let mut counterexample: Option<PairObstructionWitness> = None;
        for (i, &class) in self.class_of.iter().enumerate() {
            let representative = self.reps[class];
            let phi_diff = phi_values[i] != phi_values[representative];
            let psi_diff = psi_values[i] != psi_values[representative];
            if phi_diff {
                left_descends = false;
            }
            if psi_diff {
                right_descends = false;
            }
            if (phi_diff || psi_diff) && counterexample.is_none() {
                counterexample = Some(PairObstructionWitness {
                    x: representative,
                    y: i,
                });
            }
        }
        LocalGlobalPairObstruction {
            left_descends,
            right_descends,
            pair_descends: counterexample.is_none(),
            counterexample,
        }
    }
}

pub struct DeltaFactor<'c, 'a, P: PrimitiveDifference> {
    carrier: &'c ValidatedFiniteCarrier<'a, P>,
}

impl<'c, 'a, P: PrimitiveDifference> DeltaFactor<'c, 'a, P> {
    pub fn apply(&self, qx: QuotientClass, qy: QuotientClass) -> Option<P::Diff> {
        let id = self.carrier.carrier_id;
        if qx.carrier_id != id || qy.carrier_id != id {
            return None;
        }
        let rx = *self.carrier.reps.get(qx.index)?;
        let ry = *self.carrier.reps.get(qy.index)?;
        Some(
            self.carrier
                .diff
                .delta(&self.carrier.domain[rx], &self.carrier.domain[ry]),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::Cell;

    struct BoolAllZeroNonconstant;
    impl PrimitiveDifference for BoolAllZeroNonconstant {
        type Carrier = bool;
        type Diff = bool;
        fn delta(&self, x: &bool, _y: &bool) -> bool {
            *x
        }
        fn zero(&self, _d: &bool) -> bool {
            true
        }
    }

    #[test]
    fn bool_all_zero_nonconstant_has_no_factorization() {
        let p = BoolAllZeroNonconstant;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![false, true]).expect("zero laws hold");
        assert_eq!(vc.num_classes(), 1);
        assert!(!vc.delta_congruent_on_domain());
        assert!(!vc.delta_factors_through_quotient_on_domain());
        assert!(vc.try_delta_factor().is_err());
    }

    #[test]
    fn delta_congruence_counterexample_reported() {
        let p = BoolAllZeroNonconstant;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![false, true]).unwrap();
        match vc.validate_delta_congruence() {
            Err(PrimitiveDifferenceError::DeltaCongruenceFailure { .. }) => {}
            other => panic!("expected DeltaCongruenceFailure, got {other:?}"),
        }
    }

    struct ParityDifference;
    impl PrimitiveDifference for ParityDifference {
        type Carrier = i64;
        type Diff = i64;
        fn delta(&self, x: &i64, y: &i64) -> i64 {
            (x - y).rem_euclid(2)
        }
        fn zero(&self, d: &i64) -> bool {
            *d == 0
        }
    }

    #[test]
    fn parity_difference_descends() {
        let p = ParityDifference;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        assert_eq!(vc.num_classes(), 2);
        assert!(vc.delta_congruent_on_domain());
        let factor = vc.try_delta_factor().expect("congruent ⇒ factor exists");
        let c_even = vc.class_of_index(0).unwrap();
        let c_odd = vc.class_of_index(1).unwrap();
        assert_eq!(factor.apply(c_even, c_odd), Some(1));
    }

    #[test]
    fn delta_factor_returns_same_value_for_representatives() {
        let p = ParityDifference;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        let factor = vc.try_delta_factor().unwrap();
        assert_eq!(vc.class_of_index(0), vc.class_of_index(2));
        assert_eq!(vc.class_of_index(1), vc.class_of_index(3));
        let a = factor.apply(vc.class_of_index(0).unwrap(), vc.class_of_index(1).unwrap());
        let b = factor.apply(vc.class_of_index(2).unwrap(), vc.class_of_index(3).unwrap());
        assert_eq!(a, b);
    }

    #[test]
    fn class_of_index_is_domain_scoped() {
        let p = ParityDifference;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        assert!(vc.class_of_index(0).is_some());
        assert!(vc.class_of_index(3).is_some());
        assert!(vc.class_of_index(4).is_none());
    }

    #[test]
    fn cross_carrier_quotient_class_rejected() {
        let p = ParityDifference;
        let a = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        let b = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        assert_ne!(a.carrier_id(), b.carrier_id());
        let fa = a.try_delta_factor().unwrap();
        let class_from_b = b.class_of_index(0).unwrap();
        assert_eq!(fa.apply(class_from_b, class_from_b), None);
    }

    struct IntDiff(fn(i64) -> bool);
    impl PrimitiveDifference for IntDiff {
        type Carrier = i64;
        type Diff = i64;
        fn delta(&self, x: &i64, y: &i64) -> i64 {
            x - y
        }
        fn zero(&self, d: &i64) -> bool {
            (self.0)(*d)
        }
    }

    #[test]
    fn zero_rel_not_reflexive_rejected() {
        let p = IntDiff(|_d| false);
        assert_eq!(
            ValidatedFiniteCarrier::try_new(&p, vec![0]).err(),
            Some(PrimitiveDifferenceError::ZeroReflexivityFailure { x: 0 })
        );
    }

    #[test]
    fn zero_rel_not_symmetric_rejected() {
        let p = IntDiff(|d| d == 0 || d == 2);
        match ValidatedFiniteCarrier::try_new(&p, vec![0, 2]).err() {
            Some(PrimitiveDifferenceError::ZeroSymmetryFailure { .. }) => {}
            other => panic!("expected ZeroSymmetryFailure, got {other:?}"),
        }
    }

    #[test]
    fn zero_rel_not_transitive_rejected() {
        let p = IntDiff(|d| d.abs() <= 1);
        let domain = vec![0, 1, 2];
        match ValidatedFiniteCarrier::try_new(&p, domain.clone()).err() {
            Some(PrimitiveDifferenceError::ZeroTransitivityFailure { x, y, z }) => {
                assert!(p.zero_rel(&domain[x], &domain[y]));
                assert!(p.zero_rel(&domain[y], &domain[z]));
                assert!(!p.zero_rel(&domain[x], &domain[z]));
            }
            other => panic!("expected ZeroTransitivityFailure, got {other:?}"),
        }
    }

    #[test]
    fn quotient_class_is_opaque_and_well_formed() {
        let p = ParityDifference;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        for q in vc.residual_quotient() {
            assert!(q.index() < vc.num_classes());
            assert_eq!(q.carrier_id(), vc.carrier_id());
        }
    }

    #[test]
    fn finite_domain_scope_not_global_claim() {
        let p = ParityDifference;
        let two = ValidatedFiniteCarrier::try_new(&p, vec![0, 1]).unwrap();
        let one = ValidatedFiniteCarrier::try_new(&p, vec![0, 2]).unwrap();
        assert_eq!(two.num_classes(), 2);
        assert_eq!(one.num_classes(), 1);
    }

    #[test]
    fn observable_descends_iff_congruent_on_domain() {
        let p = ParityDifference;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        assert!(vc.observable_descends_on_domain(|x: &i64| x.rem_euclid(2)));
        assert!(!vc.observable_descends_on_domain(|x: &i64| *x));
    }

    #[test]
    fn lggr_local_green_global_red_pair_obstruction() {
        let p = ParityDifference;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        let lggr = vc.local_green_global_red(|x: &i64| x.rem_euclid(2), |x: &i64| *x);
        assert!(lggr.left_descends);
        assert!(!lggr.right_descends);
        assert!(!lggr.pair_descends);
        assert!(lggr.counterexample.is_some());
        match vc.validate_pair_descent_on_domain(|x: &i64| x.rem_euclid(2), |x: &i64| *x) {
            Err(PrimitiveDifferenceError::PairCongruenceFailure { .. }) => {}
            other => panic!("expected PairCongruenceFailure, got {other:?}"),
        }
    }

    #[test]
    fn lggr_both_descend_pair_descends() {
        let p = ParityDifference;
        let vc = ValidatedFiniteCarrier::try_new(&p, vec![0, 1, 2, 3]).unwrap();
        let lggr = vc.local_green_global_red(|x: &i64| x.rem_euclid(2), |_x: &i64| 0i64);
        assert!(lggr.left_descends && lggr.right_descends && lggr.pair_descends);
        assert!(lggr.counterexample.is_none());
        assert!(vc
            .validate_pair_descent_on_domain(|x: &i64| x.rem_euclid(2), |_x: &i64| 0i64)
            .is_ok());
    }

    #[derive(Default)]
    struct CountingParity {
        delta_calls: Cell<usize>,
    }

    impl CountingParity {
        fn reset(&self) {
            self.delta_calls.set(0);
        }

        fn calls(&self) -> usize {
            self.delta_calls.get()
        }
    }

    impl PrimitiveDifference for CountingParity {
        type Carrier = i64;
        type Diff = i64;

        fn delta(&self, x: &i64, y: &i64) -> i64 {
            self.delta_calls.set(self.delta_calls.get() + 1);
            (x - y).rem_euclid(2)
        }

        fn zero(&self, d: &i64) -> bool {
            *d == 0
        }
    }

    #[test]
    fn validation_and_descent_have_bounded_evaluation_counts() {
        const DOMAIN_LEN: usize = 128;
        let difference = CountingParity::default();
        let domain = (0..DOMAIN_LEN as i64).collect();
        let carrier = ValidatedFiniteCarrier::try_new(&difference, domain).unwrap();

        assert_eq!(difference.calls(), DOMAIN_LEN * DOMAIN_LEN);
        difference.reset();
        for i in 0..DOMAIN_LEN {
            assert!(carrier.class_of_index(i).is_some());
        }
        assert_eq!(difference.calls(), 0);

        assert!(carrier.delta_congruent_on_domain());
        assert_eq!(difference.calls(), DOMAIN_LEN * DOMAIN_LEN + 4);

        let observable_calls = Cell::new(0);
        assert!(carrier.observable_descends_on_domain(|x: &i64| {
            observable_calls.set(observable_calls.get() + 1);
            x.rem_euclid(2)
        }));
        assert_eq!(observable_calls.get(), DOMAIN_LEN);

        let left_calls = Cell::new(0);
        let right_calls = Cell::new(0);
        assert!(carrier
            .validate_pair_descent_on_domain(
                |x: &i64| {
                    left_calls.set(left_calls.get() + 1);
                    x.rem_euclid(2)
                },
                |_x: &i64| {
                    right_calls.set(right_calls.get() + 1);
                    0
                },
            )
            .is_ok());
        assert_eq!(left_calls.get(), DOMAIN_LEN);
        assert_eq!(right_calls.get(), DOMAIN_LEN);
    }
}
