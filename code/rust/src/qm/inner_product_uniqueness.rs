//! Exact replay of the sector-form uniqueness chain: an inner product on the sector carrier is
//! forced, up to scale, by sector additivity and transitive sector symmetry.
//!
//! Replays in exact rational and Gaussian-rational arithmetic the Lean modules of
//! `dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form`
//! (`SectorFormUniqueness`, `SectorFormHermitian`) and mirrors, function for function, the Python
//! twin `code/python/src/qm/inner_product_uniqueness.py`:
//!
//! * the sector-additivity defects `G_ij + G_ji` of a Gram matrix, and over `ℚ(i)` the two
//!   defects `re(H_ij + H_ji)` and `im(H_ji − H_ij)` read along the directions `1` and `i`;
//! * the diagonal readout `Σ G_ii x_i²` of a sector-additive form (symmetry not required);
//! * the invariance defects `G_{σj,σj} − G_jj` of a sector permutation and the orbit
//!   decomposition of a permutation set;
//! * the scale certificate `G = c·I` (`c = G_00`) with an exact witness for whichever hypothesis
//!   fails first: symmetry, sector additivity, invariance, transitivity;
//! * the countermodels `diag(1, 2)` (sector additive, not invariant under the swap),
//!   `1 + (all ones)` (invariant, not sector additive) and, over `ℚ(i)`, `[[1, i], [−i, 1]]`
//!   (additive along the real direction only).
//!
//! The carrier, the scalar field and the quadratic shape of the readout are supplied; the two
//! laws are hypotheses; only the form is derived. AuthorityEffect: None.
//!
//! Scalars: the crate's `Q` (canonical `BigRational`, admitted through
//! [`validate_rational`]) and [`GaussianRational`] (`Result`-valued arithmetic). Nothing panics
//! on caller data.

use std::collections::BTreeSet;

use num_traits::Zero;

use crate::linear_algebra::scalars::{
    validate_rational, Involution, RationalConstructionError, Ring, ScalarError, Semiring,
};
use crate::linear_algebra::{q, GaussianRational, Q};

pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; the carrier, scalar field \
     and quadratic readout are supplied; sector additivity and transitive sector symmetry are \
     hypotheses; only the form of the inner product is derived; assumptions exposed.";

pub const PROVENANCE: &str = "Replays the Lean modules of \
     dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form \
     (SectorFormUniqueness, SectorFormHermitian) and the Python twin \
     code/python/src/qm/inner_product_uniqueness.py.";

/// A rational Gram matrix as rows; every public entry point re-admits it through [`matrix`].
pub type Matrix = Vec<Vec<Q>>;
/// A rational carrier vector; every public entry point re-admits it through [`vector`].
pub type Vector = Vec<Q>;
/// A sector permutation as its list of images; admitted through [`permutation`].
pub type Permutation = Vec<usize>;
/// A Gaussian-rational Hermitian candidate as rows; admitted through [`hmatrix`].
pub type HMatrix = Vec<Vec<GaussianRational>>;
/// A Gaussian-rational carrier vector; admitted through [`hvector`].
pub type HVector = Vec<GaussianRational>;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum InnerProductUniquenessError {
    #[error("nonempty square matrix required")]
    NonSquareMatrix,
    #[error("nonempty vector required")]
    EmptyVector,
    #[error("exact canonical rational entries required: {0}")]
    InexactEntry(#[from] RationalConstructionError),
    #[error("scalar arithmetic: {0}")]
    Scalar(#[from] ScalarError),
    #[error("{operation}: dimension {expected} expected, got {got}")]
    DimensionMismatch {
        operation: &'static str,
        expected: usize,
        got: usize,
    },
    #[error("index {index} is outside dimension {dimension}")]
    IndexOutOfRange { index: usize, dimension: usize },
    #[error("a permutation of 0..{0} is required")]
    NotAPermutation(usize),
    #[error("disjointly supported vectors required")]
    NotDisjoint,
    #[error("a selected scalar form is required, got {0}")]
    NotSelected(&'static str),
    #[error("nonzero normalisation entry required")]
    ZeroNormalisation,
}

type Error = InnerProductUniquenessError;

/// Outcome of [`sector_additivity_certificate`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AdditivityVerdict {
    /// `qf(x) = Σ diagonal[i]·x_i²`.
    SectorAdditive { diagonal: Vec<Q> },
    /// `u = e_i`, `v = e_j` with `qf(u+v) − qf(u) − qf(v) = defect ≠ 0`.
    NotSectorAdditive {
        i: usize,
        j: usize,
        u: Vector,
        v: Vector,
        defect: Q,
    },
}

/// Outcome of [`invariance_certificate`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InvarianceVerdict {
    Invariant,
    /// `x = e_j` with `qf(permute σ x) = moved ≠ original = qf(x)`.
    NotInvariant {
        j: usize,
        x: Vector,
        moved: Q,
        original: Q,
    },
}

/// Outcome of [`transitivity_certificate`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TransitivityVerdict {
    Transitive,
    /// No supplied permutation sends `i` to `j`; the orbits of the generated group are listed.
    NotTransitive {
        i: usize,
        j: usize,
        orbits: Vec<Vec<usize>>,
    },
}

/// Outcome of [`derive_scale`]: the theorem replayed, or the first failing hypothesis.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SelectionVerdict {
    /// `G = scale·identity` with `scale = G_00`.
    Scalar { scale: Q, identity: Matrix },
    NotSymmetric {
        i: usize,
        j: usize,
    },
    NotSectorAdditive {
        i: usize,
        j: usize,
        u: Vector,
        v: Vector,
        defect: Q,
    },
    NotInvariant {
        sigma: Permutation,
        j: usize,
        x: Vector,
        moved: Q,
        original: Q,
    },
    /// The statement that survives without transitivity: the diagonal is constant on each orbit.
    NotTransitive {
        i: usize,
        j: usize,
        orbits: Vec<Vec<usize>>,
        orbit_values: Vec<Q>,
    },
}

/// Outcome of [`uniqueness_certificate`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UniquenessVerdict {
    /// Equal normalisation entries: the two forms are equal (checked).
    Equal(bool),
    /// `G2 = ratio·G` (checked).
    Proportional { ratio: Q, holds: bool },
}

/// Outcome of [`hermitian_sector_additivity_certificate`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HermitianAdditivityVerdict {
    /// `re(x* H x) = Σ diagonal[i]·|x_i|²`.
    SectorAdditive { diagonal: Vec<Q> },
    /// `u = e_i` and `v = e_j` or `v = i·e_j` with nonzero defect.
    NotSectorAdditive {
        i: usize,
        j: usize,
        u: HVector,
        v: HVector,
        defect: Q,
    },
}

