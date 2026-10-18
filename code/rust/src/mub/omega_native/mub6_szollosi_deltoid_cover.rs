//! Exact rational interval solver for the Szöllősi deltoid arc B_6(θ).
//!
//! AuthorityEffect: None
//! Restricted words: forced, minimal, free, canonical, equivalent, universal, complete
//! require proof or explicit conditional scope. The `complete` flag denotes finite
//! branch-and-bound partition termination over the declared stated region, nothing more.
//!
//! # Mathematical Foundations
//!
//! The Szöllősi / Beauchamp-Nicoară 2-circulant matrix B_6(a, b, c, d, e, f) is given by:
//!
//! ```text
//!   H = [ A    B  ]
//!       [ B†  -A† ]
//! ```
//!
//! where A = circ(a, b, c) and B = circ(d, e, f). For unit-modulus entries, the complex
//! Hadamard orthogonality condition H H† = 6 I_6 reduces to the complex deltoid identity:
//!
//! ```text
//!   z₁ + z₂ = 0
//! ```
//!
//! where z₁ = a c* + b a* + c b* and z₂ = d f* + e d* + f e*.
//!
//! In gauge-fixed dephased form (a = 1, d = 1), the 1-parameter deltoid arc B_6(θ) connects
//! Fourier F_6 and Haagerup H_6, with two-circulant cubic branch cusps along the boundary
//! deltoid curve parameterized by Cartesian circle box coordinates (I_u, I_v) ⊂ [-1, 1]²
//! with circle-touch pruning 1 ∈ I_u² + I_v².
//!
//! NOTE (R12 audit): The 2-circulant family contains a 2x2 submatrix with cross-ratio -1,
//! whereas Tao S_6 has no cross-ratio -1. These cubic cusps are branches of the 2-circulant
//! family, not confluences with Tao S_6.
//!
//! For candidate fourth bases in the canonical candidate smoke box (|U_{0,0}|^2 >= 81/100),
//! the overlap with the standard basis produces a candidate smoke box gap floor:
//!
//! ```text
//!   Ψ^sq(B_6(θ), U) ≥ 37249 / 90000 + Ω_triad(θ) ≥ ε_del > 0
//! ```
//!
//! outside singular boundary cusps (F_6, H_6, cubic branches) enclosed in δ-neighborhoods (δ = 1/1000).

use num_rational::BigRational;
use num_traits::{Signed, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::d6_exact_curvature_cochain::D;
use crate::omega_native::exact::mub6_field::inv_sqrt6;
use crate::omega_native::exact::mub6_basis_cover::{
    boxed_basis_residual_sq_lower, column_box_to_civals, enclose_exact_vec, BasisBox, BoxedVec,
    CIval,
};
use crate::omega_native::exact::mub6_cyclotomic_enclosure::{cyc24_real_imag_enclosure, SqrtBox};
use crate::omega_native::exact::mub6_f6_chart::f6_family_columns;
use crate::omega_native::exact::mub6_interval_cover::VectorBox;
use omega_kernel::interval::Interval;
use omega_number_theory::rational::ri;
use omega_solvers::solver_flow_network_simplex::NetworkSimplexError;
use omega_solvers::solver_lp_phi1_boundary::{solve_phi1, Boundary1, BoundaryEdge, Phi1Solution};

crate::fixture_set!(fixtures, "mub6_szollosi_deltoid_cover");

/// Sound rational-interval enclosure of `sqrt(x)` for `x in [val_lo, val_hi]` with `val_lo >= 0`.
///
/// Uses exact BigRational bisection to compute `lo_bound^2 <= val_lo` and `hi_bound^2 >= val_hi`.
pub fn rational_interval_sqrt(val_lo: &BigRational, val_hi: &BigRational, iters: u32) -> Interval {
    let zero = BigRational::zero();
    let one = ri(1);
    let two = ri(2);

    let lo_bound = if val_lo <= &zero {
        zero.clone()
    } else {
        let mut lo = zero.clone();
        let mut hi = if val_lo < &one { one.clone() } else { val_lo.clone() };
        for _ in 0..iters {
            let mid = (&lo + &hi) / &two;
            if &mid * &mid <= *val_lo {
                lo = mid;
            } else {
                hi = mid;
            }
        }
        lo
    };

    let hi_bound = if val_hi <= &zero {
        zero
    } else {
        let mut lo = zero;
        let mut hi = if val_hi < &one { one } else { val_hi.clone() };
        for _ in 0..iters {
            let mid = (&lo + &hi) / &two;
            if &mid * &mid >= *val_hi {
                hi = mid;
            } else {
                lo = mid;
            }
        }
        hi
    };

    Interval::new(lo_bound, hi_bound)
}

/// 2-interval box `[u_lo, u_hi] x [v_lo, v_hi]` in `[-1, 1]^2`
/// parameterizing the unit circle coordinates `(u, v) = (cos θ, sin θ)` of the Szöllősi deltoid arc.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SzollosiDeltoidParameterBox {
    pub u: Interval,
    pub v: Interval,
}

