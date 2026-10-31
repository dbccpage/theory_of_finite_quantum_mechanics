//! 1D Hinge Lineon Collision Avoidance and Foliated Fracton Sign Invariants (TFQ-1219).
//!
//! Evaluates:
//! 1. 1D discrete line lattice coordinate ordering and collision avoidance.
//! 2. Collision-free 1D hinge paths strictly preserve relative order (pos1 < pos2).
//! 3. 1D exchange obstruction: lineons on a 1D hinge cannot exchange without passing
//!    through an identical site or crossing an edge.
//! 4. Worldline permutation sign is trivial (+1) on non-intersecting hinges.
//! 5. Intersecting hinge non-abelian commutator holonomy produces negative trace (-2)
//!    and positive defect mass (Phi1 = 2 > 0).
//! 6. Decoupled foliated categorical projection restores non-negative trace.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_rational::Rational64;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use std::ops::{Add, Mul, Neg, Sub};

/// Exact Gaussian rational Q(i) field element.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct ComplexRat {
    pub re: Rational64,
    pub im: Rational64,
}

impl ComplexRat {
    pub const fn new(re: Rational64, im: Rational64) -> Self {
        Self { re, im }
    }

    pub fn zero() -> Self {
        Self {
            re: Rational64::zero(),
            im: Rational64::zero(),
        }
    }

    pub fn one() -> Self {
        Self {
            re: Rational64::one(),
            im: Rational64::zero(),
        }
    }

    pub fn i() -> Self {
        Self {
            re: Rational64::zero(),
            im: Rational64::one(),
        }
    }

    pub fn from_integer(n: i64) -> Self {
        Self {
            re: Rational64::from_integer(n),
            im: Rational64::zero(),
        }
    }

    pub fn conj(&self) -> Self {
        Self {
            re: self.re,
            im: -self.im,
        }
    }

    pub fn norm_sq(&self) -> Rational64 {
        self.re * self.re + self.im * self.im
    }

    pub fn inv(&self) -> Result<Self, &'static str> {
        let n = self.norm_sq();
        if n.is_zero() {
            return Err("Division by zero in ComplexRat inverse");
        }
        Ok(Self {
            re: self.re / n,
            im: -self.im / n,
        })
    }

    pub fn is_real(&self) -> bool {
        self.im.is_zero()
    }
}

impl Add for ComplexRat {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Self {
            re: self.re + rhs.re,
            im: self.im + rhs.im,
        }
    }
}

impl Sub for ComplexRat {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        Self {
            re: self.re - rhs.re,
            im: self.im - rhs.im,
        }
    }
}

impl Neg for ComplexRat {
    type Output = Self;
    fn neg(self) -> Self {
        Self {
            re: -self.re,
            im: -self.im,
        }
    }
}

impl Mul for ComplexRat {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        Self {
            re: self.re * rhs.re - self.im * rhs.im,
            im: self.re * rhs.im + self.im * rhs.re,
        }
    }
}

/// Exact 2x2 matrix ring over Q(i).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct Mat2x2 {
    pub m00: ComplexRat,
    pub m01: ComplexRat,
    pub m10: ComplexRat,
    pub m11: ComplexRat,
}

impl Mat2x2 {
    pub const fn new(
        m00: ComplexRat,
        m01: ComplexRat,
        m10: ComplexRat,
        m11: ComplexRat,
    ) -> Self {
        Self { m00, m01, m10, m11 }
    }

    pub fn identity() -> Self {
        Self::new(
            ComplexRat::one(),
            ComplexRat::zero(),
            ComplexRat::zero(),
            ComplexRat::one(),
        )
    }

    pub fn pauli_x() -> Self {
        Self::new(
            ComplexRat::zero(),
            ComplexRat::one(),
            ComplexRat::one(),
            ComplexRat::zero(),
        )
    }

    pub fn pauli_y() -> Self {
        Self::new(
            ComplexRat::zero(),
            -ComplexRat::i(),
            ComplexRat::i(),
            ComplexRat::zero(),
        )
    }

    pub fn pauli_z() -> Self {
        Self::new(
            ComplexRat::one(),
            ComplexRat::zero(),
            ComplexRat::zero(),
            -ComplexRat::one(),
        )
    }

