//! Separation of finite section records with declared domains, and the
//! quotient identity of an exact rational pseudometric.
//!
//! AuthorityEffect: None.
//!
//! A section record is `(id, D, v)` with a unique identity, an explicit finite
//! coordinate set `D` and a total table `v: D -> Q`. Equal list lengths do not
//! identify coordinate sets: records are compared only on a declared common
//! domain, and a record on another domain is refused as incomparable.
//!
//! For an admitted finite pseudometric `d` on record identities and an
//! admitted equivalence `E`, with `Z = {(s,t) : d(s,t) = 0}`:
//!
//! * the inherited distance on `S/E` is well defined exactly when `E ⊆ Z`
//!   (otherwise `IdentificationNotZero`);
//! * it separates classes exactly when `E = Z` (otherwise `ZeroCollision`);
//! * with at least two classes, `Δ = min{d(s,t) : not E(s,t)}` is positive and
//!   attained (otherwise `NoDistinctClasses` for one class).
//!
//! An ε-decoder bounds every report fiber by `2ε`; with `2ε < Δ` the
//! class-valued query factors through the report, decided by the DP-1 owner
//! [`crate::finite_report_query`]. All arithmetic is exact (`BigRational`).

use crate::finite_report_query::{
    FactorizationCertificate, ReportQueryDecision, ReportQueryProblem, ReportQueryRefusal,
};
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt;

/// Upper bound on the number of points admitted to a pseudometric. The
/// triangle check is cubic; larger inputs are refused, never answered.
pub const MAX_PSEUDOMETRIC_POINTS: usize = 512;

/// Which pseudometric law failed, with the points that witness it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PseudometricLaw<I> {
    Negative { left: I, right: I },
    NonzeroDiagonal { point: I },
    Asymmetric { left: I, right: I },
    Triangle { left: I, middle: I, right: I },
}

/// Which equivalence law failed, with the witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EquivalenceLaw<I> {
    UnknownPoint { point: I },
    Reflexivity { point: I },
    Symmetry { left: I, right: I },
    Transitivity { left: I, middle: I, right: I },
    OverlappingClasses { point: I },
    UncoveredPoint { point: I },
}

/// Typed refusals. None of them is a separation verdict.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SeparationRefusal<I, P> {
    DuplicateSectionIdentity { id: I },
    DuplicateCoordinate { id: Option<I>, coordinate: P },
    SectionDomainMismatch { id: I, coordinate: P },
    IncomparableDomains { id: I },
    InvalidWeight { coordinate: P },
    DuplicatePair { left: I, right: I },
    MissingPair { left: I, right: I },
    UnknownPoint { point: I },
    NoComparablePairs,
    NoDistinctClasses,
    InvalidPseudometric(PseudometricLaw<I>),
    InvalidEquivalence(EquivalenceLaw<I>),
    IdentificationNotZero { left: I, right: I, distance: BigRational },
    CarrierMismatch,
    NegativeEpsilon,
    DecoderErrorExceeds { output: I, distance: BigRational },
    OutputZeroCollision { left: I, right: I },
    ThresholdNotStrict { twice_epsilon: BigRational, gap: BigRational },
    ReportQuery(String),
    ResourceLimit,
}

impl<I: fmt::Debug, P: fmt::Debug> fmt::Display for SeparationRefusal<I, P> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

impl<I: fmt::Debug, P: fmt::Debug> std::error::Error for SeparationRefusal<I, P> {}

/// A section record with an explicit coordinate set and a total value table.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SectionRecord<I, P> {
    id: I,
    values: BTreeMap<P, BigRational>,
}

impl<I, P> SectionRecord<I, P>
where
    I: Ord + Clone + fmt::Debug,
    P: Ord + Clone + fmt::Debug,
{
    /// Admits a record: `domain` enumerates `D` without repeats and `rows`
    /// is exactly one value for every coordinate of `D`.
    pub fn new(
        id: I,
        domain: &[P],
        rows: &[(P, BigRational)],
    ) -> Result<Self, SeparationRefusal<I, P>> {
        let mut declared = BTreeSet::new();
        for p in domain {
            if !declared.insert(p.clone()) {
                return Err(SeparationRefusal::DuplicateCoordinate {
                    id: Some(id),
                    coordinate: p.clone(),
                });
            }
        }
        let mut values = BTreeMap::new();
        for (p, v) in rows {
            if !declared.contains(p) {
                return Err(SeparationRefusal::SectionDomainMismatch {
                    id,
                    coordinate: p.clone(),
                });
            }
            if values.insert(p.clone(), v.clone()).is_some() {
                return Err(SeparationRefusal::DuplicateCoordinate {
                    id: Some(id),
                    coordinate: p.clone(),
                });
            }
        }
        if let Some(p) = declared.iter().find(|p| !values.contains_key(*p)) {
            return Err(SeparationRefusal::SectionDomainMismatch {
                id,
                coordinate: p.clone(),
            });
        }
        Ok(Self { id, values })
    }

    pub fn id(&self) -> &I {
        &self.id
    }

    pub fn domain(&self) -> BTreeSet<P> {
        self.values.keys().cloned().collect()
    }

    pub fn values(&self) -> &BTreeMap<P, BigRational> {
        &self.values
    }
}