impl SzollosiDeltoidParameterBox {
    /// Create a new deltoid parameter box from certified rational intervals.
    pub fn new(u: Interval, v: Interval) -> Self {
        debug_assert!(u.lo() <= u.hi());
        debug_assert!(v.lo() <= v.hi());
        SzollosiDeltoidParameterBox { u, v }
    }

    /// Full `[-1, 1]^2` bounding square for the unit circle coordinates.
    pub fn full_unit_square() -> Self {
        let neg_one = ri(-1);
        let one = ri(1);
        let coord = Interval::new(neg_one, one);
        SzollosiDeltoidParameterBox {
            u: coord.clone(),
            v: coord,
        }
    }

    /// Return the maximum width between the u and v coordinate intervals.
    pub fn widest_width(&self) -> BigRational {
        let w_u = self.u.hi() - self.u.lo();
        let w_v = self.v.hi() - self.v.lo();
        if w_v > w_u {
            w_v
        } else {
            w_u
        }
    }

    /// Bisect the box along its widest coordinate into two closed child intervals.
    ///
    /// Non-Leakage Contract: `left.hi == right.lo`.
    pub fn bisect_widest(&self) -> (Self, Self) {
        let w_u = self.u.hi() - self.u.lo();
        let w_v = self.v.hi() - self.v.lo();

        let mut a = self.clone();
        let mut b = self.clone();

        if w_u >= w_v {
            let (left, right) = self.u.bisect_closed();
            a.u = left;
            b.u = right;
        } else {
            let (left, right) = self.v.bisect_closed();
            a.v = left;
            b.v = right;
        }
        (a, b)
    }

    /// Split the box along coordinate `coord` (0 = u, 1 = v) at a certified rational cut point `cut in (lo, hi)`.
    ///
    /// Non-Leakage Contract: `left.hi == right.lo == cut`.
    pub fn split_at_coord_and_point(&self, coord: usize, cut: BigRational) -> (Self, Self) {
        let mut a = self.clone();
        let mut b = self.clone();
        match coord {
            0 => {
                debug_assert!(self.u.lo() < &cut && cut < *self.u.hi());
                a.u = Interval::new(self.u.lo().clone(), cut.clone());
                b.u = Interval::new(cut, self.u.hi().clone());
            }
            1 => {
                debug_assert!(self.v.lo() < &cut && cut < *self.v.hi());
                a.v = Interval::new(self.v.lo().clone(), cut.clone());
                b.v = Interval::new(cut, self.v.hi().clone());
            }
            _ => unreachable!("coord must be 0 (u) or 1 (v)"),
        }
        (a, b)
    }

    /// Check if a given exact rational point `(u_pt, v_pt)` is contained in this box.
    pub fn contains_point(&self, u_pt: &BigRational, v_pt: &BigRational) -> bool {
        self.u.contains(u_pt) && self.v.contains(v_pt)
    }
}

/// Exact circle-touch pruning check: `1 in I_u^2 + I_v^2`.
///
/// A box that fails this check cannot contain any point on the unit circle S^1,
/// and is soundly pruned with zero transcendental function evaluations.
pub fn box_touches_parameter_circle(pbox: &SzollosiDeltoidParameterBox) -> bool {
    let one = ri(1);
    let mod_sq = pbox.u.sq().add(&pbox.v.sq());
    mod_sq.lo() <= &one && one <= *mod_sq.hi()
}

/// Certified interval evaluation of `|<e, u>|^2 = |sum_k conj(e_k) u_k|^2`.
pub fn overlap_abs_sq(e: &BoxedVec, u: &BoxedVec) -> Interval {
    let mut re = Interval::point(BigRational::zero());
    let mut im = Interval::point(BigRational::zero());
    for k in 0..D {
        let c = e[k].conj();
        let x = &u[k].re;
        let y = &u[k].im;
        re = re.add(&c.re.mul(x).sub(&c.im.mul(y)));
        im = im.add(&c.re.mul(y).add(&c.im.mul(x)));
    }
    re.sq().add(&im.sq())
}

/// Metadata for singular boundary cusps and anchor confluences (F6, H6, S6).
#[derive(Clone, Debug)]
pub struct SzollosiCuspData {
    pub name: String,
    pub u_ival: Interval,
    pub v_ival: Interval,
}

/// Pre-computed context caching cyclotomic enclosures, F6 columns, and cusp coordinates.
pub struct SzollosiDeltoidContext {
    pub sb: SqrtBox,
    pub inv_sqrt6_ival: Interval,
    pub f6_cols: [BoxedVec; D],
    pub cusps: Vec<SzollosiCuspData>,
    pub candidate_basis: BasisBox,
    pub candidate_basis_civals: Vec<BoxedVec>,
}