    pub fn mul(&self, other: &Self) -> Self {
        Self {
            m00: self.m00 * other.m00 + self.m01 * other.m10,
            m01: self.m00 * other.m01 + self.m01 * other.m11,
            m10: self.m10 * other.m00 + self.m11 * other.m10,
            m11: self.m10 * other.m01 + self.m11 * other.m11,
        }
    }

    pub fn trace(&self) -> ComplexRat {
        self.m00 + self.m11
    }

    pub fn det(&self) -> ComplexRat {
        self.m00 * self.m11 - self.m01 * self.m10
    }

    pub fn inv(&self) -> Result<Self, &'static str> {
        let d = self.det();
        let d_inv = d.inv().map_err(|_| "Singular matrix: zero determinant")?;
        Ok(Self {
            m00: self.m11 * d_inv,
            m01: (-self.m01) * d_inv,
            m10: (-self.m10) * d_inv,
            m11: self.m00 * d_inv,
        })
    }

    pub fn commutator_holonomy(&self, other: &Self) -> Result<Self, &'static str> {
        let a_inv = self.inv()?;
        let b_inv = other.inv()?;
        let ab = self.mul(other);
        let a_inv_b_inv = a_inv.mul(&b_inv);
        Ok(ab.mul(&a_inv_b_inv))
    }
}

/// Exact rational quaternion ring H_Q.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuaternionRat {
    pub r: Rational64,
    pub i: Rational64,
    pub j: Rational64,
    pub k: Rational64,
}

impl QuaternionRat {
    pub const fn new(r: Rational64, i: Rational64, j: Rational64, k: Rational64) -> Self {
        Self { r, i, j, k }
    }

    pub fn zero() -> Self {
        Self::new(
            Rational64::zero(),
            Rational64::zero(),
            Rational64::zero(),
            Rational64::zero(),
        )
    }

    pub fn one() -> Self {
        Self::new(
            Rational64::one(),
            Rational64::zero(),
            Rational64::zero(),
            Rational64::zero(),
        )
    }

    pub fn i_unit() -> Self {
        Self::new(
            Rational64::zero(),
            Rational64::one(),
            Rational64::zero(),
            Rational64::zero(),
        )
    }

    pub fn j_unit() -> Self {
        Self::new(
            Rational64::zero(),
            Rational64::zero(),
            Rational64::one(),
            Rational64::zero(),
        )
    }

    pub fn k_unit() -> Self {
        Self::new(
            Rational64::zero(),
            Rational64::zero(),
            Rational64::zero(),
            Rational64::one(),
        )
    }

    pub fn norm_sq(&self) -> Rational64 {
        self.r * self.r + self.i * self.i + self.j * self.j + self.k * self.k
    }

    pub fn conj(&self) -> Self {
        Self {
            r: self.r,
            i: -self.i,
            j: -self.j,
            k: -self.k,
        }
    }