/// Outcome of [`hermitian_derive_scale`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HermitianSelectionVerdict {
    /// `H = scale·identity` with real `scale = re H_00`.
    Scalar { scale: Q, identity: HMatrix },
    NotHermitian {
        i: usize,
        j: usize,
    },
    NotSectorAdditive {
        i: usize,
        j: usize,
        u: HVector,
        v: HVector,
        defect: Q,
    },
    NotInvariant {
        sigma: Permutation,
        j: usize,
        x: HVector,
        moved: Q,
        original: Q,
    },
    NotTransitive {
        i: usize,
        j: usize,
        orbits: Vec<Vec<usize>>,
        orbit_values: Vec<Q>,
    },
}

// ============================================================================
// Exact-input admission and the rational matrix algebra (supplied, not derived)
// ============================================================================

/// Admit a nonempty square matrix of canonical rationals.
pub fn matrix(rows: &[Vec<Q>]) -> Result<Matrix, Error> {
    let n = rows.len();
    if n == 0 || rows.iter().any(|r| r.len() != n) {
        return Err(Error::NonSquareMatrix);
    }
    for x in rows.iter().flatten() {
        validate_rational(x)?;
    }
    Ok(rows.to_vec())
}

/// Admit a nonempty vector of canonical rationals.
pub fn vector(xs: &[Q]) -> Result<Vector, Error> {
    if xs.is_empty() {
        return Err(Error::EmptyVector);
    }
    for x in xs {
        validate_rational(x)?;
    }
    Ok(xs.to_vec())
}

fn same_length(operation: &'static str, expected: usize, got: usize) -> Result<(), Error> {
    if expected == got {
        Ok(())
    } else {
        Err(Error::DimensionMismatch {
            operation,
            expected,
            got,
        })
    }
}

fn index_in(index: usize, dimension: usize) -> Result<(), Error> {
    if index < dimension {
        Ok(())
    } else {
        Err(Error::IndexOutOfRange { index, dimension })
    }
}

/// The identity Gram matrix.
pub fn identity(n: usize) -> Matrix {
    (0..n)
        .map(|i| (0..n).map(|j| if i == j { q(1) } else { q(0) }).collect())
        .collect()
}

/// `c·e_i`.
pub fn unit_vector(n: usize, i: usize, c: &Q) -> Result<Vector, Error> {
    index_in(i, n)?;
    validate_rational(c)?;
    Ok((0..n).map(|k| if k == i { c.clone() } else { q(0) }).collect())
}

/// `A·x`.
pub fn mat_vec(a: &Matrix, x: &Vector) -> Result<Vector, Error> {
    for row in a {
        same_length("mat_vec", row.len(), x.len())?;
    }
    Ok(a.iter()
        .map(|row| row.iter().zip(x).fold(q(0), |acc, (r, v)| acc + r * v))
        .collect())
}

/// `x·y`.
pub fn dot(x: &Vector, y: &Vector) -> Result<Q, Error> {
    same_length("dot", x.len(), y.len())?;
    Ok(x.iter().zip(y).fold(q(0), |acc, (a, b)| acc + a * b))
}

/// The bilinear pairing `x·(G y)`.
pub fn pairing(g: &Matrix, x: &Vector, y: &Vector) -> Result<Q, Error> {
    dot(x, &mat_vec(g, y)?)
}

/// The quadratic readout `x·(G x)`.
pub fn quadratic_form(g: &Matrix, x: &Vector) -> Result<Q, Error> {
    pairing(g, x, x)
}

/// `Gᵀ = G`.
pub fn is_symmetric(g: &Matrix) -> Result<bool, Error> {
    let g = matrix(g)?;
    let n = g.len();
    Ok((0..n).all(|i| (0..n).all(|j| g[i][j] == g[j][i])))
}

// ============================================================================
// Supports and sector permutations
// ============================================================================

/// No sector carries both: for every `k`, `u[k] == 0` or `v[k] == 0`.
pub fn disjoint_support(u: &Vector, v: &Vector) -> Result<bool, Error> {
    same_length("disjoint_support", u.len(), v.len())?;
    Ok(u.iter().zip(v).all(|(a, b)| a.is_zero() || b.is_zero()))
}

/// Admit `sigma` as a list of images, a bijection of `0..n`.
pub fn permutation(sigma: &[usize], n: usize) -> Result<Permutation, Error> {
    let mut seen = vec![false; n];
    if sigma.len() != n {
        return Err(Error::NotAPermutation(n));
    }
    for &k in sigma {
        if k >= n || seen[k] {
            return Err(Error::NotAPermutation(n));
        }
        seen[k] = true;
    }
    Ok(sigma.to_vec())
}

/// `sigma⁻¹`.
pub fn inverse_permutation(sigma: &[usize]) -> Result<Permutation, Error> {
    let s = permutation(sigma, sigma.len())?;
    let mut inv = vec![0; s.len()];
    for (i, &k) in s.iter().enumerate() {
        inv[k] = i;
    }
    Ok(inv)
}

/// `(permute σ x)[i] = x[σ⁻¹(i)]`: the coordinate action with `permute(σ, e_j) = e_{σ(j)}`.
pub fn permute(sigma: &[usize], x: &Vector) -> Result<Vector, Error> {
    let s = permutation(sigma, x.len())?;
    let inv = inverse_permutation(&s)?;
    Ok((0..x.len()).map(|i| x[inv[i]].clone()).collect())
}

/// Orbits of the sectors under the group generated by `perms` (sorted lists).
pub fn orbits(perms: &[Permutation], n: usize) -> Result<Vec<Vec<usize>>, Error> {
    let mut ps = Vec::new();
    for p in perms {
        let p = permutation(p, n)?;
        let inv = inverse_permutation(&p)?;
        ps.push((p, inv));
    }
    let mut seen = vec![false; n];
    let mut out = Vec::new();
    for i in 0..n {
        if seen[i] {
            continue;
        }
        let mut orbit = vec![i];
        let mut stack = vec![i];
        seen[i] = true;
        while let Some(a) = stack.pop() {
            for (p, inv) in &ps {
                for b in [p[a], inv[a]] {
                    if !seen[b] {
                        seen[b] = true;
                        orbit.push(b);
                        stack.push(b);
                    }
                }
            }
        }
        orbit.sort_unstable();
        out.push(orbit);
    }
    Ok(out)
}