/// An admitted finite pseudometric: a complete exact rational table on all
/// ordered pairs that passed nonnegativity, zero diagonal, symmetry and the
/// triangle inequality.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinitePseudometric<I> {
    points: BTreeSet<I>,
    distance: BTreeMap<(I, I), BigRational>,
}

impl<I> FinitePseudometric<I>
where
    I: Ord + Clone + fmt::Debug,
{
    /// Admits a complete ordered-pair table.
    pub fn new<P>(
        points: &[I],
        rows: &[((I, I), BigRational)],
    ) -> Result<Self, SeparationRefusal<I, P>> {
        if points.len() > MAX_PSEUDOMETRIC_POINTS {
            return Err(SeparationRefusal::ResourceLimit);
        }
        let mut set = BTreeSet::new();
        for p in points {
            if !set.insert(p.clone()) {
                return Err(SeparationRefusal::DuplicateSectionIdentity { id: p.clone() });
            }
        }
        let mut distance = BTreeMap::new();
        for ((l, r), v) in rows {
            if !set.contains(l) {
                return Err(SeparationRefusal::UnknownPoint { point: l.clone() });
            }
            if !set.contains(r) {
                return Err(SeparationRefusal::UnknownPoint { point: r.clone() });
            }
            if distance.insert((l.clone(), r.clone()), v.clone()).is_some() {
                return Err(SeparationRefusal::DuplicatePair {
                    left: l.clone(),
                    right: r.clone(),
                });
            }
        }
        for l in &set {
            for r in &set {
                if !distance.contains_key(&(l.clone(), r.clone())) {
                    return Err(SeparationRefusal::MissingPair {
                        left: l.clone(),
                        right: r.clone(),
                    });
                }
            }
        }
        let metric = Self {
            points: set,
            distance,
        };
        metric
            .check_laws()
            .map_err(SeparationRefusal::InvalidPseudometric)?;
        Ok(metric)
    }

    fn get(&self, l: &I, r: &I) -> BigRational {
        self.distance
            .get(&(l.clone(), r.clone()))
            .cloned()
            .unwrap_or_else(BigRational::zero)
    }

    /// Re-checks every pseudometric law on the stored table.
    pub fn check_laws(&self) -> Result<(), PseudometricLaw<I>> {
        for l in &self.points {
            if !self.get(l, l).is_zero() {
                return Err(PseudometricLaw::NonzeroDiagonal { point: l.clone() });
            }
            for r in &self.points {
                let d = self.get(l, r);
                if d.is_negative() {
                    return Err(PseudometricLaw::Negative {
                        left: l.clone(),
                        right: r.clone(),
                    });
                }
                if d != self.get(r, l) {
                    return Err(PseudometricLaw::Asymmetric {
                        left: l.clone(),
                        right: r.clone(),
                    });
                }
            }
        }
        for l in &self.points {
            for m in &self.points {
                let lm = self.get(l, m);
                for r in &self.points {
                    if self.get(l, r) > &lm + self.get(m, r) {
                        return Err(PseudometricLaw::Triangle {
                            left: l.clone(),
                            middle: m.clone(),
                            right: r.clone(),
                        });
                    }
                }
            }
        }
        Ok(())
    }

    pub fn points(&self) -> &BTreeSet<I> {
        &self.points
    }

    /// The distance between two admitted points, `None` for an unknown point.
    pub fn distance(&self, l: &I, r: &I) -> Option<&BigRational> {
        self.distance.get(&(l.clone(), r.clone()))
    }

    /// Restriction to a subset of the points (a pseudometric again).
    pub fn restrict<P>(&self, subset: &BTreeSet<I>) -> Result<Self, SeparationRefusal<I, P>> {
        if let Some(p) = subset.iter().find(|p| !self.points.contains(*p)) {
            return Err(SeparationRefusal::UnknownPoint { point: p.clone() });
        }
        let distance = self
            .distance
            .iter()
            .filter(|((l, r), _)| subset.contains(l) && subset.contains(r))
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect();
        Ok(Self {
            points: subset.clone(),
            distance,
        })
    }
}