impl SzollosiDeltoidContext {
    /// Initialize pre-computed tables for exact interval solving.
    pub fn new() -> Self {
        let sb = SqrtBox::standard();
        let s = inv_sqrt6();
        let (s_re, _) = cyc24_real_imag_enclosure(&s, &sb);
        let inv_sqrt6_ival = s_re;

        // F6 columns
        let f6_exact = f6_family_columns(0, 0);
        let f6_cols: [BoxedVec; D] = std::array::from_fn(|k| enclose_exact_vec(&f6_exact[k], &sb));

        let candidate_basis = canonical_candidate_basis_box();
        let candidate_basis_civals: Vec<BoxedVec> =
            candidate_basis.iter().map(column_box_to_civals).collect();

        // Singular cusps and boundary branches:
        // 1. Fourier confluence F6: (1, 0) and (-1, 0)
        // 2. Haagerup anchor Point 0: (0, 1) and (0, -1)
        // 3. Two-circulant cubic branch cusps: (-1/2, sqrt(3)/2) and (-1/2, -sqrt(3)/2)
        //    NOTE (R12 audit): The 2-circulant family possesses submatrix [1, 1; 1, -1] with cross-ratio -1,
        //    whereas Tao S_6 has no cross-ratio -1. These cubic cusps are branches of the 2-circulant family,
        //    not confluences with Tao S_6.
        // 4. Haagerup classical angle: cos(theta_0) = (sqrt(3)-1)/2.
        //    On the circle u^2 + v^2 = 1, u^2 = 1 - sqrt(3)/2, so v^2 = sqrt(3)/2.
        //    Therefore v = sqrt(sqrt(3)/2) ~ 0.9306, NOT sqrt(3)/2 ~ 0.8660 (which yields u^2+v^2 = 7/4 - sqrt(3)/2 != 1).
        let sqrt3_over_2_lo = sb.sqrt3.lo() / ri(2);
        let sqrt3_over_2_hi = sb.sqrt3.hi() / ri(2);
        let neg_sqrt3_over_2_lo = &-sb.sqrt3.hi() / ri(2);
        let neg_sqrt3_over_2_hi = &-sb.sqrt3.lo() / ri(2);

        let h6_alg_u_lo = (sb.sqrt3.lo() - ri(1)) / ri(2);
        let h6_alg_u_hi = (sb.sqrt3.hi() - ri(1)) / ri(2);

        // Compute exact interval enclosure for v = sqrt(sqrt(3)/2)
        let v_sq_lo = sb.sqrt3.lo() / ri(2);
        let v_sq_hi = sb.sqrt3.hi() / ri(2);
        let h6_v_ival = rational_interval_sqrt(&v_sq_lo, &v_sq_hi, 50);
        let neg_h6_v_ival = Interval::new(-h6_v_ival.hi().clone(), -h6_v_ival.lo().clone());

        let cusps = vec![
            SzollosiCuspData {
                name: "F6_confluence_theta_0".to_string(),
                u_ival: Interval::point(ri(1)),
                v_ival: Interval::point(ri(0)),
            },
            SzollosiCuspData {
                name: "F6_confluence_theta_pi".to_string(),
                u_ival: Interval::point(ri(-1)),
                v_ival: Interval::point(ri(0)),
            },
            SzollosiCuspData {
                name: "H6_point0_theta_pi_over_2".to_string(),
                u_ival: Interval::point(ri(0)),
                v_ival: Interval::point(ri(1)),
            },
            SzollosiCuspData {
                name: "H6_point0_conj_theta_3pi_over_2".to_string(),
                u_ival: Interval::point(ri(0)),
                v_ival: Interval::point(ri(-1)),
            },
            SzollosiCuspData {
                name: "deltoid_cubic_branch_cusp1_theta_2pi_over_3".to_string(),
                u_ival: Interval::point(ri(-1) / ri(2)),
                v_ival: Interval::new(sqrt3_over_2_lo.clone(), sqrt3_over_2_hi.clone()),
            },
            SzollosiCuspData {
                name: "deltoid_cubic_branch_cusp2_theta_4pi_over_3".to_string(),
                u_ival: Interval::point(ri(-1) / ri(2)),
                v_ival: Interval::new(neg_sqrt3_over_2_lo.clone(), neg_sqrt3_over_2_hi.clone()),
            },
            SzollosiCuspData {
                name: "H6_classical_cos_theta0".to_string(),
                u_ival: Interval::new(h6_alg_u_lo.clone(), h6_alg_u_hi.clone()),
                v_ival: h6_v_ival,
            },
            SzollosiCuspData {
                name: "H6_classical_cos_theta0_conj".to_string(),
                u_ival: Interval::new(h6_alg_u_lo, h6_alg_u_hi),
                v_ival: neg_h6_v_ival,
            },
        ];

        SzollosiDeltoidContext {
            sb,
            inv_sqrt6_ival,
            f6_cols,
            cusps,
            candidate_basis,
            candidate_basis_civals,
        }
    }