/// The group generated by `perms` (identity, products and inverses, sorted): the replay of the
/// inductive predicate `Generated`.
pub fn closure(perms: &[Permutation], n: usize) -> Result<Vec<Permutation>, Error> {
    let mut gens: Vec<Permutation> = Vec::new();
    for p in perms {
        let p = permutation(p, n)?;
        gens.push(inverse_permutation(&p)?);
        gens.push(p);
    }
    let ident: Permutation = (0..n).collect();
    let mut group: BTreeSet<Permutation> = BTreeSet::new();
    group.insert(ident.clone());
    let mut stack = vec![ident];
    while let Some(a) = stack.pop() {
        for g in &gens {
            let b: Permutation = (0..n).map(|i| g[a[i]]).collect();
            if group.insert(b.clone()) {
                stack.push(b);
            }
        }
    }
    Ok(group.into_iter().collect())
}

/// `Transitive` when every pair `(i, j)` with `i ≠ j` has a supplied `σ` with `σ[i] == j`.
pub fn transitivity_certificate(perms: &[Permutation], n: usize) -> Result<TransitivityVerdict, Error> {
    let ps: Vec<Permutation> = perms
        .iter()
        .map(|p| permutation(p, n))
        .collect::<Result<_, _>>()?;
    for i in 0..n {
        for j in 0..n {
            if i != j && !ps.iter().any(|p| p[i] == j) {
                return Ok(TransitivityVerdict::NotTransitive {
                    i,
                    j,
                    orbits: orbits(perms, n)?,
                });
            }
        }
    }
    Ok(TransitivityVerdict::Transitive)
}

/// All permutations of `0..n` (lexicographic).
pub fn all_permutations(n: usize) -> Vec<Permutation> {
    fn go(prefix: &mut Vec<usize>, used: &mut Vec<bool>, out: &mut Vec<Permutation>) {
        if prefix.len() == used.len() {
            out.push(prefix.clone());
            return;
        }
        for k in 0..used.len() {
            if !used[k] {
                used[k] = true;
                prefix.push(k);
                go(prefix, used, out);
                prefix.pop();
                used[k] = false;
            }
        }
    }
    let mut out = Vec::new();
    go(&mut Vec::new(), &mut vec![false; n], &mut out);
    out
}

/// The transposition of sectors `a` and `b`.
pub fn swap(n: usize, a: usize, b: usize) -> Result<Permutation, Error> {
    index_in(a, n)?;
    index_in(b, n)?;
    let mut s: Permutation = (0..n).collect();
    s.swap(a, b);
    Ok(s)
}

// ============================================================================
// Rational sector forms: additivity, invariance, selection
// ============================================================================

/// `qf(u+v) − qf(u) − qf(v)` for disjointly supported `u`, `v` (equal to `pair(u,v) + pair(v,u)`).
pub fn sector_additivity_defect(g: &Matrix, u: &Vector, v: &Vector) -> Result<Q, Error> {
    let g = matrix(g)?;
    let u = vector(u)?;
    let v = vector(v)?;
    if !disjoint_support(&u, &v)? {
        return Err(Error::NotDisjoint);
    }
    let sum: Vector = u.iter().zip(&v).map(|(a, b)| a + b).collect();
    Ok(quadratic_form(&g, &sum)? - quadratic_form(&g, &u)? - quadratic_form(&g, &v)?)
}

/// The pair sums `G_ij + G_ji` for `i < j`; all zero iff the readout is sector additive.
pub fn sector_additivity_defects(g: &Matrix) -> Result<Vec<((usize, usize), Q)>, Error> {
    let g = matrix(g)?;
    let n = g.len();
    let mut out = Vec::new();
    for i in 0..n {
        for j in i + 1..n {
            out.push(((i, j), &g[i][j] + &g[j][i]));
        }
    }
    Ok(out)
}

/// The theorem `offdiag_pair_sum_eq_zero` / `qf_eq_sum_diag_sq_of_sectorAdditive` replayed.
pub fn sector_additivity_certificate(g: &Matrix) -> Result<AdditivityVerdict, Error> {
    let g = matrix(g)?;
    let n = g.len();
    for ((i, j), s) in sector_additivity_defects(&g)? {
        if !s.is_zero() {
            let u = unit_vector(n, i, &q(1))?;
            let v = unit_vector(n, j, &q(1))?;
            let defect = sector_additivity_defect(&g, &u, &v)?;
            return Ok(AdditivityVerdict::NotSectorAdditive { i, j, u, v, defect });
        }
    }
    Ok(AdditivityVerdict::SectorAdditive {
        diagonal: (0..n).map(|i| g[i][i].clone()).collect(),
    })
}

/// `Σ G_ii x_i²`: equals `qf(G, x)` exactly when `G` is sector additive (symmetry not required).
pub fn diagonal_readout(g: &Matrix, x: &Vector) -> Result<Q, Error> {
    let g = matrix(g)?;
    let x = vector(x)?;
    same_length("diagonal_readout", g.len(), x.len())?;
    Ok((0..x.len()).fold(q(0), |acc, i| acc + &g[i][i] * &x[i] * &x[i]))
}

/// `G_{σj,σj} − G_jj` for every sector `j`.
pub fn invariance_defects(g: &Matrix, sigma: &[usize]) -> Result<Vec<(usize, Q)>, Error> {
    let g = matrix(g)?;
    let s = permutation(sigma, g.len())?;
    Ok((0..g.len())
        .map(|j| (j, &g[s[j]][s[j]] - &g[j][j]))
        .collect())
}

/// The lemma `diag_eq_of_invariant` replayed, with the unit vector witness.
pub fn invariance_certificate(g: &Matrix, sigma: &[usize]) -> Result<InvarianceVerdict, Error> {
    let g = matrix(g)?;
    let n = g.len();
    let s = permutation(sigma, n)?;
    for (j, d) in invariance_defects(&g, &s)? {
        if !d.is_zero() {
            let x = unit_vector(n, j, &q(1))?;
            let moved = quadratic_form(&g, &permute(&s, &x)?)?;
            let original = quadratic_form(&g, &x)?;
            return Ok(InvarianceVerdict::NotInvariant {
                j,
                x,
                moved,
                original,
            });
        }
    }
    Ok(InvarianceVerdict::Invariant)
}