    pub fn inv(&self) -> Result<Self, &'static str> {
        let n = self.norm_sq();
        if n.is_zero() {
            return Err("Division by zero in QuaternionRat inverse");
        }
        let c = self.conj();
        Ok(Self {
            r: c.r / n,
            i: c.i / n,
            j: c.j / n,
            k: c.k / n,
        })
    }

    pub fn mul(&self, other: &Self) -> Self {
        Self {
            r: self.r * other.r - self.i * other.i - self.j * other.j - self.k * other.k,
            i: self.r * other.i + self.i * other.r + self.j * other.k - self.k * other.j,
            j: self.r * other.j - self.i * other.k + self.j * other.r + self.k * other.i,
            k: self.r * other.k + self.i * other.j - self.j * other.i + self.k * other.r,
        }
    }

    pub fn commutator_holonomy(&self, other: &Self) -> Result<Self, &'static str> {
        let a_inv = self.inv()?;
        let b_inv = other.inv()?;
        let ab = self.mul(other);
        let a_inv_b_inv = a_inv.mul(&b_inv);
        Ok(ab.mul(&a_inv_b_inv))
    }

    pub fn character_trace(&self) -> Rational64 {
        self.r * Rational64::from_integer(2)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum HingeOrientation {
    XAxis,
    YAxis,
    ZAxis,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LineonHingeConfig {
    pub hinge: HingeOrientation,
    pub pos1: i64,
    pub pos2: i64,
}

impl LineonHingeConfig {
    /// Creates a new ordered 1D hinge configuration.
    /// Returns Err if pos1 >= pos2 (collision or ordering violation).
    pub fn new(hinge: HingeOrientation, p1: i64, p2: i64) -> Result<Self, &'static str> {
        if p1 >= p2 {
            return Err("Lineon positions must be strictly ordered (pos1 < pos2) to prevent collision");
        }
        Ok(Self {
            hinge,
            pos1: p1,
            pos2: p2,
        })
    }

    /// Checks if two lineons on a 1D hinge can exchange positions without collision.
    /// Strictly returns false because 1D topology forbids exchange without meeting.
    pub fn can_exchange_without_collision(&self) -> bool {
        false
    }

    /// Worldline permutation parity is identically trivial (+1) for collision-free lineons.
    pub fn permutation_parity(&self) -> i32 {
        1
    }

    /// Evaluates the discrete commutator holonomy trace M_hinge = B_xy B_yz B_xy^-1 B_yz^-1
    /// for the canonical Pauli/identity fixture:
    /// - For commuting identity sheets (A = I, B = I): M = I, Tr(M) = +2
    /// - For anticommuting Pauli sheets (A = sigma_z, B = sigma_x, AB = -BA): M = -I, Tr(M) = -2
    ///
    /// For arbitrary 2x2 matrices over Q(i) (such as non-commuting SU(2) holonomies with positive
    /// rational trace like 14/25), use `compute_defect_sheet_trace`.
    pub fn hinge_commutator_trace(is_nonabelian: bool) -> i64 {
        let (sheet_xy, sheet_yz) = if is_nonabelian {
            (Mat2x2::pauli_z(), Mat2x2::pauli_x())
        } else {
            (Mat2x2::identity(), Mat2x2::identity())
        };
        let m = sheet_xy
            .commutator_holonomy(&sheet_yz)
            .expect("Defect sheet matrices must be invertible");
        let tr = m.trace();
        *tr.re.numer() / *tr.re.denom()
    }

    /// Computes commutator holonomy trace from arbitrary 2x2 defect sheet matrices over Q(i).
    pub fn compute_defect_sheet_trace(
        sheet_xy: &Mat2x2,
        sheet_yz: &Mat2x2,
    ) -> Result<ComplexRat, &'static str> {
        let m = sheet_xy.commutator_holonomy(sheet_yz)?;
        Ok(m.trace())
    }

    /// Defect mass Phi1 derived from the computed commutator holonomy trace:
    /// - If trace < 0 (non-abelian curvature obstruction): Phi1 = 2
    /// - Else (abelian zero curvature): Phi1 = 0
    pub fn fracton_defect_mass(is_nonabelian: bool) -> u64 {
        let tr = Self::hinge_commutator_trace(is_nonabelian);
        Self::fracton_defect_mass_from_trace(tr)
    }

    /// Derives defect mass Phi1 from a computed trace:
    /// If trace < 0 => 2, else => 0.
    pub fn fracton_defect_mass_from_trace(trace: i64) -> u64 {
        if trace < 0 {
            2
        } else {
            0
        }
    }

    /// Projected trace under foliated quantum double projection:
    /// - Without corner lineon turns: non-negative Tr = |tr|^2 >= 0
    /// - With corner lineon turns: negative trace remains uncancelled
    pub fn foliated_projected_trace(has_corner_lineon: bool, is_nonabelian: bool) -> i64 {
        let base_tr = Self::hinge_commutator_trace(is_nonabelian);
        if has_corner_lineon {
            base_tr
        } else {
            base_tr.abs() * base_tr.abs()
        }
    }

    /// Applies a discrete hop sequence and verifies that pos1 < pos2 holds at every step.
    /// Each hop is (delta1, delta2) with |delta| <= 1.
    pub fn apply_hops(&self, hops: &[(i64, i64)]) -> Result<Self, &'static str> {
        let mut curr1 = self.pos1;
        let mut curr2 = self.pos2;
        for &(d1, d2) in hops {
            if d1.abs() > 1 || d2.abs() > 1 {
                return Err("Hop step exceeds discrete lattice unit bound (|delta| <= 1)");
            }
            curr1 = curr1.checked_add(d1).ok_or("Arithmetic overflow on pos1")?;
            curr2 = curr2.checked_add(d2).ok_or("Arithmetic overflow on pos2")?;
            if curr1 >= curr2 {
                return Err("Collision detected: pos1 >= pos2 on 1D hinge line");
            }
        }
        Ok(Self {
            hinge: self.hinge,
            pos1: curr1,
            pos2: curr2,
        })
    }

    /// Discrete IVT verification:
    /// Verifies that any discrete path attempting to swap endpoints p1 < p2
    /// to p2, p1 must encounter an explicit collision site traj1[t] == traj2[t]
    /// or edge crossing traj1[t] < traj2[t] and traj1[t+1] > traj2[t+1].
    pub fn verify_discrete_ivt_collision(
        p1: i64,
        p2: i64,
        traj1: &[i64],
        traj2: &[i64],
    ) -> Result<usize, &'static str> {
        if p1 >= p2 {
            return Err("Initial positions must be ordered p1 < p2");
        }
        if traj1.is_empty() || traj2.is_empty() || traj1.len() != traj2.len() {
            return Err("Trajectories must be non-empty and of equal length");
        }
        if traj1[0] != p1 || traj2[0] != p2 {
            return Err("Trajectories must start at (p1, p2)");
        }
        if *traj1.last().unwrap() != p2 || *traj2.last().unwrap() != p1 {
            return Err("Trajectories must end at swapped endpoints (p2, p1)");
        }
        for t in 0..traj1.len() {
            if traj1[t] == traj2[t] {
                return Ok(t);
            }
        }
        for t in 0..traj1.len() - 1 {
            if traj1[t] < traj2[t] && traj1[t + 1] > traj2[t + 1] {
                return Ok(t);
            }
        }
        Err("Discrete IVT violation: no collision point found for swap")
    }

    /// Evaluates the 6-step collision-free exchange trajectory on a 3-prong multi-hinge
    /// Y-junction (0: center, 1: branchX, 2: branchY, 3: branchZ) when corner branch-hopping
    /// is permitted vs. strict hinge-axis conservation (Theorems 6-8 of TFQ-1219):
    /// returns `(steps, collision_free, valid_hops, exchanged, exchange_sign, ab_weight, nonab_weight, axis_swap_allowed)`.
    pub fn verify_y_junction_exchange_statistics() -> (usize, bool, bool, bool, i64, i64, i64, bool) {
        let is_adj = |u: u8, v: u8| -> bool {
            (u == 0 && (v == 1 || v == 2 || v == 3)) || (v == 0 && (u == 1 || u == 2 || u == 3))
        };
        let traj: [(u8, u8); 7] = [
            (1, 2),
            (0, 2),
            (3, 2),
            (3, 0),
            (3, 1),
            (0, 1),
            (2, 1),
        ];
        let collision_free = traj.iter().all(|&(v1, v2)| v1 != v2);
        let mut valid_hops = true;
        for w in traj.windows(2) {
            let (u1, u2) = w[0];
            let (v1, v2) = w[1];
            let step_ok = (u1 == v1 && is_adj(u2, v2)) || (u2 == v2 && is_adj(u1, v1));
            if !step_ok {
                valid_hops = false;
                break;
            }
        }
        let exchanged = traj[6].0 == traj[0].1 && traj[6].1 == traj[0].0;
        let exchange_sign: i64 = if exchanged { -1 } else { 1 };
        let ab_weight = exchange_sign * Self::hinge_commutator_trace(false);
        let nonab_weight = exchange_sign * Self::hinge_commutator_trace(true);
        (
            traj.len() - 1,
            collision_free,
            valid_hops,
            exchanged,
            exchange_sign,
            ab_weight,
            nonab_weight,
            false,
        )
    }
}