/// The weighted coordinate pseudometric `d(s,t) = Σ_x w_x |v_s(x) − v_t(x)|`
/// on a declared common domain. Every record must have exactly that domain
/// (else `IncomparableDomains`); weights must be total on it and
/// nonnegative (zero weights admit a pseudometric that does not separate
/// functions); at least two records are required (else `NoComparablePairs`).
pub fn weighted_coordinate_pseudometric<I, P>(
    records: &[SectionRecord<I, P>],
    common_domain: &[P],
    weights: &[(P, BigRational)],
) -> Result<FinitePseudometric<I>, SeparationRefusal<I, P>>
where
    I: Ord + Clone + fmt::Debug,
    P: Ord + Clone + fmt::Debug,
{
    let mut domain = BTreeSet::new();
    for p in common_domain {
        if !domain.insert(p.clone()) {
            return Err(SeparationRefusal::DuplicateCoordinate {
                id: None,
                coordinate: p.clone(),
            });
        }
    }
    let mut w = BTreeMap::new();
    for (p, v) in weights {
        if !domain.contains(p) || v.is_negative() || w.insert(p.clone(), v.clone()).is_some() {
            return Err(SeparationRefusal::InvalidWeight {
                coordinate: p.clone(),
            });
        }
    }
    if let Some(p) = domain.iter().find(|p| !w.contains_key(*p)) {
        return Err(SeparationRefusal::InvalidWeight {
            coordinate: p.clone(),
        });
    }
    let mut ids = Vec::with_capacity(records.len());
    let mut seen = BTreeSet::new();
    for r in records {
        if !seen.insert(r.id.clone()) {
            return Err(SeparationRefusal::DuplicateSectionIdentity { id: r.id.clone() });
        }
        if r.domain() != domain {
            return Err(SeparationRefusal::IncomparableDomains { id: r.id.clone() });
        }
        ids.push(r.id.clone());
    }
    if records.len() < 2 {
        return Err(SeparationRefusal::NoComparablePairs);
    }
    let mut rows = Vec::new();
    for s in records {
        for t in records {
            let mut total = BigRational::zero();
            for (p, wp) in &w {
                let (Some(a), Some(b)) = (s.values.get(p), t.values.get(p)) else {
                    return Err(SeparationRefusal::IncomparableDomains { id: s.id.clone() });
                };
                total += wp * (a - b).abs();
            }
            rows.push(((s.id.clone(), t.id.clone()), total));
        }
    }
    FinitePseudometric::new(&ids, &rows)
}

/// An admitted equivalence relation on a declared finite point set.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FiniteEquivalence<I> {
    points: BTreeSet<I>,
    related: BTreeSet<(I, I)>,
}