/// The selection theorem `eq_smul_one` replayed on a supplied symmetric Gram matrix and
/// permutation set, or the first failing hypothesis with an exact witness.
pub fn derive_scale(g: &Matrix, perms: &[Permutation]) -> Result<SelectionVerdict, Error> {
    let g = matrix(g)?;
    let n = g.len();
    for i in 0..n {
        for j in 0..n {
            if g[i][j] != g[j][i] {
                return Ok(SelectionVerdict::NotSymmetric { i, j });
            }
        }
    }
    if let AdditivityVerdict::NotSectorAdditive { i, j, u, v, defect } =
        sector_additivity_certificate(&g)?
    {
        return Ok(SelectionVerdict::NotSectorAdditive { i, j, u, v, defect });
    }
    let ps: Vec<Permutation> = perms
        .iter()
        .map(|p| permutation(p, n))
        .collect::<Result<_, _>>()?;
    for p in &ps {
        if let InvarianceVerdict::NotInvariant {
            j,
            x,
            moved,
            original,
        } = invariance_certificate(&g, p)?
        {
            return Ok(SelectionVerdict::NotInvariant {
                sigma: p.clone(),
                j,
                x,
                moved,
                original,
            });
        }
    }
    if let TransitivityVerdict::NotTransitive { i, j, orbits } =
        transitivity_certificate(&closure(&ps, n)?, n)?
    {
        let orbit_values = orbits.iter().map(|o| g[o[0]][o[0]].clone()).collect();
        return Ok(SelectionVerdict::NotTransitive {
            i,
            j,
            orbits,
            orbit_values,
        });
    }
    let scale = g[0][0].clone();
    let expected: Matrix = (0..n)
        .map(|i| {
            (0..n)
                .map(|j| if i == j { scale.clone() } else { q(0) })
                .collect()
        })
        .collect();
    debug_assert_eq!(g, expected);
    Ok(SelectionVerdict::Scalar {
        scale,
        identity: identity(n),
    })
}

/// `scale_pos` replayed: the derived scale is positive iff the selected form is positive definite.
pub fn scale_is_positive(g: &Matrix, perms: &[Permutation]) -> Result<bool, Error> {
    match derive_scale(g, perms)? {
        SelectionVerdict::Scalar { scale, .. } => Ok(scale > q(0)),
        other => Err(Error::NotSelected(verdict_name(&other))),
    }
}

fn verdict_name(v: &SelectionVerdict) -> &'static str {
    match v {
        SelectionVerdict::Scalar { .. } => "scalar",
        SelectionVerdict::NotSymmetric { .. } => "not_symmetric",
        SelectionVerdict::NotSectorAdditive { .. } => "not_sector_additive",
        SelectionVerdict::NotInvariant { .. } => "not_invariant",
        SelectionVerdict::NotTransitive { .. } => "not_transitive",
    }
}

/// `unique_of_normalized` / `unique_up_to_scale` replayed on two selected forms.
pub fn uniqueness_certificate(
    g: &Matrix,
    g2: &Matrix,
    perms: &[Permutation],
    i0: usize,
) -> Result<UniquenessVerdict, Error> {
    for m in [g, g2] {
        if let other @ (SelectionVerdict::NotSymmetric { .. }
        | SelectionVerdict::NotSectorAdditive { .. }
        | SelectionVerdict::NotInvariant { .. }
        | SelectionVerdict::NotTransitive { .. }) = derive_scale(m, perms)?
        {
            return Err(Error::NotSelected(verdict_name(&other)));
        }
    }
    let g = matrix(g)?;
    let g2 = matrix(g2)?;
    same_length("uniqueness_certificate", g.len(), g2.len())?;
    index_in(i0, g.len())?;
    let c1 = &g[i0][i0];
    let c2 = &g2[i0][i0];
    if c1 == c2 {
        return Ok(UniquenessVerdict::Equal(g == g2));
    }
    if c1.is_zero() {
        return Err(Error::ZeroNormalisation);
    }
    let ratio = c2 / c1;
    let scaled: Matrix = g
        .iter()
        .map(|r| r.iter().map(|a| &ratio * a).collect())
        .collect();
    Ok(UniquenessVerdict::Proportional {
        ratio,
        holds: g2 == scaled,
    })
}

// ============================================================================
// Gaussian-rational (Hermitian) sector forms
// ============================================================================

fn gzero() -> GaussianRational {
    GaussianRational::from_integers(0, 0)
}

/// The imaginary unit `i`.
pub fn gi() -> GaussianRational {
    GaussianRational::from_integers(0, 1)
}

/// Admit a nonempty square Gaussian-rational matrix.
pub fn hmatrix(rows: &[Vec<GaussianRational>]) -> Result<HMatrix, Error> {
    let n = rows.len();
    if n == 0 || rows.iter().any(|r| r.len() != n) {
        return Err(Error::NonSquareMatrix);
    }
    for x in rows.iter().flatten() {
        x.validate()?;
    }
    Ok(rows.to_vec())
}

/// Admit a nonempty Gaussian-rational vector.
pub fn hvector(xs: &[GaussianRational]) -> Result<HVector, Error> {
    if xs.is_empty() {
        return Err(Error::EmptyVector);
    }
    for x in xs {
        x.validate()?;
    }
    Ok(xs.to_vec())
}

/// The Gaussian identity.
pub fn hidentity(n: usize) -> HMatrix {
    (0..n)
        .map(|i| {
            (0..n)
                .map(|j| GaussianRational::from_integers(if i == j { 1 } else { 0 }, 0))
                .collect()
        })
        .collect()
}

/// `c·e_i` over `ℚ(i)`.
pub fn hunit_vector(n: usize, i: usize, c: &GaussianRational) -> Result<HVector, Error> {
    index_in(i, n)?;
    c.validate()?;
    Ok((0..n).map(|k| if k == i { c.clone() } else { gzero() }).collect())
}

/// Disjoint sector supports over `ℚ(i)`.
pub fn hdisjoint_support(u: &HVector, v: &HVector) -> Result<bool, Error> {
    same_length("hdisjoint_support", u.len(), v.len())?;
    for (a, b) in u.iter().zip(v) {
        if !(a.try_is_zero()? || b.try_is_zero()?) {
            return Ok(false);
        }
    }
    Ok(true)
}

/// `(permute σ x)[i] = x[σ⁻¹(i)]` over `ℚ(i)`.
pub fn hpermute(sigma: &[usize], x: &HVector) -> Result<HVector, Error> {
    let s = permutation(sigma, x.len())?;
    let inv = inverse_permutation(&s)?;
    Ok((0..x.len()).map(|i| x[inv[i]].clone()).collect())
}

/// `x* y = Σ conj(x_k) y_k`.
pub fn hinner(x: &HVector, y: &HVector) -> Result<GaussianRational, Error> {
    same_length("hinner", x.len(), y.len())?;
    let mut acc = gzero();
    for (a, b) in x.iter().zip(y) {
        acc = acc.try_add(&a.try_conj()?.try_mul(b)?)?;
    }
    Ok(acc)
}

