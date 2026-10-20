// Finite dependent products of explicitly supplied finite set fibers.
// This does not interpret arbitrary HoTT references or establish univalence.
// AuthorityEffect: None.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FinitePiLimits {
    pub max_fibers: usize,
    pub max_reference_bytes: usize,
    pub max_cardinality: usize,
    /// Conservative per-call storage visits and native arithmetic steps;
    /// excludes caller-owned input/output allocation and elapsed time.
    pub max_work: usize,
}

impl Default for FinitePiLimits {
    fn default() -> Self {
        Self { max_fibers: 4096, max_reference_bytes: 65536,
            max_cardinality: 1_000_000, max_work: 1_000_000 }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum FinitePiError {
    #[error(transparent)]
    Presentation(#[from] PiTypeError),
    #[error("finite dependent-product size arithmetic overflows usize")]
    SizeOverflow,
    #[error("{resource} needs {requested} units, above limit {limit}")]
    Limit { resource: &'static str, requested: usize, limit: usize },
    #[error("section has {actual} coordinates, expected {expected}")]
    Arity { expected: usize, actual: usize },
    #[error("the dependent product has no sections")]
    NoSections,
    #[error("section ordinal {ordinal} is outside cardinality {cardinality}")]
    Ordinal { ordinal: usize, cardinality: usize },
    #[error("coordinate {fiber} has value {value}, outside fiber size {size}")]
    Coordinate { fiber: usize, value: usize, size: usize },
}

/// An admitted finite set model of a dependent function space.
///
/// Fiber `i` is the ordinal set `0..fiber_sizes[i]`; sections select one value
/// in each fiber. The empty base has exactly the empty section. Any empty
/// fiber makes the product empty, even if an earlier partial product would
/// overflow. The declaration supplies presentation names, not a proof that
/// a separately named registry denotes these finite fibers.
///
/// Immutable borrows prevent later mutation of the admitted description and
/// fiber slice. Admission, ranking and decoding allocate no owned buffers.
/// Output buffers remain caller-owned and are unchanged on every refusal.
///
/// ```compile_fail
/// use tfqm_homotopy_type_theory::pi_type::{FinitePi, FinitePiLimits, PiType};
/// let declaration = PiType { base_type_ref: "A".into(), family_ref: "B".into() };
/// let _ = FinitePi { declaration: &declaration, fiber_sizes: &[2],
///     cardinality: 1, limits: FinitePiLimits::default() };
/// ```
#[derive(Debug)]
pub struct FinitePi<'a> {
    declaration: &'a PiType,
    fiber_sizes: &'a [usize],
    cardinality: usize,
    limits: FinitePiLimits,
}

fn finite_pi_limit(resource: &'static str, requested: usize, limit: usize) -> Result<(), FinitePiError> {
    if requested > limit { return Err(FinitePiError::Limit { resource, requested, limit }); }
    Ok(())
}

fn finite_pi_work(fibers: usize, factor: usize, limit: usize) -> Result<(), FinitePiError> {
    let requested = fibers.checked_mul(factor).ok_or(FinitePiError::SizeOverflow)?;
    finite_pi_limit("work", requested, limit)
}

fn finite_pi_cardinality(fibers: &[usize]) -> Result<usize, FinitePiError> {
    // Inspect all fibers before multiplying: [MAX, 2, 0] denotes the empty
    // product, not an arithmetic failure in a mathematically unused prefix.
    if fibers.contains(&0) { return Ok(0); }
    fibers.iter().try_fold(1usize, |product, size|
        product.checked_mul(*size).ok_or(FinitePiError::SizeOverflow))
}

impl PiType {
    /// Borrow an explicitly supplied finite family under inclusive limits.
    /// References are validated and byte-budgeted, but not resolved against
    /// any external type registry. No input or output storage is copied.
    pub fn finite_model<'a>(&'a self, fiber_sizes: &'a [usize], limits: FinitePiLimits)
        -> Result<FinitePi<'a>, FinitePiError> {
        self.validate()?;
        let bytes = self.base_type_ref.len().checked_add(self.family_ref.len())
            .ok_or(FinitePiError::SizeOverflow)?;
        finite_pi_limit("reference bytes", bytes, limits.max_reference_bytes)?;
        finite_pi_limit("fibers", fiber_sizes.len(), limits.max_fibers)?;
        finite_pi_work(fiber_sizes.len(), 4, limits.max_work)?;
        let cardinality = finite_pi_cardinality(fiber_sizes)?;
        finite_pi_limit("cardinality", cardinality, limits.max_cardinality)?;
        Ok(FinitePi { declaration: self, fiber_sizes, cardinality, limits })
    }
}

impl<'a> FinitePi<'a> {
    pub fn declaration(&self) -> &'a PiType { self.declaration }
    pub fn fiber_sizes(&self) -> &'a [usize] { self.fiber_sizes }
    pub fn cardinality(&self) -> usize { self.cardinality }

    fn arity(&self, actual: usize) -> Result<(), FinitePiError> {
        if actual != self.fiber_sizes.len() {
            return Err(FinitePiError::Arity { expected: self.fiber_sizes.len(), actual });
        }
        Ok(())
    }

    fn admit_coordinates(&self, coordinates: &[usize]) -> Result<(), FinitePiError> {
        for (fiber, (&value, &size)) in coordinates.iter().zip(self.fiber_sizes).enumerate() {
            if value >= size { return Err(FinitePiError::Coordinate { fiber, value, size }); }
        }
        Ok(())
    }

    /// Lexicographic mixed-radix ordinal, with the last fiber varying fastest.
    /// All coordinates are admitted before any rank arithmetic.
    pub fn rank(&self, coordinates: &[usize]) -> Result<usize, FinitePiError> {
        self.arity(coordinates.len())?;
        finite_pi_work(self.fiber_sizes.len(), 6, self.limits.max_work)?;
        if self.cardinality == 0 { return Err(FinitePiError::NoSections); }
        self.admit_coordinates(coordinates)?;
        coordinates.iter().zip(self.fiber_sizes).try_fold(0usize, |rank, (&value, &size)|
            rank.checked_mul(size).and_then(|value_before| value_before.checked_add(value))
                .ok_or(FinitePiError::SizeOverflow))
    }

    /// Decode an ordinal without allocating. Every possible refusal occurs
    /// before the first output write. Admitted positive cardinality implies
    /// every radix is positive, so division/remainder cannot encounter zero.
    pub fn unrank_into(&self, ordinal: usize, output: &mut [usize]) -> Result<(), FinitePiError> {
        self.arity(output.len())?;
        finite_pi_work(self.fiber_sizes.len(), 4, self.limits.max_work)?;
        if ordinal >= self.cardinality {
            return Err(FinitePiError::Ordinal { ordinal, cardinality: self.cardinality });
        }
        let mut remaining = ordinal;
        for (slot, &size) in output.iter_mut().zip(self.fiber_sizes).rev() {
            *slot = remaining % size;
            remaining /= size;
        }
        Ok(())
    }
}

#[cfg(test)]
mod finite_pi_challenges {
    use super::*;

    fn declaration() -> PiType {
        PiType { base_type_ref: "A".into(), family_ref: "B".into() }
    }
    fn oracle(fibers: &[usize]) -> Vec<Vec<usize>> {
        let mut sections = vec![Vec::new()];
        for size in fibers {
            let mut next = Vec::new();
            for prefix in &sections {
                for value in 0..*size {
                    let mut extended = prefix.clone();
                    extended.push(value);
                    next.push(extended);
                }
            }
            sections = next;
        }
        sections
    }

    #[test]
    fn every_small_finite_family_matches_independent_cartesian_enumeration() {
        let declaration = declaration();
        for count in 0..=4u32 {
            for mut code in 0..4usize.pow(count) {
                let fibers: Vec<_> = (0..count).map(|_| { let value = code % 4; code /= 4; value }).collect();
                let model = declaration.finite_model(&fibers, FinitePiLimits::default()).unwrap();
                let expected = oracle(&fibers);
                assert_eq!(model.cardinality(), expected.len());
                assert_eq!(model.declaration(), &declaration);
                assert_eq!(model.fiber_sizes(), fibers);
                for (ordinal, section) in expected.iter().enumerate() {
                    assert_eq!(model.rank(section), Ok(ordinal));
                    let mut decoded = vec![usize::MAX; fibers.len()];
                    assert_eq!(model.unrank_into(ordinal, &mut decoded), Ok(()));
                    assert_eq!(&decoded, section);
                }
                let mut untouched = vec![11; fibers.len()];
                assert!(matches!(model.unrank_into(expected.len(), &mut untouched), Err(FinitePiError::Ordinal { .. })));
                assert_eq!(untouched, vec![11; fibers.len()]);
            }
        }
    }

    #[test]
    fn empty_base_empty_fibers_and_extreme_ordinals_have_exact_semantics() {
        let declaration = declaration();
        let limits = FinitePiLimits { max_cardinality: usize::MAX, ..FinitePiLimits::default() };
        let empty = declaration.finite_model(&[], limits).unwrap();
        assert_eq!(empty.cardinality(), 1);
        assert_eq!(empty.rank(&[]), Ok(0));
        assert_eq!(empty.unrank_into(0, &mut []), Ok(()));
        let zero = declaration.finite_model(&[usize::MAX, 2, 0], limits).unwrap();
        assert_eq!(zero.cardinality(), 0);
        assert_eq!(zero.rank(&[0, 0, 0]), Err(FinitePiError::NoSections));
        assert!(matches!(declaration.finite_model(&[usize::MAX, 2], limits), Err(FinitePiError::SizeOverflow)));
        let maximum = declaration.finite_model(&[usize::MAX], limits).unwrap();
        assert_eq!(maximum.rank(&[usize::MAX - 1]), Ok(usize::MAX - 1));
        let mut output = [0];
        maximum.unrank_into(usize::MAX - 1, &mut output).unwrap();
        assert_eq!(output, [usize::MAX - 1]);
        assert!(matches!(maximum.rank(&[usize::MAX]), Err(FinitePiError::Coordinate { fiber: 0, .. })));
    }

    #[test]
    fn admission_and_query_limits_are_inclusive_and_refusals_preserve_output() {
        let declaration = declaration();
        let exact = FinitePiLimits { max_fibers: 2, max_reference_bytes: 2, max_cardinality: 6, max_work: 12 };
        let model = declaration.finite_model(&[2, 3], exact).unwrap();
        assert_eq!(model.rank(&[1, 2]), Ok(5));
        for limits in [FinitePiLimits { max_fibers: 1, ..exact },
            FinitePiLimits { max_reference_bytes: 1, ..exact },
            FinitePiLimits { max_cardinality: 5, ..exact },
            FinitePiLimits { max_work: 7, ..exact }] {
            assert!(matches!(declaration.finite_model(&[2, 3], limits), Err(FinitePiError::Limit { .. })));
        }
        let restricted = declaration.finite_model(&[2, 3], FinitePiLimits { max_work: 11, ..exact }).unwrap();
        assert!(matches!(restricted.rank(&[1, 2]), Err(FinitePiError::Limit { resource: "work", requested: 12, limit: 11 })));
        let mut output = [7, 7];
        assert!(matches!(model.unrank_into(6, &mut output), Err(FinitePiError::Ordinal { .. })));
        assert_eq!(output, [7, 7]);
        let mut wrong_arity = [7];
        assert_eq!(model.unrank_into(0, &mut wrong_arity), Err(FinitePiError::Arity { expected: 2, actual: 1 }));
        assert_eq!(wrong_arity, [7]);
        assert!(matches!(model.rank(&[0]), Err(FinitePiError::Arity { .. })));
        assert!(matches!(model.rank(&[0, 3]), Err(FinitePiError::Coordinate { fiber: 1, value: 3, size: 3 })));
        let invalid = PiType { base_type_ref: String::new(), family_ref: "B".into() };
        assert!(matches!(invalid.finite_model(&[], exact), Err(FinitePiError::Presentation(PiTypeError::EmptyBaseTypeRef))));
    }
}