impl<I> FiniteEquivalence<I>
where
    I: Ord + Clone + fmt::Debug,
{
    /// Admits an explicit relation. It is never closed silently: missing
    /// reflexive, symmetric or transitive pairs are refused with a witness.
    pub fn from_pairs<P>(
        points: &[I],
        pairs: &[(I, I)],
    ) -> Result<Self, SeparationRefusal<I, P>> {
        let mut set = BTreeSet::new();
        for p in points {
            if !set.insert(p.clone()) {
                return Err(SeparationRefusal::DuplicateSectionIdentity { id: p.clone() });
            }
        }
        let mut related = BTreeSet::new();
        for (l, r) in pairs {
            for p in [l, r] {
                if !set.contains(p) {
                    return Err(SeparationRefusal::InvalidEquivalence(
                        EquivalenceLaw::UnknownPoint { point: p.clone() },
                    ));
                }
            }
            related.insert((l.clone(), r.clone()));
        }
        let e = Self {
            points: set,
            related,
        };
        e.check_laws().map_err(SeparationRefusal::InvalidEquivalence)?;
        Ok(e)
    }

    /// Admits a partition: classes must be disjoint and cover the points.
    pub fn from_classes<P>(
        points: &[I],
        classes: &[Vec<I>],
    ) -> Result<Self, SeparationRefusal<I, P>> {
        let mut owner: BTreeMap<I, usize> = BTreeMap::new();
        for (k, class) in classes.iter().enumerate() {
            for p in class {
                if owner.insert(p.clone(), k).is_some() {
                    return Err(SeparationRefusal::InvalidEquivalence(
                        EquivalenceLaw::OverlappingClasses { point: p.clone() },
                    ));
                }
            }
        }
        for p in points {
            if !owner.contains_key(p) {
                return Err(SeparationRefusal::InvalidEquivalence(
                    EquivalenceLaw::UncoveredPoint { point: p.clone() },
                ));
            }
        }
        let mut pairs = Vec::new();
        for class in classes {
            for l in class {
                for r in class {
                    pairs.push((l.clone(), r.clone()));
                }
            }
        }
        Self::from_pairs(points, &pairs)
    }

    /// Re-checks reflexivity, symmetry and transitivity.
    pub fn check_laws(&self) -> Result<(), EquivalenceLaw<I>> {
        for p in &self.points {
            if !self.related(p, p) {
                return Err(EquivalenceLaw::Reflexivity { point: p.clone() });
            }
        }
        for (l, r) in &self.related {
            if !self.related(r, l) {
                return Err(EquivalenceLaw::Symmetry {
                    left: l.clone(),
                    right: r.clone(),
                });
            }
        }
        for (l, m) in &self.related {
            for (m2, r) in &self.related {
                if m == m2 && !self.related(l, r) {
                    return Err(EquivalenceLaw::Transitivity {
                        left: l.clone(),
                        middle: m.clone(),
                        right: r.clone(),
                    });
                }
            }
        }
        Ok(())
    }

    pub fn related(&self, l: &I, r: &I) -> bool {
        self.related.contains(&(l.clone(), r.clone()))
    }

    pub fn points(&self) -> &BTreeSet<I> {
        &self.points
    }

    /// The classes, each as an ordered set, ordered by least element.
    pub fn classes(&self) -> Vec<BTreeSet<I>> {
        let mut out: Vec<BTreeSet<I>> = Vec::new();
        let mut done = BTreeSet::new();
        for p in &self.points {
            if done.contains(p) {
                continue;
            }
            let class: BTreeSet<I> = self
                .points
                .iter()
                .filter(|q| self.related(p, q))
                .cloned()
                .collect();
            done.extend(class.iter().cloned());
            out.push(class);
        }
        out
    }

    /// The least element of the class of `p`, if `p` is a point.
    pub fn class_representative(&self, p: &I) -> Option<I> {
        self.points.iter().find(|q| self.related(p, q)).cloned()
    }

    /// Restriction to a subset (an equivalence again).
    pub fn restrict<P>(&self, subset: &BTreeSet<I>) -> Result<Self, SeparationRefusal<I, P>> {
        if let Some(p) = subset.iter().find(|p| !self.points.contains(*p)) {
            return Err(SeparationRefusal::UnknownPoint { point: p.clone() });
        }
        Ok(Self {
            points: subset.clone(),
            related: self
                .related
                .iter()
                .filter(|(l, r)| subset.contains(l) && subset.contains(r))
                .cloned()
                .collect(),
        })
    }
}

/// The two separation verdicts on admitted input.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SeparationOutcome<I> {
    /// `E ⊆ Z` holds, but `(left, right)` is at distance zero and not equivalent.
    ZeroCollision { left: I, right: I },
    /// `E = Z`, at least two classes, gap `Δ > 0` attained at `attaining_pair`.
    Separated {
        classes: Vec<BTreeSet<I>>,
        pair_distances: BTreeMap<(I, I), BigRational>,
        gap: BigRational,
        attaining_pair: (I, I),
    },
}