/// `H·x` over `ℚ(i)`.
pub fn hmat_vec(h: &HMatrix, x: &HVector) -> Result<HVector, Error> {
    let mut out = Vec::with_capacity(h.len());
    for row in h {
        same_length("hmat_vec", row.len(), x.len())?;
        let mut acc = gzero();
        for (a, b) in row.iter().zip(x) {
            acc = acc.try_add(&a.try_mul(b)?)?;
        }
        out.push(acc);
    }
    Ok(out)
}

/// The Hermitian readout `re(x* H x)`.
pub fn re_hermitian_form(h: &HMatrix, x: &HVector) -> Result<Q, Error> {
    Ok(hinner(x, &hmat_vec(h, x)?)?.real().clone())
}

/// `Hᴴ = H`.
pub fn is_hermitian(h: &HMatrix) -> Result<bool, Error> {
    let h = hmatrix(h)?;
    let n = h.len();
    for i in 0..n {
        for j in 0..n {
            if h[i][j] != h[j][i].try_conj()? {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

/// `re((u+v)* H (u+v)) − re(u* H u) − re(v* H v)` for disjointly supported Gaussian vectors.
pub fn hermitian_sector_additivity_defect(h: &HMatrix, u: &HVector, v: &HVector) -> Result<Q, Error> {
    let h = hmatrix(h)?;
    let u = hvector(u)?;
    let v = hvector(v)?;
    if !hdisjoint_support(&u, &v)? {
        return Err(Error::NotDisjoint);
    }
    let mut sum = Vec::with_capacity(u.len());
    for (a, b) in u.iter().zip(&v) {
        sum.push(a.try_add(b)?);
    }
    Ok(re_hermitian_form(&h, &sum)? - re_hermitian_form(&h, &u)? - re_hermitian_form(&h, &v)?)
}

/// For `i < j` the two defects read along the directions `1` and `i`:
/// `(re(H_ij + H_ji), im(H_ji − H_ij))`.
pub fn hermitian_sector_additivity_defects(h: &HMatrix) -> Result<Vec<((usize, usize), Q, Q)>, Error> {
    let h = hmatrix(h)?;
    let n = h.len();
    let mut out = Vec::new();
    for i in 0..n {
        for j in i + 1..n {
            let dre = h[i][j].try_add(&h[j][i])?.real().clone();
            let dim = h[j][i].try_sub(&h[i][j])?.imag().clone();
            out.push(((i, j), dre, dim));
        }
    }
    Ok(out)
}

/// `offdiag_re_add_re` / `offdiag_im_sub_im` replayed, with the direction that fails as witness.
pub fn hermitian_sector_additivity_certificate(h: &HMatrix) -> Result<HermitianAdditivityVerdict, Error> {
    let h = hmatrix(h)?;
    let n = h.len();
    for ((i, j), dre, dim) in hermitian_sector_additivity_defects(&h)? {
        let u = hunit_vector(n, i, &GaussianRational::from_integers(1, 0))?;
        if !dre.is_zero() {
            let v = hunit_vector(n, j, &GaussianRational::from_integers(1, 0))?;
            let defect = hermitian_sector_additivity_defect(&h, &u, &v)?;
            return Ok(HermitianAdditivityVerdict::NotSectorAdditive { i, j, u, v, defect });
        }
        if !dim.is_zero() {
            let v = hunit_vector(n, j, &gi())?;
            let defect = hermitian_sector_additivity_defect(&h, &u, &v)?;
            return Ok(HermitianAdditivityVerdict::NotSectorAdditive { i, j, u, v, defect });
        }
    }
    Ok(HermitianAdditivityVerdict::SectorAdditive {
        diagonal: (0..n).map(|i| h[i][i].real().clone()).collect(),
    })
}

/// `re H_{σj,σj} − re H_jj` for every sector `j`.
pub fn hermitian_invariance_defects(h: &HMatrix, sigma: &[usize]) -> Result<Vec<(usize, Q)>, Error> {
    let h = hmatrix(h)?;
    let s = permutation(sigma, h.len())?;
    Ok((0..h.len())
        .map(|j| (j, h[s[j]][s[j]].real() - h[j][j].real()))
        .collect())
}

/// The Hermitian selection theorem replayed: `H = scale·I` with real `scale = re H_00`, or the
/// first failing hypothesis with an exact witness.
pub fn hermitian_derive_scale(h: &HMatrix, perms: &[Permutation]) -> Result<HermitianSelectionVerdict, Error> {
    let h = hmatrix(h)?;
    let n = h.len();
    for i in 0..n {
        for j in 0..n {
            if h[i][j] != h[j][i].try_conj()? {
                return Ok(HermitianSelectionVerdict::NotHermitian { i, j });
            }
        }
    }
    if let HermitianAdditivityVerdict::NotSectorAdditive { i, j, u, v, defect } =
        hermitian_sector_additivity_certificate(&h)?
    {
        return Ok(HermitianSelectionVerdict::NotSectorAdditive { i, j, u, v, defect });
    }
    let ps: Vec<Permutation> = perms
        .iter()
        .map(|p| permutation(p, n))
        .collect::<Result<_, _>>()?;
    for p in &ps {
        for (j, d) in hermitian_invariance_defects(&h, p)? {
            if !d.is_zero() {
                let x = hunit_vector(n, j, &GaussianRational::from_integers(1, 0))?;
                let moved = re_hermitian_form(&h, &hpermute(p, &x)?)?;
                let original = re_hermitian_form(&h, &x)?;
                return Ok(HermitianSelectionVerdict::NotInvariant {
                    sigma: p.clone(),
                    j,
                    x,
                    moved,
                    original,
                });
            }
        }
    }
    if let TransitivityVerdict::NotTransitive { i, j, orbits } =
        transitivity_certificate(&closure(&ps, n)?, n)?
    {
        let orbit_values = orbits.iter().map(|o| h[o[0]][o[0]].real().clone()).collect();
        return Ok(HermitianSelectionVerdict::NotTransitive {
            i,
            j,
            orbits,
            orbit_values,
        });
    }
    let scale = h[0][0].real().clone();
    debug_assert!(h[0][0].imag().is_zero());
    Ok(HermitianSelectionVerdict::Scalar {
        scale,
        identity: hidentity(n),
    })
}

// ============================================================================
// Countermodels (each hypothesis is used)
// ============================================================================

/// `diag(1, 2)`: symmetric, positive definite, sector additive, not invariant under the swap.
pub fn diag12() -> Matrix {
    vec![vec![q(1), q(0)], vec![q(0), q(2)]]
}

/// `1 + (all ones)`: symmetric, positive definite, invariant under every permutation of two
/// sectors, not sector additive.
pub fn unif12() -> Matrix {
    vec![vec![q(2), q(1)], vec![q(1), q(2)]]
}

/// `[[1, i], [−i, 1]]`: Hermitian, additive along the real direction on `(e₀, e₁)`, not sector
/// additive (the direction `i·e₁` fails).
pub fn imag_leak12() -> HMatrix {
    vec![
        vec![GaussianRational::from_integers(1, 0), gi()],
        vec![GaussianRational::from_integers(0, -1), GaussianRational::from_integers(1, 0)],
    ]
}

/// The nontrivial permutation of two sectors, as a one-element set.
pub fn s2() -> Vec<Permutation> {
    vec![vec![1, 0]]
}

#[cfg(test)]
mod tests {
    use super::*;

    fn fr(a: i64, b: i64) -> Q {
        Q::new(num_bigint::BigInt::from(a), num_bigint::BigInt::from(b))
    }

    fn gq(re: i64, im: i64) -> GaussianRational {
        GaussianRational::from_integers(re, im)
    }

    /// Deterministic linear congruential source for small fixture integers.
    struct Lcg(u64);
    impl Lcg {
        fn next(&mut self) -> u64 {
            self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            self.0 >> 33
        }
        fn int(&mut self, lo: i64, hi: i64) -> i64 {
            lo + (self.next() % ((hi - lo + 1) as u64)) as i64
        }
        fn rat(&mut self) -> Q {
            fr(self.int(-4, 4), self.int(1, 3))
        }
    }

    fn rand_sym(r: &mut Lcg, n: usize) -> Matrix {
        let a: Matrix = (0..n)
            .map(|_| (0..n).map(|_| fr(r.int(-3, 3), r.int(1, 2))).collect())
            .collect();
        (0..n)
            .map(|i| (0..n).map(|j| &a[i][j] + &a[j][i]).collect())
            .collect()
    }

    fn split_support(r: &mut Lcg, x: &Vector) -> (Vector, Vector) {
        let mut u = vec![q(0); x.len()];
        let mut v = vec![q(0); x.len()];
        for (i, a) in x.iter().enumerate() {
            if r.int(0, 1) == 0 {
                u[i] = a.clone();
            } else {
                v[i] = a.clone();
            }
        }
        (u, v)
    }

    fn uv(n: usize, i: usize) -> Vector {
        unit_vector(n, i, &q(1)).unwrap()
    }

    #[test]
    fn permute_moves_unit_vectors_forward() {
        for n in 2..=4 {
            for s in all_permutations(n) {
                for j in 0..n {
                    assert_eq!(permute(&s, &uv(n, j)).unwrap(), uv(n, s[j]));
                }
            }
        }
        assert_eq!(all_permutations(4).len(), 24);
    }

    #[test]
    fn inverse_and_admission() {
        assert_eq!(inverse_permutation(&[1, 2, 0]).unwrap(), vec![2, 0, 1]);
        assert_eq!(swap(3, 0, 2).unwrap(), vec![2, 1, 0]);
        for bad in [vec![0usize, 0], vec![1, 2], vec![0, 1, 1]] {
            assert!(matches!(permutation(&bad, bad.len()), Err(Error::NotAPermutation(_))));
        }
        assert!(matches!(permutation(&[0, 1], 3), Err(Error::NotAPermutation(3))));
        assert!(matches!(swap(2, 0, 2), Err(Error::IndexOutOfRange { index: 2, dimension: 2 })));
    }

    #[test]
    fn orbits_and_transitivity() {
        assert_eq!(orbits(&[vec![1, 0, 2]], 3).unwrap(), vec![vec![0, 1], vec![2]]);
        assert_eq!(orbits(&[vec![1, 2, 0]], 3).unwrap(), vec![vec![0, 1, 2]]);
        assert_eq!(
            transitivity_certificate(&[vec![1, 2, 0]], 3).unwrap(),
            TransitivityVerdict::NotTransitive { i: 0, j: 2, orbits: vec![vec![0, 1, 2]] }
        );
        assert_eq!(
            transitivity_certificate(&closure(&[vec![1, 2, 0]], 3).unwrap(), 3).unwrap(),
            TransitivityVerdict::Transitive
        );
        assert_eq!(
            transitivity_certificate(&[vec![0, 1, 2], vec![1, 0, 2]], 3).unwrap(),
            TransitivityVerdict::NotTransitive { i: 0, j: 2, orbits: vec![vec![0, 1], vec![2]] }
        );
        assert_eq!(transitivity_certificate(&[vec![1, 0]], 2).unwrap(), TransitivityVerdict::Transitive);
        assert_eq!(
            transitivity_certificate(&[vec![0, 1]], 2).unwrap(),
            TransitivityVerdict::NotTransitive { i: 0, j: 1, orbits: vec![vec![0], vec![1]] }
        );
    }

    #[test]
    fn closure_is_the_generated_group() {
        assert_eq!(closure(&[vec![1, 2, 0]], 3).unwrap(), vec![vec![0, 1, 2], vec![1, 2, 0], vec![2, 0, 1]]);
        assert_eq!(closure(&[], 3).unwrap(), vec![vec![0, 1, 2]]);
        assert_eq!(closure(&[vec![1, 0, 2, 3], vec![1, 2, 3, 0]], 4).unwrap().len(), 24);
        assert_eq!(closure(&[vec![1, 0, 2]], 3).unwrap(), vec![vec![0, 1, 2], vec![1, 0, 2]]);
        for s in closure(&[vec![1, 2, 3, 0]], 4).unwrap() {
            assert_eq!(invariance_certificate(&identity(4), &s).unwrap(), InvarianceVerdict::Invariant);
        }
    }

    #[test]
    fn defect_equals_pair_sum_on_unit_vectors() {
        let mut r = Lcg(1);
        for n in 2..=4 {
            for _ in 0..5 {
                let a: Matrix = (0..n).map(|_| (0..n).map(|_| q(r.int(-3, 3))).collect()).collect();
                for ((i, j), s) in sector_additivity_defects(&a).unwrap() {
                    assert_eq!(sector_additivity_defect(&a, &uv(n, i), &uv(n, j)).unwrap(), s);
                }
            }
        }
    }

    #[test]
    fn sector_additive_iff_pair_sums_vanish_on_random_splits() {
        let mut r = Lcg(2);
        for n in 2..=4 {
            for _ in 0..20 {
                let a: Matrix = (0..n).map(|_| (0..n).map(|_| q(r.int(-3, 3))).collect()).collect();
                let x: Vector = (0..n).map(|_| r.rat()).collect();
                let (u, v) = split_support(&mut r, &x);
                match sector_additivity_certificate(&a).unwrap() {
                    AdditivityVerdict::SectorAdditive { .. } => {
                        assert!(sector_additivity_defect(&a, &u, &v).unwrap().is_zero());
                        assert_eq!(quadratic_form(&a, &x).unwrap(), diagonal_readout(&a, &x).unwrap());
                    }
                    AdditivityVerdict::NotSectorAdditive { i, j, defect, .. } => {
                        assert!(!defect.is_zero());
                        assert_eq!(defect, &a[i][j] + &a[j][i]);
                    }
                }
            }
        }
    }

    #[test]
    fn readout_of_sector_additive_form_is_diagonal_without_symmetry() {
        let a = vec![vec![q(3), q(5)], vec![q(-5), q(-1)]];
        assert_eq!(
            sector_additivity_certificate(&a).unwrap(),
            AdditivityVerdict::SectorAdditive { diagonal: vec![q(3), q(-1)] }
        );
        assert!(!is_symmetric(&a).unwrap());
        for x in [vec![q(1), q(1)], vec![q(2), q(-3)], vec![fr(1, 2), fr(1, 3)]] {
            assert_eq!(quadratic_form(&a, &x).unwrap(), diagonal_readout(&a, &x).unwrap());
        }
    }

    #[test]
    fn disjoint_support_required_and_shapes_checked() {
        assert!(matches!(
            sector_additivity_defect(&identity(2), &vec![q(1), q(1)], &vec![q(0), q(1)]),
            Err(Error::NotDisjoint)
        ));
        assert!(matches!(
            diagonal_readout(&identity(2), &vec![q(1), q(2), q(3)]),
            Err(Error::DimensionMismatch { .. })
        ));
        assert!(matches!(matrix(&[vec![q(1), q(2)]]), Err(Error::NonSquareMatrix)));
        assert!(matches!(vector(&[]), Err(Error::EmptyVector)));
        assert!(matches!(unit_vector(2, 2, &q(1)), Err(Error::IndexOutOfRange { .. })));
    }

    #[test]
    fn invariance_defects_are_diagonal_differences() {
        let a = vec![
            vec![q(1), q(0), q(0)],
            vec![q(0), q(2), q(0)],
            vec![q(0), q(0), q(1)],
        ];
        assert_eq!(invariance_defects(&a, &[2, 1, 0]).unwrap(), vec![(0, q(0)), (1, q(0)), (2, q(0))]);
        assert_eq!(invariance_certificate(&a, &[2, 1, 0]).unwrap(), InvarianceVerdict::Invariant);
        assert_eq!(
            invariance_certificate(&a, &[1, 0, 2]).unwrap(),
            InvarianceVerdict::NotInvariant { j: 0, x: uv(3, 0), moved: q(2), original: q(1) }
        );
    }

    #[test]
    fn identity_form_invariant_under_every_permutation() {
        let mut r = Lcg(3);
        for n in 2..=4 {
            for s in all_permutations(n) {
                assert_eq!(invariance_certificate(&identity(n), &s).unwrap(), InvarianceVerdict::Invariant);
                let x: Vector = (0..n).map(|_| r.rat()).collect();
                assert_eq!(
                    quadratic_form(&identity(n), &permute(&s, &x).unwrap()).unwrap(),
                    quadratic_form(&identity(n), &x).unwrap()
                );
            }
        }
    }

    #[test]
    fn identity_is_selected_and_normalised() {
        for n in 1..=4 {
            assert_eq!(
                derive_scale(&identity(n), &all_permutations(n)).unwrap(),
                SelectionVerdict::Scalar { scale: q(1), identity: identity(n) }
            );
            assert!(scale_is_positive(&identity(n), &all_permutations(n)).unwrap());
        }
    }

    #[test]
    fn scalar_multiples_and_scale_sign() {
        for c in [q(3), fr(1, 2), q(-2)] {
            let a: Matrix = (0..3)
                .map(|i| (0..3).map(|j| if i == j { c.clone() } else { q(0) }).collect())
                .collect();
            let cycle = vec![vec![1, 2, 0]];
            assert_eq!(
                derive_scale(&a, &cycle).unwrap(),
                SelectionVerdict::Scalar { scale: c.clone(), identity: identity(3) }
            );
            assert_eq!(scale_is_positive(&a, &cycle).unwrap(), c > q(0));
        }
    }

    #[test]
    fn random_symmetric_forms_reduce_to_the_theorem() {
        let mut r = Lcg(4);
        for n in 2..=3 {
            for _ in 0..30 {
                let a = rand_sym(&mut r, n);
                match derive_scale(&a, &all_permutations(n)).unwrap() {
                    SelectionVerdict::Scalar { scale, .. } => {
                        let expected: Matrix = (0..n)
                            .map(|i| (0..n).map(|j| if i == j { scale.clone() } else { q(0) }).collect())
                            .collect();
                        assert_eq!(a, expected);
                    }
                    SelectionVerdict::NotSectorAdditive { i, j, defect, .. } => {
                        assert_eq!(defect, q(2) * &a[i][j]);
                        assert!(!defect.is_zero());
                    }
                    SelectionVerdict::NotInvariant { .. } => {}
                    other => panic!("unexpected verdict {other:?}"),
                }
            }
        }
    }

    #[test]
    fn transitivity_needed_orbit_values() {
        let a = vec![
            vec![q(1), q(0), q(0)],
            vec![q(0), q(1), q(0)],
            vec![q(0), q(0), q(5)],
        ];
        assert_eq!(
            derive_scale(&a, &[vec![1, 0, 2]]).unwrap(),
            SelectionVerdict::NotTransitive {
                i: 0,
                j: 2,
                orbits: vec![vec![0, 1], vec![2]],
                orbit_values: vec![q(1), q(5)],
            }
        );
        assert!(matches!(
            derive_scale(&a, &[vec![1, 0, 2], vec![0, 2, 1]]).unwrap(),
            SelectionVerdict::NotInvariant { .. }
        ));
    }

    #[test]
    fn non_symmetric_refused_with_witness() {
        assert_eq!(
            derive_scale(&vec![vec![q(1), q(1)], vec![q(0), q(1)]], &s2()).unwrap(),
            SelectionVerdict::NotSymmetric { i: 0, j: 1 }
        );
    }

    #[test]
    fn uniqueness() {
        let a = vec![vec![q(2), q(0)], vec![q(0), q(2)]];
        let b = vec![vec![q(3), q(0)], vec![q(0), q(3)]];
        assert_eq!(uniqueness_certificate(&a, &a, &s2(), 0).unwrap(), UniquenessVerdict::Equal(true));
        assert_eq!(
            uniqueness_certificate(&a, &b, &s2(), 0).unwrap(),
            UniquenessVerdict::Proportional { ratio: fr(3, 2), holds: true }
        );
        assert!(matches!(
            uniqueness_certificate(&diag12(), &a, &s2(), 0),
            Err(Error::NotSelected("not_invariant"))
        ));
    }

    #[test]
    fn diag12_is_sector_additive_positive_but_not_invariant() {
        let d = diag12();
        assert!(is_symmetric(&d).unwrap());
        assert_eq!(
            sector_additivity_certificate(&d).unwrap(),
            AdditivityVerdict::SectorAdditive { diagonal: vec![q(1), q(2)] }
        );
        assert_eq!(
            derive_scale(&d, &s2()).unwrap(),
            SelectionVerdict::NotInvariant {
                sigma: vec![1, 0],
                j: 0,
                x: uv(2, 0),
                moved: q(2),
                original: q(1),
            }
        );
        for x in [vec![q(1), q(0)], vec![q(0), q(1)], vec![q(1), q(-1)], vec![fr(1, 2), fr(1, 3)]] {
            assert!(quadratic_form(&d, &x).unwrap() > q(0));
        }
        assert_eq!(
            derive_scale(&d, &[vec![0, 1]]).unwrap(),
            SelectionVerdict::NotTransitive {
                i: 0,
                j: 1,
                orbits: vec![vec![0], vec![1]],
                orbit_values: vec![q(1), q(2)],
            }
        );
    }

    #[test]
    fn unif12_is_invariant_positive_but_not_sector_additive() {
        let u = unif12();
        assert!(is_symmetric(&u).unwrap());
        let mut both = s2();
        both.push(vec![0, 1]);
        for s in &both {
            assert_eq!(invariance_certificate(&u, s).unwrap(), InvarianceVerdict::Invariant);
        }
        assert_eq!(
            derive_scale(&u, &both).unwrap(),
            SelectionVerdict::NotSectorAdditive { i: 0, j: 1, u: uv(2, 0), v: uv(2, 1), defect: q(2) }
        );
        for x in [vec![q(1), q(0)], vec![q(0), q(1)], vec![q(1), q(-1)], vec![fr(1, 2), fr(-1, 3)]] {
            assert!(quadratic_form(&u, &x).unwrap() > q(0));
        }
        assert_eq!(quadratic_form(&u, &vec![q(1), q(1)]).unwrap(), q(6));
        assert_eq!(
            quadratic_form(&u, &uv(2, 0)).unwrap() + quadratic_form(&u, &uv(2, 1)).unwrap(),
            q(4)
        );
    }

    #[test]
    fn identity_selected_over_gaussian_rationals() {
        for n in 1..=3 {
            assert_eq!(
                hermitian_derive_scale(&hidentity(n), &all_permutations(n)).unwrap(),
                HermitianSelectionVerdict::Scalar { scale: q(1), identity: hidentity(n) }
            );
        }
    }

    #[test]
    fn both_directions_are_needed() {
        let l = imag_leak12();
        assert!(is_hermitian(&l).unwrap());
        assert_eq!(hermitian_sector_additivity_defects(&l).unwrap(), vec![((0, 1), q(0), q(-2))]);
        let e0 = hunit_vector(2, 0, &gq(1, 0)).unwrap();
        let e1 = hunit_vector(2, 1, &gq(1, 0)).unwrap();
        let ie1 = hunit_vector(2, 1, &gi()).unwrap();
        assert!(hermitian_sector_additivity_defect(&l, &e0, &e1).unwrap().is_zero());
        assert_eq!(hermitian_sector_additivity_defect(&l, &e0, &ie1).unwrap(), q(-2));
        let mut both = s2();
        both.push(vec![0, 1]);
        assert_eq!(
            hermitian_derive_scale(&l, &both).unwrap(),
            HermitianSelectionVerdict::NotSectorAdditive { i: 0, j: 1, u: e0, v: ie1, defect: q(-2) }
        );
    }

    #[test]
    fn hermitian_defects_match_the_two_directions_randomly() {
        let mut r = Lcg(5);
        for _ in 0..20 {
            let n = if r.int(0, 1) == 0 { 2 } else { 3 };
            let h: HMatrix = (0..n)
                .map(|_| (0..n).map(|_| gq(r.int(-2, 2), r.int(-2, 2))).collect())
                .collect();
            for ((i, j), dre, dim) in hermitian_sector_additivity_defects(&h).unwrap() {
                let u = hunit_vector(n, i, &gq(1, 0)).unwrap();
                assert_eq!(
                    hermitian_sector_additivity_defect(&h, &u, &hunit_vector(n, j, &gq(1, 0)).unwrap()).unwrap(),
                    dre
                );
                assert_eq!(
                    hermitian_sector_additivity_defect(&h, &u, &hunit_vector(n, j, &gi()).unwrap()).unwrap(),
                    dim
                );
            }
        }
    }

    #[test]
    fn hermitian_witnesses() {
        let h = vec![vec![gq(1, 0), gq(0, 0)], vec![gq(0, 0), gq(2, 0)]];
        assert_eq!(
            hermitian_derive_scale(&h, &s2()).unwrap(),
            HermitianSelectionVerdict::NotInvariant {
                sigma: vec![1, 0],
                j: 0,
                x: hunit_vector(2, 0, &gq(1, 0)).unwrap(),
                moved: q(2),
                original: q(1),
            }
        );
        assert_eq!(
            hermitian_derive_scale(&vec![vec![gq(1, 0), gi()], vec![gi(), gq(1, 0)]], &s2()).unwrap(),
            HermitianSelectionVerdict::NotHermitian { i: 0, j: 1 }
        );
        assert_eq!(
            hermitian_derive_scale(&h, &[vec![0, 1]]).unwrap(),
            HermitianSelectionVerdict::NotTransitive {
                i: 0,
                j: 1,
                orbits: vec![vec![0], vec![1]],
                orbit_values: vec![q(1), q(2)],
            }
        );
        assert!(matches!(
            hermitian_sector_additivity_defect(&h, &vec![gq(1, 0), gq(1, 0)], &vec![gq(0, 0), gq(1, 0)]),
            Err(Error::NotDisjoint)
        ));
    }
}