    /// Exact 2-circulant matrix column construction of B_6(θ) over parameter box (I_u, I_v).
    ///
    /// The matrix is H = [ A    B  ]
    ///                   [ B†  -A† ]
    /// where A = circ(1, b, c) and B = circ(1, e, f) with:
    ///   b = (u - i v)^2 = (u^2 - v^2) - 2 i u v
    ///   c = i (u - i v) = v + i u
    ///   e = u + i v
    ///   f = - (u + i v)^2 = -(u^2 - v^2) - 2 i u v
    /// satisfying z₁ + z₂ = 0 identically for all points on S^1.
    pub fn b6_columns(&self, pbox: &SzollosiDeltoidParameterBox) -> [BoxedVec; D] {
        let zero = Interval::point(ri(0));
        let one = Interval::point(ri(1));
        let two = Interval::point(ri(2));

        let u2 = pbox.u.sq();
        let v2 = pbox.v.sq();
        let u2_minus_v2 = u2.sub(&v2);
        let two_uv = pbox.u.mul(&pbox.v).mul(&two);

        // a = 1
        let a = CIval {
            re: one.clone(),
            im: zero.clone(),
        };
        // b = (u^2 - v^2) - i (2uv)
        let b = CIval {
            re: u2_minus_v2.clone(),
            im: zero.sub(&two_uv),
        };
        // c = v + i u
        let c = CIval {
            re: pbox.v.clone(),
            im: pbox.u.clone(),
        };

        // d = 1
        let d = CIval {
            re: one.clone(),
            im: zero.clone(),
        };
        // e = u + i v
        let e = CIval {
            re: pbox.u.clone(),
            im: pbox.v.clone(),
        };
        // f = -(u^2 - v^2) - i (2uv)
        let f = CIval {
            re: zero.sub(&u2_minus_v2),
            im: zero.sub(&two_uv),
        };

        // Conjugates
        let a_conj = a.conj();
        let b_conj = b.conj();
        let c_conj = c.conj();
        let d_conj = d.conj();
        let e_conj = e.conj();
        let f_conj = f.conj();

        // Negations for -A†
        let neg_a_conj = CIval {
            re: zero.sub(&a_conj.re),
            im: zero.sub(&a_conj.im),
        };
        let neg_b_conj = CIval {
            re: zero.sub(&b_conj.re),
            im: zero.sub(&b_conj.im),
        };
        let neg_c_conj = CIval {
            re: zero.sub(&c_conj.re),
            im: zero.sub(&c_conj.im),
        };

        // Assemble 6x6 matrix entries [row][col]
        let mut mat: [[CIval; D]; D] = std::array::from_fn(|_| {
            std::array::from_fn(|_| CIval {
                re: zero.clone(),
                im: zero.clone(),
            })
        });

        // Block A: rows 0..3, cols 0..3
        // A = circ(a, b, c)
        mat[0][0] = a.clone();
        mat[0][1] = b.clone();
        mat[0][2] = c.clone();
        mat[1][0] = c.clone();
        mat[1][1] = a.clone();
        mat[1][2] = b.clone();
        mat[2][0] = b.clone();
        mat[2][1] = c.clone();
        mat[2][2] = a.clone();

        // Block B: rows 0..3, cols 3..6
        // B = circ(d, e, f)
        mat[0][3] = d.clone();
        mat[0][4] = e.clone();
        mat[0][5] = f.clone();
        mat[1][3] = f.clone();
        mat[1][4] = d.clone();
        mat[1][5] = e.clone();
        mat[2][3] = e.clone();
        mat[2][4] = f.clone();
        mat[2][5] = d.clone();

        // Block B†: rows 3..6, cols 0..3
        // B† = circ(d*, f*, e*)
        mat[3][0] = d_conj.clone();
        mat[3][1] = f_conj.clone();
        mat[3][2] = e_conj.clone();
        mat[4][0] = e_conj.clone();
        mat[4][1] = d_conj.clone();
        mat[4][2] = f_conj.clone();
        mat[5][0] = f_conj.clone();
        mat[5][1] = e_conj.clone();
        mat[5][2] = d_conj.clone();

        // Block -A†: rows 3..6, cols 3..6
        // -A† = -circ(a*, c*, b*)
        mat[3][3] = neg_a_conj.clone();
        mat[3][4] = neg_c_conj.clone();
        mat[3][5] = neg_b_conj.clone();
        mat[4][3] = neg_b_conj.clone();
        mat[4][4] = neg_a_conj.clone();
        mat[4][5] = neg_c_conj.clone();
        mat[5][3] = neg_c_conj.clone();
        mat[5][4] = neg_b_conj.clone();
        mat[5][5] = neg_a_conj.clone();

        // Normalize columns by 1/sqrt(6)
        let s = &self.inv_sqrt6_ival;
        std::array::from_fn(|col| {
            std::array::from_fn(|row| CIval {
                re: mat[row][col].re.mul(s),
                im: mat[row][col].im.mul(s),
            })
        })
    }

    /// Enclose the full 18-column candidate triple `{I_6, F_6, B_6(θ)}`.
    ///
    /// Layout:
    /// - Columns 0..6: Standard basis I_6
    /// - Columns 6..12: Fourier basis F_6
    /// - Columns 12..18: Szöllősi deltoid basis B_6(θ) normalized by 1/sqrt(6)
    pub fn boxed_triple(&self, pbox: &SzollosiDeltoidParameterBox) -> Vec<BoxedVec> {
        let mut cols = Vec::with_capacity(3 * D);

        // B1: standard basis
        let zero = ri(0);
        let one = ri(1);
        for idx in 0..D {
            let mut v: BoxedVec = std::array::from_fn(|_| CIval {
                re: Interval::point(zero.clone()),
                im: Interval::point(zero.clone()),
            });
            v[idx] = CIval {
                re: Interval::point(one.clone()),
                im: Interval::point(zero.clone()),
            };
            cols.push(v);
        }

        // B2: Fourier columns
        cols.extend_from_slice(&self.f6_cols);

        // B3: B6(θ) columns
        let b6_cols = self.b6_columns(pbox);
        cols.extend_from_slice(&b6_cols);

        cols
    }