/// Decides separation of `S/E` under `d` over the complete pair set.
pub fn decide_separation<I, P>(
    metric: &FinitePseudometric<I>,
    equivalence: &FiniteEquivalence<I>,
) -> Result<SeparationOutcome<I>, SeparationRefusal<I, P>>
where
    I: Ord + Clone + fmt::Debug,
{
    if metric.points != equivalence.points {
        return Err(SeparationRefusal::CarrierMismatch);
    }
    if metric.points.len() < 2 {
        return Err(SeparationRefusal::NoComparablePairs);
    }
    // E ⊆ Z, on every pair including the diagonal.
    for ((l, r), d) in &metric.distance {
        if equivalence.related(l, r) && !d.is_zero() {
            return Err(SeparationRefusal::IdentificationNotZero {
                left: l.clone(),
                right: r.clone(),
                distance: d.clone(),
            });
        }
    }
    // Z ⊆ E.
    for ((l, r), d) in &metric.distance {
        if l < r && d.is_zero() && !equivalence.related(l, r) {
            return Ok(SeparationOutcome::ZeroCollision {
                left: l.clone(),
                right: r.clone(),
            });
        }
    }
    let classes = equivalence.classes();
    if classes.len() < 2 {
        return Err(SeparationRefusal::NoDistinctClasses);
    }
    let mut pair_distances = BTreeMap::new();
    let mut best: Option<((I, I), BigRational)> = None;
    for ((l, r), d) in &metric.distance {
        if l >= r {
            continue;
        }
        pair_distances.insert((l.clone(), r.clone()), d.clone());
        if equivalence.related(l, r) {
            continue;
        }
        let better = match &best {
            None => true,
            Some((_, g)) => d < g,
        };
        if better {
            best = Some(((l.clone(), r.clone()), d.clone()));
        }
    }
    let Some((attaining_pair, gap)) = best else {
        return Err(SeparationRefusal::NoDistinctClasses);
    };
    Ok(SeparationOutcome::Separated {
        classes,
        pair_distances,
        gap,
        attaining_pair,
    })
}

/// Why a separation verdict failed replay.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SeparationReplayFailure {
    VerdictDiffers,
    ClassesMismatch,
    PairTableMismatch,
    GapNotPositive,
    AttainingPairNotInterclass,
    AttainingPairDistanceMismatch,
    GapNotLowerBound,
    CollisionNotZero,
    CollisionEquivalent,
    CollisionPointUnknown,
}

/// Replays a separation verdict against the admitted inputs without trusting
/// the producer: each field is recomputed or checked against the table.
pub fn verify_separation<I>(
    metric: &FinitePseudometric<I>,
    equivalence: &FiniteEquivalence<I>,
    outcome: &SeparationOutcome<I>,
) -> Result<(), SeparationReplayFailure>
where
    I: Ord + Clone + fmt::Debug,
{
    match outcome {
        SeparationOutcome::ZeroCollision { left, right } => {
            let Some(d) = metric.distance(left, right) else {
                return Err(SeparationReplayFailure::CollisionPointUnknown);
            };
            if !d.is_zero() {
                return Err(SeparationReplayFailure::CollisionNotZero);
            }
            if equivalence.related(left, right) {
                return Err(SeparationReplayFailure::CollisionEquivalent);
            }
            Ok(())
        }
        SeparationOutcome::Separated {
            classes,
            pair_distances,
            gap,
            attaining_pair,
        } => {
            let recomputed: Result<SeparationOutcome<I>, SeparationRefusal<I, ()>> =
                decide_separation(metric, equivalence);
            if !matches!(recomputed, Ok(SeparationOutcome::Separated { .. })) {
                return Err(SeparationReplayFailure::VerdictDiffers);
            }
            if *classes != equivalence.classes() {
                return Err(SeparationReplayFailure::ClassesMismatch);
            }
            let expected: BTreeMap<(I, I), BigRational> = metric
                .distance
                .iter()
                .filter(|((l, r), _)| l < r)
                .map(|(k, v)| (k.clone(), v.clone()))
                .collect();
            if *pair_distances != expected {
                return Err(SeparationReplayFailure::PairTableMismatch);
            }
            if !gap.is_positive() {
                return Err(SeparationReplayFailure::GapNotPositive);
            }
            let (a, b) = attaining_pair;
            if equivalence.related(a, b) || metric.distance(a, b).is_none() {
                return Err(SeparationReplayFailure::AttainingPairNotInterclass);
            }
            if metric.distance(a, b) != Some(gap) {
                return Err(SeparationReplayFailure::AttainingPairDistanceMismatch);
            }
            for ((l, r), d) in &expected {
                if !equivalence.related(l, r) && d < gap {
                    return Err(SeparationReplayFailure::GapNotLowerBound);
                }
            }
            Ok(())
        }
    }
}

/// Result of the ε-decoder threshold argument.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClassFactorization<X, A, I> {
    /// Largest output distance inside one report fiber (at most `2ε`).
    pub fiber_diameter: BigRational,
    pub twice_epsilon: BigRational,
    pub gap: BigRational,
    /// DP-1 certificate for the class-valued query `x ↦ [q(x)]`, classes
    /// named by their least element.
    pub certificate: FactorizationCertificate<X, A, I>,
}