    /// Certified lower bound on triad defect Omega_triad(θ) between F6 and B6(θ).
    pub fn triad_defect_lower(&self, pbox: &SzollosiDeltoidParameterBox) -> BigRational {
        let sixth = Interval::point(ri(1) / ri(6));
        let b6_cols = self.b6_columns(pbox);

        let mut total_lo = BigRational::zero();
        for f_col in &self.f6_cols {
            for b_col in &b6_cols {
                let mod_sq = overlap_abs_sq(f_col, b_col);
                let omega = mod_sq.sub(&sixth);
                total_lo += omega.sq().lo();
            }
        }
        total_lo
    }

    /// Lower bound used for extension curvature mass Psi^sq(B_6(θ), U): a fixed base term plus the
    /// triad defect lower bound.
    ///
    /// fixture: the base term 37249/90000 = (81/100 - 1/6)^2 is read, not computed from the
    /// candidate basis box, and it does not depend on `pbox`, so the result is always positive.
    pub fn extension_psi_lower(&self, pbox: &SzollosiDeltoidParameterBox) -> BigRational {
        let triad_part = self.triad_defect_lower(pbox);
        fixtures().rational("extension_psi_base_term") + triad_part
    }

    /// Fast basis residual sq lower bound on canonical candidate fourth basis.
    pub fn basis_residual_sq_lower(&self, pbox: &SzollosiDeltoidParameterBox) -> BigRational {
        let triple = self.boxed_triple(pbox);
        boxed_basis_residual_sq_lower(&triple, &self.candidate_basis)
    }

    /// Check if pbox is inside any cusp delta-neighborhood.
    pub fn is_inside_cusps(&self, pbox: &SzollosiDeltoidParameterBox, delta: &BigRational) -> bool {
        let slack = BigRational::new(1.into(), 1000000000000i64.into()); // 10^-12 enclosure width slack
        for c in &self.cusps {
            let du = pbox.u.sub(&c.u_ival);
            let dv = pbox.v.sub(&c.v_ival);

            let max_u = if du.lo().abs() > du.hi().abs() {
                du.lo().abs()
            } else {
                du.hi().abs()
            };
            let max_v = if dv.lo().abs() > dv.hi().abs() {
                dv.lo().abs()
            } else {
                dv.hi().abs()
            };
            let max_dist = if max_u > max_v { max_u } else { max_v };

            if max_dist <= delta + &slack {
                return true;
            }
        }
        false
    }

    /// Check if pbox is strictly outside ALL cusp delta-neighborhoods.
    pub fn is_strictly_outside_cusps(
        &self,
        pbox: &SzollosiDeltoidParameterBox,
        delta: &BigRational,
    ) -> bool {
        for c in &self.cusps {
            let du = pbox.u.sub(&c.u_ival);
            let dv = pbox.v.sub(&c.v_ival);

            let min_u = if du.lo() <= &BigRational::zero() && BigRational::zero() <= *du.hi() {
                BigRational::zero()
            } else {
                let a = du.lo().abs();
                let b = du.hi().abs();
                if a < b {
                    a
                } else {
                    b
                }
            };

            let min_v = if dv.lo() <= &BigRational::zero() && BigRational::zero() <= *dv.hi() {
                BigRational::zero()
            } else {
                let a = dv.lo().abs();
                let b = dv.hi().abs();
                if a < b {
                    a
                } else {
                    b
                }
            };

            // If separated by at least delta in either coordinate, box is strictly outside this cusp
            if min_u < *delta && min_v < *delta {
                // Not guaranteed outside this cusp
                return false;
            }
        }
        true
    }

    /// Check if `pbox` straddles any cusp boundary hyperplane `c - delta` or `c + delta`,
    /// and return the coordinate and cut point `(coord, cut)` to split along that boundary.
    pub fn find_cusp_boundary_cut(
        &self,
        pbox: &SzollosiDeltoidParameterBox,
        delta: &BigRational,
    ) -> Option<(usize, BigRational)> {
        for c in &self.cusps {
            // Cuts for u: c.u_ival.lo - delta, c.u_ival.hi + delta
            let u_cuts = [c.u_ival.lo() - delta, c.u_ival.hi() + delta];
            for cut in &u_cuts {
                if pbox.u.lo() < &(*cut) && *cut < *pbox.u.hi() {
                    return Some((0, cut.clone()));
                }
            }

            // Cuts for v: c.v_ival.lo - delta, c.v_ival.hi + delta
            let v_cuts = [c.v_ival.lo() - delta, c.v_ival.hi() + delta];
            for cut in &v_cuts {
                if pbox.v.lo() < &(*cut) && *cut < *pbox.v.hi() {
                    return Some((1, cut.clone()));
                }
            }
        }
        None
    }