/// The ε-decoder argument (S5–S6). `ambient` is an admitted pseudometric on
/// output points with equivalence `equivalence`; `report_rows` and
/// `query_rows` are total tables on `source`; `decoder_rows` is a total table
/// on the realized report image into `ambient`. Checks `ε ≥ 0` and
/// `d(q(x), D(p(x))) ≤ ε` for every `x`, computes the fiber diameter, decides
/// separation on the family of outputs `q(X)`, requires `2ε < Δ`, and then
/// decides the class-valued query with the DP-1 owner.
#[allow(clippy::too_many_arguments)]
pub fn epsilon_decoder_class_factorization<X, A, I>(
    ambient: &FinitePseudometric<I>,
    equivalence: &FiniteEquivalence<I>,
    source: &[X],
    report_codomain: &[A],
    report_rows: &[(X, A)],
    query_rows: &[(X, I)],
    decoder_rows: &[(A, I)],
    epsilon: &BigRational,
) -> Result<ClassFactorization<X, A, I>, SeparationRefusal<I, X>>
where
    X: Ord + Clone + fmt::Debug,
    A: Ord + Clone + fmt::Debug,
    I: Ord + Clone + fmt::Debug,
{
    if ambient.points != equivalence.points {
        return Err(SeparationRefusal::CarrierMismatch);
    }
    if epsilon.is_negative() {
        return Err(SeparationRefusal::NegativeEpsilon);
    }
    let outputs: Vec<I> = ambient.points.iter().cloned().collect();
    let problem = ReportQueryProblem::new(
        source,
        report_codomain,
        &outputs,
        report_rows,
        query_rows,
    )
    .map_err(|e: ReportQueryRefusal<X>| SeparationRefusal::ReportQuery(format!("{e:?}")))?;
    let image = problem.realized_image();
    let decoder = crate::finite_report_query::admit_total_table(
        &image,
        &ambient.points,
        decoder_rows,
        crate::finite_report_query::MapRole::Refinement,
    )
    .map_err(|e: ReportQueryRefusal<A>| SeparationRefusal::ReportQuery(format!("{e:?}")))?;
    for (x, a) in problem.report() {
        let (Some(qx), Some(da)) = (problem.query().get(x), decoder.get(a)) else {
            return Err(SeparationRefusal::ReportQuery("decoder not total".into()));
        };
        let d = ambient.get(qx, da);
        if &d > epsilon {
            return Err(SeparationRefusal::DecoderErrorExceeds {
                output: qx.clone(),
                distance: d,
            });
        }
    }
    let mut fiber_diameter = BigRational::zero();
    for (x, a) in problem.report() {
        for (y, b) in problem.report() {
            if a != b {
                continue;
            }
            if let (Some(qx), Some(qy)) = (problem.query().get(x), problem.query().get(y)) {
                let d = ambient.get(qx, qy);
                if d > fiber_diameter {
                    fiber_diameter = d;
                }
            }
        }
    }
    let twice_epsilon = epsilon + epsilon;
    let output_set: BTreeSet<I> = problem.query().values().cloned().collect();
    let sub_metric = ambient.restrict::<X>(&output_set)?;
    let sub_eq = equivalence.restrict::<X>(&output_set)?;
    let gap = match decide_separation::<I, X>(&sub_metric, &sub_eq)? {
        SeparationOutcome::Separated { gap, .. } => gap,
        SeparationOutcome::ZeroCollision { left, right } => {
            return Err(SeparationRefusal::OutputZeroCollision { left, right })
        }
    };
    if twice_epsilon >= gap {
        return Err(SeparationRefusal::ThresholdNotStrict { twice_epsilon, gap });
    }
    let class_rows: Vec<(X, I)> = problem
        .query()
        .iter()
        .filter_map(|(x, q)| equivalence.class_representative(q).map(|c| (x.clone(), c)))
        .collect();
    let class_problem = ReportQueryProblem::new(
        source,
        report_codomain,
        &outputs,
        report_rows,
        &class_rows,
    )
    .map_err(|e: ReportQueryRefusal<X>| SeparationRefusal::ReportQuery(format!("{e:?}")))?;
    match class_problem.decide() {
        ReportQueryDecision::Factorable(certificate) => Ok(ClassFactorization {
            fiber_diameter,
            twice_epsilon,
            gap,
            certificate,
        }),
        ReportQueryDecision::Collision(c) => Err(SeparationRefusal::ReportQuery(format!(
            "class collision under 2ε < Δ: {c:?}"
        ))),
    }
}