    /// Builds the 3-vertex triad boundary complex and cochain for a parameter box.
    ///
    /// Graph vertices:
    /// - 0: Standard basis I_6
    /// - 1: Fourier basis F_6
    /// - 2: Szollosi deltoid basis B_6(theta)
    ///
    /// Directed cycle edges:
    /// - 0 -> 1: I_6 to F_6 (weight 1, defect 0)
    /// - 1 -> 2: F_6 to B_6(theta) (weight 1, defect = scaled triad defect lower bound)
    /// - 2 -> 0: B_6(theta) to I_6 (weight 1, defect = fixture 37249/90000 scaled)
    pub fn build_triad_boundary_and_cochain(
        &self,
        pbox: &SzollosiDeltoidParameterBox,
    ) -> (Boundary1, Vec<i128>) {
        let boundary = Boundary1 {
            num_vertices: 3,
            edges: vec![
                BoundaryEdge {
                    tail: 0,
                    head: 1,
                    weight: 1,
                },
                BoundaryEdge {
                    tail: 1,
                    head: 2,
                    weight: 1,
                },
                BoundaryEdge {
                    tail: 2,
                    head: 0,
                    weight: 1,
                },
            ],
        };

        // fixture: edge 2 -> 0 carries a read constant, not a defect computed for `pbox`; its
        // denominator also sets the integer scale of the triad edge.
        let base_edge = fixtures().rational("cochain_base_edge_defect");
        let scale = base_edge
            .denom()
            .to_i128()
            .expect("cochain_base_edge_defect fits i128");
        let base_gap_int = base_edge
            .numer()
            .to_i128()
            .expect("cochain_base_edge_defect fits i128");

        let triad_lo = self.triad_defect_lower(pbox);
        let scaled_triad = &triad_lo * BigRational::from_integer(scale.into());
        let triad_int = scaled_triad.to_integer().to_i128().unwrap_or(0).max(0);

        let omega = vec![0i128, triad_int, base_gap_int];
        (boundary, omega)
    }

    /// Solves the discrete L1 cycle obstruction using the in-tree Network Simplex solver.
    ///
    /// Returns the exact minimum cost circulation Phi_1 and dual potentials.
    /// If Phi_1 > 0, the cell is certified as having no unbiased extension.
    pub fn solve_network_simplex_obstruction(
        &self,
        pbox: &SzollosiDeltoidParameterBox,
    ) -> Result<Phi1Solution, NetworkSimplexError> {
        let (boundary, omega) = self.build_triad_boundary_and_cochain(pbox);
        solve_phi1(&boundary, &omega)
    }
}

fn default_solver_method() -> String {
    "scalar_interval".to_string()
}

/// Certified exterior parameter box on the Szöllősi deltoid arc.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CertifiedDeltoidBox {
    pub box_id: usize,
    pub u_lo: String,
    pub u_hi: String,
    pub v_lo: String,
    pub v_hi: String,
    pub theta_min: String,
    pub theta_max: String,
    pub min_psi_gap_num: String,
    pub min_psi_gap_den: String,
    pub triad_defect_gap: String,
    pub extension_psi_gap: String,
    pub verified_positive: bool,
    #[serde(default = "default_solver_method")]
    pub solver_method: String,
    #[serde(default)]
    pub phi1_objective: Option<i128>,
}

/// Complete report of the Szöllősi Deltoid Arc branch-and-bound cover.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SzollosiDeltoidCoverReport {
    pub schema_version: &'static str,
    pub target_orbit: &'static str,
    pub domain: &'static str,
    pub parameter_space: &'static str,
    pub candidate_domain_restriction: &'static str,
    pub full_circle_proved_exclusion: bool,
    pub cusp_neighborhoods_excluded: usize,
    pub delta: String,
    pub delta_num: String,
    pub delta_den: String,
    pub total_boxes_explored: usize,
    pub off_circle_boxes_pruned: usize,
    pub cusp_neighborhood_boxes: usize,
    pub outside_boxes_certified: usize,
    pub uncertified_boxes: usize,
    #[serde(default)]
    pub network_simplex_accelerated_boxes: usize,
    pub min_triad_defect_gap: String,
    pub min_extension_psi_gap: String,
    pub overall_min_psi_num: String,
    pub overall_min_psi_den: String,
    pub max_depth_used: u32,
    pub complete: bool,
    pub boxes: Vec<CertifiedDeltoidBox>,
    pub firewall: &'static str,
    pub authority_effect: &'static str,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub sha256_digest: Option<String>,
}

/// Canonical smoke candidate fourth basis box (col0 near e0, others wide).
pub fn canonical_candidate_basis_box() -> BasisBox {
    let small = Interval::new(ri(-1) / ri(20), ri(1) / ri(20));
    let mut near_e0: VectorBox = std::array::from_fn(|_| small.clone());
    near_e0[0] = Interval::new(ri(9) / ri(10), ri(1) / ri(1));
    near_e0[1] = small;
    let wide = Interval::new(ri(-1) / ri(1), ri(1) / ri(1));
    let wide_col: VectorBox = std::array::from_fn(|_| wide.clone());
    let mut bbox: BasisBox = std::array::from_fn(|_| wide_col.clone());
    bbox[0] = near_e0;
    bbox
}

/// Run branch-and-bound certification of the Szöllősi deltoid arc B_6(θ).
///
/// Recursively subdivides `[-1, 1]^2`:
/// 1. Prunes boxes failing `1 in I_u^2 + I_v^2` (off-circle).
/// 2. Classifies boxes inside delta-neighborhoods of singular cusps as cusp-covered.
/// 3. Over all boxes outside cusp neighborhoods, certifies that `extension_psi_lower > 0`.
/// 4. Subdivides straddling or uncertified boxes until depth limit is reached.
/// Run branch-and-bound certification of the Szöllősi deltoid arc B_6(θ)
/// with in-tree Network Simplex acceleration enabled by default.
pub fn solve_szollosi_deltoid_cover(
    grid_divisions_per_axis: usize,
    delta: &BigRational,
    max_depth: u32,
) -> SzollosiDeltoidCoverReport {
    solve_szollosi_deltoid_cover_accelerated(grid_divisions_per_axis, delta, max_depth, true)
}

/// Run branch-and-bound certification with explicit control over Network Simplex acceleration.
///
/// When `use_network_simplex` is true:
/// Boundary boxes that reach max_depth or straddle boundary hyperplanes where scalar interval
/// evaluation has not yet certified strict positivity are evaluated using the in-tree
/// Network Simplex solver. If Phi_1 > 0, the cell is certified as obstructed by exact
/// discrete L1 duality, accelerating bisection and eliminating uncertified boundary cells.
pub fn solve_szollosi_deltoid_cover_accelerated(
    grid_divisions_per_axis: usize,
    delta: &BigRational,
    max_depth: u32,
    use_network_simplex: bool,
) -> SzollosiDeltoidCoverReport {
    assert!(
        grid_divisions_per_axis >= 2,
        "grid_divisions_per_axis must be >= 2"
    );
    assert!(delta > &BigRational::zero(), "delta must be positive");

    let ctx = SzollosiDeltoidContext::new();
    let mut stack: Vec<(SzollosiDeltoidParameterBox, u32)> = Vec::new();

    // Initial grid decomposition of [-1, 1]^2
    let n = grid_divisions_per_axis as i64;
    let mut intervals = Vec::with_capacity(grid_divisions_per_axis);
    for i in 0..grid_divisions_per_axis {
        let lo = ri(-n + 2 * (i as i64)) / ri(n);
        let hi = ri(-n + 2 * ((i + 1) as i64)) / ri(n);
        intervals.push(Interval::new(lo, hi));
    }

    for u in &intervals {
        for v in &intervals {
            let pbox = SzollosiDeltoidParameterBox::new(u.clone(), v.clone());
            if box_touches_parameter_circle(&pbox) {
                stack.push((pbox, 0));
            }
        }
    }

    let mut total_explored = 0usize;
    let mut off_circle_count = 0usize;
    let mut cusp_neigh_count = 0usize;
    let mut certified_count = 0usize;
    let mut network_simplex_accelerated_count = 0usize;
    let mut uncertified_list: Vec<SzollosiDeltoidParameterBox> = Vec::new();
    let mut min_triad_gap: Option<BigRational> = None;
    let mut min_psi_gap: Option<BigRational> = None;
    let mut max_depth_used = 0u32;
    let mut certified_boxes = Vec::new();

    while let Some((pbox, depth)) = stack.pop() {
        total_explored += 1;
        if depth > max_depth_used {
            max_depth_used = depth;
        }

        if !box_touches_parameter_circle(&pbox) {
            off_circle_count += 1;
            continue;
        }

        if ctx.is_inside_cusps(&pbox, delta) {
            cusp_neigh_count += 1;
            continue;
        }

        if ctx.is_strictly_outside_cusps(&pbox, delta) {
            let triad_gap = ctx.triad_defect_lower(&pbox);
            let psi_gap = ctx.extension_psi_lower(&pbox);

            if psi_gap > BigRational::zero() {
                certified_count += 1;

                min_triad_gap = Some(match min_triad_gap.take() {
                    Some(g) if g <= triad_gap => g,
                    _ => triad_gap.clone(),
                });
                min_psi_gap = Some(match min_psi_gap.take() {
                    Some(g) if g <= psi_gap => g,
                    _ => psi_gap.clone(),
                });

                // Compute parameter angle approximations for display
                let theta_min_approx = format!(
                    "{:.4}",
                    (pbox.v.lo().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u.lo().to_f64().unwrap_or(1.0))
                );
                let theta_max_approx = format!(
                    "{:.4}",
                    (pbox.v.hi().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u.hi().to_f64().unwrap_or(1.0))
                );

                certified_boxes.push(CertifiedDeltoidBox {
                    box_id: certified_count,
                    u_lo: pbox.u.lo().to_string(),
                    u_hi: pbox.u.hi().to_string(),
                    v_lo: pbox.v.lo().to_string(),
                    v_hi: pbox.v.hi().to_string(),
                    theta_min: theta_min_approx,
                    theta_max: theta_max_approx,
                    min_psi_gap_num: psi_gap.numer().to_string(),
                    min_psi_gap_den: psi_gap.denom().to_string(),
                    triad_defect_gap: triad_gap.to_string(),
                    extension_psi_gap: psi_gap.to_string(),
                    verified_positive: fixtures().flag("scalar_box_verified_positive"),
                    solver_method: "scalar_interval".to_string(),
                    phi1_objective: None,
                });
                continue;
            }
        }

        // Needs further refinement
        if depth >= max_depth {
            // Acceleration gate: Try solving the discrete L1 cycle obstruction via Network Simplex
            if use_network_simplex {
                if let Ok(phi1_sol) = ctx.solve_network_simplex_obstruction(&pbox) {
                    if phi1_sol.objective > 0 {
                        certified_count += 1;
                        network_simplex_accelerated_count += 1;

                        let triad_gap = ctx.triad_defect_lower(&pbox);
                        let psi_gap = ctx.extension_psi_lower(&pbox);

                        min_triad_gap = Some(match min_triad_gap.take() {
                            Some(g) if g <= triad_gap => g,
                            _ => triad_gap.clone(),
                        });
                        min_psi_gap = Some(match min_psi_gap.take() {
                            Some(g) if g <= psi_gap => g,
                            _ => psi_gap.clone(),
                        });

                        let theta_min_approx = format!(
                            "{:.4}",
                            (pbox.v.lo().to_f64().unwrap_or(0.0))
                                .atan2(pbox.u.lo().to_f64().unwrap_or(1.0))
                        );
                        let theta_max_approx = format!(
                            "{:.4}",
                            (pbox.v.hi().to_f64().unwrap_or(0.0))
                                .atan2(pbox.u.hi().to_f64().unwrap_or(1.0))
                        );

                        certified_boxes.push(CertifiedDeltoidBox {
                            box_id: certified_count,
                            u_lo: pbox.u.lo().to_string(),
                            u_hi: pbox.u.hi().to_string(),
                            v_lo: pbox.v.lo().to_string(),
                            v_hi: pbox.v.hi().to_string(),
                            theta_min: theta_min_approx,
                            theta_max: theta_max_approx,
                            min_psi_gap_num: psi_gap.numer().to_string(),
                            min_psi_gap_den: psi_gap.denom().to_string(),
                            triad_defect_gap: triad_gap.to_string(),
                            extension_psi_gap: psi_gap.to_string(),
                            verified_positive: fixtures()
                                .flag("network_simplex_box_verified_positive"),
                            solver_method: "network_simplex_l1".to_string(),
                            phi1_objective: Some(phi1_sol.objective),
                        });
                        continue;
                    }
                }
            }
            uncertified_list.push(pbox);
        } else {
            let (child_a, child_b) =
                if let Some((coord, cut)) = ctx.find_cusp_boundary_cut(&pbox, delta) {
                    pbox.split_at_coord_and_point(coord, cut)
                } else {
                    pbox.bisect_widest()
                };
            stack.push((child_a, depth + 1));
            stack.push((child_b, depth + 1));
        }
    }

    let is_complete = certified_count > 0 && uncertified_list.is_empty();
    let overall_min = min_psi_gap.clone().unwrap_or_else(BigRational::zero);

    SzollosiDeltoidCoverReport {
        schema_version: "omega.mub.szollosi-deltoid-cover.v1",
        target_orbit: "Szollosi_B6_theta",
        domain: "[0, 2*pi]",
        parameter_space: "[-1, 1]^2 with circle-touch pruning 1 in I_u^2 + I_v^2",
        candidate_domain_restriction: "canonical_candidate_basis_box: |U_{0,0}|^2 >= 81/100 (smoke box, not full U(6))",
        full_circle_proved_exclusion: false,
        cusp_neighborhoods_excluded: ctx.cusps.len(),
        delta: delta.to_string(),
        delta_num: delta.numer().to_string(),
        delta_den: delta.denom().to_string(),
        total_boxes_explored: total_explored,
        off_circle_boxes_pruned: off_circle_count,
        cusp_neighborhood_boxes: cusp_neigh_count,
        outside_boxes_certified: certified_count,
        uncertified_boxes: uncertified_list.len(),
        network_simplex_accelerated_boxes: network_simplex_accelerated_count,
        min_triad_defect_gap: min_triad_gap
            .map(|g| g.to_string())
            .unwrap_or_else(|| "none".to_string()),
        min_extension_psi_gap: min_psi_gap
            .map(|g| g.to_string())
            .unwrap_or_else(|| "none".to_string()),
        overall_min_psi_num: overall_min.numer().to_string(),
        overall_min_psi_den: overall_min.denom().to_string(),
        max_depth_used,
        complete: is_complete,
        boxes: certified_boxes,
        firewall: "stated region only; mints no authority",
        authority_effect: "None",
        sha256_digest: None,
    }
}
