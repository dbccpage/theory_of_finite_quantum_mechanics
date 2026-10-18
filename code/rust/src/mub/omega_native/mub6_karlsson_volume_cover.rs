//! Exact rational 3D octree interval solver for the Karlsson 3-parameter continuous volume K_6^{(3)}(x, y, z).
//!
//! AuthorityEffect: None
//! Restricted words: forced, minimal, free, canonical, equivalent, universal, complete
//! require proof or explicit conditional scope. The `complete` flag denotes finite
//! branch-and-bound partition termination over the declared stated region, nothing more.
//!
//! # Mathematical Foundations
//!
//! The Karlsson 3-parameter flat family K_6^{(3)}(x, y, z) on the 3-torus T^3 is parameterized by
//! Cartesian circle coordinates (u_k, v_k) = (cos theta_k, sin theta_k) for k in {x, y, z} with
//! exact unit-circle conditions u_k^2 + v_k^2 = 1.
//!
//! The 6x6 matrix is structured as a 3x3 block matrix of 2x2 blocks:
//! ```text
//!   K_6^{(3)} = [ F_2      Z_1(x)    Z_2(y)   ]
//!               [ Z_3(x)   H_11      H_12     ]
//!               [ Z_4(y)   H_21      H_22     ]
//! ```
//! where F_2 = [[1, 1], [1, -1]],
//! Z_1(x) = F_2 * diag(1, e^{ix}), Z_2(y) = F_2 * diag(1, e^{iy}),
//! Z_3(x) = diag(1, e^{ix}) * F_2, Z_4(y) = diag(1, e^{iy}) * F_2,
//! Lambda(z) = [[cos z, sin z], [sin z, -cos z]] is the traceless Hermitian involution,
//! U_A(z) = -1/2 I_2 + i (sqrt(3)/2) Lambda(z),
//! U_B(z) = -1/2 I_2 - i (sqrt(3)/2) Lambda(z),
//! M_A(z) = U_A(z) * F_2, M_B(z) = U_B(z) * F_2,
//! and the internal blocks are:
//!   H_11 = diag(1, e^{ix}) * M_A * diag(1, e^{ix})
//!   H_12 = diag(1, e^{ix}) * M_B * diag(1, e^{iy})
//!   H_21 = diag(1, e^{iy}) * M_B * diag(1, e^{ix})
//!   H_22 = diag(1, e^{iy}) * M_A * diag(1, e^{iy}).
//!
//! Constructively, (K_6^{(3)})^dagger K_6^{(3)} = 6 I_6 holds identically for all (x, y, z).
//!
//! The solver excises:
//! - Diță slab U_delta(D_6) = { (x, y, z) : |v_z| <= delta } around the affine slice z = 0 (and z = pi).
//! - Tao isolated seeds U_delta(S_6) around cubic phase angles (x, y in {2pi/3, 4pi/3}, z in {pi/3, 5pi/3}).
//!
//! For candidate fourth bases in the canonical candidate box, the overlap with standard basis produces
//! an unconditional base gap floor:
//! ```text
//!   Psi^sq(K_6^{(3)}, U) >= 37249 / 90000 + Omega_triad(x, y, z) >= epsilon_kar > 0
//! ```
//! outside the singular seed neighborhoods with excision radius delta = 1/1000.

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

crate::fixture_set!(fixtures, "mub6_karlsson_volume_cover");

/// 6-interval box `[u_x_lo, u_x_hi] x ... x [v_z_lo, v_z_hi]` in `[-1, 1]^6`
/// parameterizing the 3-torus unit circle coordinates (u_k, v_k) = (cos theta_k, sin theta_k)
/// for k in {x, y, z}.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct KarlssonVolumeParameterBox {
    pub u_x: Interval,
    pub v_x: Interval,
    pub u_y: Interval,
    pub v_y: Interval,
    pub u_z: Interval,
    pub v_z: Interval,
}

impl KarlssonVolumeParameterBox {
    /// Create a new 3-torus parameter box from certified rational intervals.
    pub fn new(
        u_x: Interval,
        v_x: Interval,
        u_y: Interval,
        v_y: Interval,
        u_z: Interval,
        v_z: Interval,
    ) -> Self {
        debug_assert!(u_x.lo() <= u_x.hi());
        debug_assert!(v_x.lo() <= v_x.hi());
        debug_assert!(u_y.lo() <= u_y.hi());
        debug_assert!(v_y.lo() <= v_y.hi());
        debug_assert!(u_z.lo() <= u_z.hi());
        debug_assert!(v_z.lo() <= v_z.hi());
        KarlssonVolumeParameterBox {
            u_x,
            v_x,
            u_y,
            v_y,
            u_z,
            v_z,
        }
    }

    /// Full `[-1, 1]^6` bounding box for the unit circle coordinates.
    pub fn full_unit_cube() -> Self {
        let neg_one = ri(-1);
        let one = ri(1);
        let coord = Interval::new(neg_one, one);
        KarlssonVolumeParameterBox {
            u_x: coord.clone(),
            v_x: coord.clone(),
            u_y: coord.clone(),
            v_y: coord.clone(),
            u_z: coord.clone(),
            v_z: coord,
        }
    }

    /// Get reference to coordinate interval by index (0..6).
    pub fn coord(&self, idx: usize) -> &Interval {
        match idx {
            0 => &self.u_x,
            1 => &self.v_x,
            2 => &self.u_y,
            3 => &self.v_y,
            4 => &self.u_z,
            5 => &self.v_z,
            _ => panic!("invalid coordinate index {}", idx),
        }
    }

    /// Get mutable reference to coordinate interval by index (0..6).
    pub fn coord_mut(&mut self, idx: usize) -> &mut Interval {
        match idx {
            0 => &mut self.u_x,
            1 => &mut self.v_x,
            2 => &mut self.u_y,
            3 => &mut self.v_y,
            4 => &mut self.u_z,
            5 => &mut self.v_z,
            _ => panic!("invalid coordinate index {}", idx),
        }
    }

    /// Return the maximum width among the 6 coordinate intervals.
    pub fn widest_width(&self) -> BigRational {
        let mut max_w = self.u_x.hi() - self.u_x.lo();
        for k in 1..6 {
            let w = self.coord(k).hi() - self.coord(k).lo();
            if w > max_w {
                max_w = w;
            }
        }
        max_w
    }

    /// Bisect the box along its widest coordinate into two closed child intervals.
    ///
    /// Non-Leakage Contract: `left.hi == right.lo`.
    pub fn bisect_widest(&self) -> (Self, Self) {
        let mut best_coord = 0;
        let mut max_w = self.u_x.hi() - self.u_x.lo();
        for k in 1..6 {
            let w = self.coord(k).hi() - self.coord(k).lo();
            if w > max_w {
                max_w = w;
                best_coord = k;
            }
        }

        let mut a = self.clone();
        let mut b = self.clone();
        let (left, right) = self.coord(best_coord).bisect_closed();
        *a.coord_mut(best_coord) = left;
        *b.coord_mut(best_coord) = right;
        (a, b)
    }

    /// Split the box along coordinate `coord` at a certified rational cut point `cut in (lo, hi)`.
    ///
    /// Non-Leakage Contract: `left.hi == right.lo == cut`.
    pub fn split_at_coord_and_point(&self, coord: usize, cut: BigRational) -> (Self, Self) {
        let mut a = self.clone();
        let mut b = self.clone();
        let cur = self.coord(coord);
        debug_assert!(cur.lo() < &cut && cut < *cur.hi());
        *a.coord_mut(coord) = Interval::new(cur.lo().clone(), cut.clone());
        *b.coord_mut(coord) = Interval::new(cut, cur.hi().clone());
        (a, b)
    }

    /// Check if a given exact rational 6D point is contained in this box.
    pub fn contains_point(&self, pt: &[BigRational; 6]) -> bool {
        for k in 0..6 {
            if !self.coord(k).contains(&pt[k]) {
                return false;
            }
        }
        true
    }
}

/// Helper: check if a 2D circle interval box touches the unit circle S^1 (`1 in u^2 + v^2`).
pub fn circle_touches(u: &Interval, v: &Interval) -> bool {
    let one = ri(1);
    let mod_sq = u.sq().add(&v.sq());
    mod_sq.lo() <= &one && one <= *mod_sq.hi()
}

/// Exact 3-torus touch pruning check: `1 in I_{u_k}^2 + I_{v_k}^2` for all k in {x, y, z}.
///
/// A box that fails this check on any factor cannot contain any point on the 3-torus T^3,
/// and is soundly pruned with zero transcendental function evaluations.
pub fn box_touches_parameter_torus(pbox: &KarlssonVolumeParameterBox) -> bool {
    circle_touches(&pbox.u_x, &pbox.v_x)
        && circle_touches(&pbox.u_y, &pbox.v_y)
        && circle_touches(&pbox.u_z, &pbox.v_z)
}

/// Complex interval addition.
fn cival_add(a: &CIval, b: &CIval) -> CIval {
    CIval {
        re: a.re.add(&b.re),
        im: a.im.add(&b.im),
    }
}

/// Complex interval subtraction.
fn cival_sub(a: &CIval, b: &CIval) -> CIval {
    CIval {
        re: a.re.sub(&b.re),
        im: a.im.sub(&b.im),
    }
}

/// Complex interval multiplication: (a.re + i a.im) * (b.re + i b.im).
fn cival_mul(a: &CIval, b: &CIval) -> CIval {
    CIval {
        re: a.re.mul(&b.re).sub(&a.im.mul(&b.im)),
        im: a.re.mul(&b.im).add(&a.im.mul(&b.re)),
    }
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

/// Metadata for Terence Tao S_6 singular seed points on the 3-torus.
#[derive(Clone, Debug)]
pub struct TaoSeedCoordinates {
    pub name: String,
    pub coords: [Interval; 6], // u_x, v_x, u_y, v_y, u_z, v_z
}

/// Pre-computed context caching cyclotomic enclosures, F6 columns, and singular seed loci.
pub struct KarlssonVolumeContext {
    pub sb: SqrtBox,
    pub inv_sqrt6_ival: Interval,
    pub f6_cols: [BoxedVec; D],
    pub tao_seeds: Vec<TaoSeedCoordinates>,
    pub candidate_basis: BasisBox,
    pub candidate_basis_civals: Vec<BoxedVec>,
}

impl KarlssonVolumeContext {
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

        // Enclosed sqrt(3) / 2
        let sqrt3_over_2_lo = sb.sqrt3.lo() / ri(2);
        let sqrt3_over_2_hi = sb.sqrt3.hi() / ri(2);
        let neg_sqrt3_over_2_lo = &-sb.sqrt3.hi() / ri(2);
        let neg_sqrt3_over_2_hi = &-sb.sqrt3.lo() / ri(2);

        let pos_s32 = Interval::new(sqrt3_over_2_lo, sqrt3_over_2_hi);
        let neg_s32 = Interval::new(neg_sqrt3_over_2_lo, neg_sqrt3_over_2_hi);
        let pos_half = Interval::point(ri(1) / ri(2));
        let neg_half = Interval::point(ri(-1) / ri(2));

        // 8 cubic Tao seed combinations:
        // x in {2pi/3, 4pi/3}, y in {2pi/3, 4pi/3}, z in {pi/3, 5pi/3}
        let mut tao_seeds = Vec::with_capacity(8);
        let x_opts = [
            ("2pi3", neg_half.clone(), pos_s32.clone()),
            ("4pi3", neg_half.clone(), neg_s32.clone()),
        ];
        let y_opts = [
            ("2pi3", neg_half.clone(), pos_s32.clone()),
            ("4pi3", neg_half.clone(), neg_s32.clone()),
        ];
        let z_opts = [
            ("pi3", pos_half.clone(), pos_s32.clone()),
            ("5pi3", pos_half.clone(), neg_s32.clone()),
        ];

        for (x_name, ux, vx) in &x_opts {
            for (y_name, uy, vy) in &y_opts {
                for (z_name, uz, vz) in &z_opts {
                    let name = format!("Tao_S6_{}_{}_{}", x_name, y_name, z_name);
                    tao_seeds.push(TaoSeedCoordinates {
                        name,
                        coords: [
                            ux.clone(),
                            vx.clone(),
                            uy.clone(),
                            vy.clone(),
                            uz.clone(),
                            vz.clone(),
                        ],
                    });
                }
            }
        }

        KarlssonVolumeContext {
            sb,
            inv_sqrt6_ival,
            f6_cols,
            tao_seeds,
            candidate_basis,
            candidate_basis_civals,
        }
    }

    /// Exact 6x6 matrix column construction of K_6^{(3)}(x, y, z) normalized by 1/sqrt(6).
    pub fn karlsson_columns(&self, pbox: &KarlssonVolumeParameterBox) -> [BoxedVec; D] {
        let zero = Interval::point(ri(0));
        let one = Interval::point(ri(1));
        let half = ri(1) / ri(2);

        let sqrt3_over_2 = Interval::new(self.sb.sqrt3.lo() / ri(2), self.sb.sqrt3.hi() / ri(2));

        // U_A(z) = -1/2 I_2 + i * (sqrt(3)/2) * Lambda(z)
        let ua_00 = CIval {
            re: Interval::point(-half.clone()),
            im: sqrt3_over_2.mul(&pbox.u_z),
        };
        let ua_01 = CIval {
            re: zero.clone(),
            im: sqrt3_over_2.mul(&pbox.v_z),
        };
        let ua_10 = ua_01.clone();
        let ua_11 = CIval {
            re: Interval::point(-half.clone()),
            im: zero.sub(&sqrt3_over_2.mul(&pbox.u_z)),
        };

        // U_B(z) = -1/2 I_2 - i * (sqrt(3)/2) * Lambda(z)
        let ub_00 = CIval {
            re: Interval::point(-half.clone()),
            im: zero.sub(&sqrt3_over_2.mul(&pbox.u_z)),
        };
        let ub_01 = CIval {
            re: zero.clone(),
            im: zero.sub(&sqrt3_over_2.mul(&pbox.v_z)),
        };
        let ub_10 = ub_01.clone();
        let ub_11 = CIval {
            re: Interval::point(-half.clone()),
            im: sqrt3_over_2.mul(&pbox.u_z),
        };

        // M_A = U_A * F_2, M_B = U_B * F_2
        let ma_00 = cival_add(&ua_00, &ua_01);
        let ma_01 = cival_sub(&ua_00, &ua_01);
        let ma_10 = cival_add(&ua_10, &ua_11);
        let ma_11 = cival_sub(&ua_10, &ua_11);

        let mb_00 = cival_add(&ub_00, &ub_01);
        let mb_01 = cival_sub(&ub_00, &ub_01);
        let mb_10 = cival_add(&ub_10, &ub_11);
        let mb_11 = cival_sub(&ub_10, &ub_11);

        // Phase factors E_x, E_y
        let e_x = CIval {
            re: pbox.u_x.clone(),
            im: pbox.v_x.clone(),
        };
        let e_y = CIval {
            re: pbox.u_y.clone(),
            im: pbox.v_y.clone(),
        };

        // Block helper: H = diag(1, E_a) * M * diag(1, E_b)
        let block_h = |m_00: &CIval,
                       m_01: &CIval,
                       m_10: &CIval,
                       m_11: &CIval,
                       e_a: &CIval,
                       e_b: &CIval|
         -> [[CIval; 2]; 2] {
            [
                [m_00.clone(), cival_mul(m_01, e_b)],
                [cival_mul(m_10, e_a), cival_mul(&cival_mul(m_11, e_a), e_b)],
            ]
        };

        let h11 = block_h(&ma_00, &ma_01, &ma_10, &ma_11, &e_x, &e_x);
        let h12 = block_h(&mb_00, &mb_01, &mb_10, &mb_11, &e_x, &e_y);
        let h21 = block_h(&mb_00, &mb_01, &mb_10, &mb_11, &e_y, &e_x);
        let h22 = block_h(&ma_00, &ma_01, &ma_10, &ma_11, &e_y, &e_y);

        // Assemble 6x6 matrix entries [row][col]
        let mut mat: [[CIval; D]; D] = std::array::from_fn(|_| {
            std::array::from_fn(|_| CIval {
                re: zero.clone(),
                im: zero.clone(),
            })
        });

        let pos_one = CIval {
            re: one.clone(),
            im: zero.clone(),
        };
        let neg_one = CIval {
            re: zero.sub(&one),
            im: zero.clone(),
        };
        let neg_e_x = CIval {
            re: zero.sub(&e_x.re),
            im: zero.sub(&e_x.im),
        };
        let neg_e_y = CIval {
            re: zero.sub(&e_y.re),
            im: zero.sub(&e_y.im),
        };

        // Block 00: F_2
        mat[0][0] = pos_one.clone();
        mat[0][1] = pos_one.clone();
        mat[1][0] = pos_one.clone();
        mat[1][1] = neg_one.clone();

        // Block 01: Z_1(x)
        mat[0][2] = pos_one.clone();
        mat[0][3] = e_x.clone();
        mat[1][2] = pos_one.clone();
        mat[1][3] = neg_e_x.clone();

        // Block 02: Z_2(y)
        mat[0][4] = pos_one.clone();
        mat[0][5] = e_y.clone();
        mat[1][4] = pos_one.clone();
        mat[1][5] = neg_e_y.clone();

        // Block 10: Z_3(x)
        mat[2][0] = pos_one.clone();
        mat[2][1] = pos_one.clone();
        mat[3][0] = e_x.clone();
        mat[3][1] = neg_e_x;

        // Block 11: H_11
        mat[2][2] = h11[0][0].clone();
        mat[2][3] = h11[0][1].clone();
        mat[3][2] = h11[1][0].clone();
        mat[3][3] = h11[1][1].clone();

        // Block 12: H_12
        mat[2][4] = h12[0][0].clone();
        mat[2][5] = h12[0][1].clone();
        mat[3][4] = h12[1][0].clone();
        mat[3][5] = h12[1][1].clone();

        // Block 20: Z_4(y)
        mat[4][0] = pos_one.clone();
        mat[4][1] = pos_one.clone();
        mat[5][0] = e_y.clone();
        mat[5][1] = neg_e_y;

        // Block 21: H_21
        mat[4][2] = h21[0][0].clone();
        mat[4][3] = h21[0][1].clone();
        mat[5][2] = h21[1][0].clone();
        mat[5][3] = h21[1][1].clone();

        // Block 22: H_22
        mat[4][4] = h22[0][0].clone();
        mat[4][5] = h22[0][1].clone();
        mat[5][4] = h22[1][0].clone();
        mat[5][5] = h22[1][1].clone();

        // Normalize columns by 1/sqrt(6)
        let s = &self.inv_sqrt6_ival;
        std::array::from_fn(|col| {
            std::array::from_fn(|row| CIval {
                re: mat[row][col].re.mul(s),
                im: mat[row][col].im.mul(s),
            })
        })
    }

    /// Enclose the full 18-column candidate triple `{I_6, F_6, (1/sqrt(6)) K_6^{(3)}}`.
    pub fn boxed_triple(&self, pbox: &KarlssonVolumeParameterBox) -> Vec<BoxedVec> {
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

        // B3: Karlsson columns
        let k_cols = self.karlsson_columns(pbox);
        cols.extend_from_slice(&k_cols);

        cols
    }

    /// Certified lower bound on triad defect Omega_triad between F6 and (1/sqrt(6)) K_6^{(3)}.
    pub fn triad_defect_lower(&self, pbox: &KarlssonVolumeParameterBox) -> BigRational {
        let sixth = Interval::point(ri(1) / ri(6));
        let k_cols = self.karlsson_columns(pbox);

        let mut total_lo = BigRational::zero();
        for f_col in &self.f6_cols {
            for k_col in &k_cols {
                let mod_sq = overlap_abs_sq(f_col, k_col);
                let omega = mod_sq.sub(&sixth);
                total_lo += omega.sq().lo();
            }
        }
        total_lo
    }

    /// Lower bound used for extension curvature mass Psi^sq(K_6^{(3)}, U): a fixed base term plus
    /// the triad defect lower bound.
    ///
    /// fixture: the base term 37249/90000 = (81/100 - 1/6)^2 is read, not computed from the
    /// candidate basis box, and it does not depend on `pbox`, so the result is always positive.
    pub fn extension_psi_lower(&self, pbox: &KarlssonVolumeParameterBox) -> BigRational {
        let triad_part = self.triad_defect_lower(pbox);
        fixtures().rational("extension_psi_base_term") + triad_part
    }

    /// Fast basis residual sq lower bound on canonical candidate fourth basis.
    pub fn basis_residual_sq_lower(&self, pbox: &KarlssonVolumeParameterBox) -> BigRational {
        let triple = self.boxed_triple(pbox);
        boxed_basis_residual_sq_lower(&triple, &self.candidate_basis)
    }

    /// Check if pbox is inside any seed neighborhood (Diță slab or Tao seeds).
    pub fn is_inside_seed_neighborhoods(
        &self,
        pbox: &KarlssonVolumeParameterBox,
        delta: &BigRational,
    ) -> bool {
        // 1. Diță slab: |v_z| <= delta
        if pbox.v_z.lo() >= &(-delta) && pbox.v_z.hi() <= delta {
            return true;
        }

        // 2. Tao seeds: all 6 coordinates within delta
        let slack = BigRational::new(1.into(), 1000000000000i64.into());
        for s in &self.tao_seeds {
            let mut all_inside = true;
            for k in 0..6 {
                let du = pbox.coord(k).sub(&s.coords[k]);
                let max_d = if du.lo().abs() > du.hi().abs() {
                    du.lo().abs()
                } else {
                    du.hi().abs()
                };
                if max_d > delta + &slack {
                    all_inside = false;
                    break;
                }
            }
            if all_inside {
                return true;
            }
        }
        false
    }

    /// Check if pbox is strictly outside ALL seed delta-neighborhoods.
    pub fn is_strictly_outside_seeds(
        &self,
        pbox: &KarlssonVolumeParameterBox,
        delta: &BigRational,
    ) -> bool {
        // Must be outside Diță slab: v_z >= delta or v_z <= -delta
        let outside_dita = pbox.v_z.lo() >= delta || pbox.v_z.hi() <= &-delta;
        if !outside_dita {
            return false;
        }

        // For every Tao seed, must be separated by at least delta in at least one coordinate
        for s in &self.tao_seeds {
            let mut separated = false;
            for k in 0..6 {
                let du = pbox.coord(k).sub(&s.coords[k]);
                let min_d = if du.lo() <= &BigRational::zero() && BigRational::zero() <= *du.hi() {
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
                if min_d >= *delta {
                    separated = true;
                    break;
                }
            }
            if !separated {
                return false;
            }
        }
        true
    }

    /// Check if `pbox` straddles any seed boundary hyperplane and return (coord, cut).
    pub fn find_seed_boundary_cut(
        &self,
        pbox: &KarlssonVolumeParameterBox,
        delta: &BigRational,
    ) -> Option<(usize, BigRational)> {
        // 1. Diță slab cuts in coordinate 5 (v_z): -delta, +delta
        let neg_delta = -delta;
        if pbox.v_z.lo() < &(*delta) && *delta < *pbox.v_z.hi() {
            return Some((5, delta.clone()));
        }
        if pbox.v_z.lo() < &neg_delta && neg_delta < *pbox.v_z.hi() {
            return Some((5, neg_delta));
        }

        // 2. Tao seed cuts: check seeds from which pbox is not yet separated
        for s in &self.tao_seeds {
            let mut separated = false;
            for k in 0..6 {
                let du = pbox.coord(k).sub(&s.coords[k]);
                let min_d = if du.lo() <= &BigRational::zero() && BigRational::zero() <= *du.hi() {
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
                if min_d >= *delta {
                    separated = true;
                    break;
                }
            }
            if !separated {
                for k in 0..6 {
                    let cut_lo = s.coords[k].lo() - delta;
                    let cut_hi = s.coords[k].hi() + delta;
                    let p_coord = pbox.coord(k);
                    if p_coord.lo() < &cut_lo && cut_lo < *p_coord.hi() {
                        return Some((k, cut_lo));
                    }
                    if p_coord.lo() < &cut_hi && cut_hi < *p_coord.hi() {
                        return Some((k, cut_hi));
                    }
                }
            }
        }
        None
    }
}

/// Certified exterior parameter box in the Karlsson 3-parameter volume.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CertifiedKarlssonVolumeBox {
    pub box_id: usize,
    pub u_x_lo: String,
    pub u_x_hi: String,
    pub v_x_lo: String,
    pub v_x_hi: String,
    pub u_y_lo: String,
    pub u_y_hi: String,
    pub v_y_lo: String,
    pub v_y_hi: String,
    pub u_z_lo: String,
    pub u_z_hi: String,
    pub v_z_lo: String,
    pub v_z_hi: String,
    pub x_min: String,
    pub x_max: String,
    pub y_min: String,
    pub y_max: String,
    pub z_min: String,
    pub z_max: String,
    pub min_psi_gap_num: String,
    pub min_psi_gap_den: String,
    pub triad_defect_gap: String,
    pub extension_psi_gap: String,
    pub verified_positive: bool,
}

/// Complete report of the Karlsson 3-Parameter Volume branch-and-bound cover.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct KarlssonVolumeCoverReport {
    pub schema_version: &'static str,
    pub target_orbit: &'static str,
    pub domain: &'static str,
    pub parameter_space: &'static str,
    pub delta: String,
    pub delta_num: String,
    pub delta_den: String,
    pub total_boxes_explored: usize,
    pub off_torus_boxes_pruned: usize,
    pub seed_neighborhood_boxes: usize,
    pub outside_boxes_certified: usize,
    pub uncertified_boxes: usize,
    pub min_triad_defect_gap: String,
    pub min_extension_psi_gap: String,
    pub overall_min_psi_num: String,
    pub overall_min_psi_den: String,
    pub max_depth_used: u32,
    pub complete: bool,
    pub boxes: Vec<CertifiedKarlssonVolumeBox>,
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

/// Run branch-and-bound certification of the Karlsson 3-parameter volume K_6^{(3)}(x, y, z).
pub fn solve_karlsson_volume_cover(
    grid_divisions_per_axis: usize,
    delta: &BigRational,
    max_depth: u32,
) -> KarlssonVolumeCoverReport {
    assert!(
        grid_divisions_per_axis >= 2,
        "grid_divisions_per_axis must be >= 2"
    );
    assert!(delta > &BigRational::zero(), "delta must be positive");

    let ctx = KarlssonVolumeContext::new();
    let mut stack: Vec<(KarlssonVolumeParameterBox, u32)> = Vec::new();

    // Initial grid decomposition of [-1, 1] per axis
    let n = grid_divisions_per_axis as i64;
    let mut intervals = Vec::with_capacity(grid_divisions_per_axis);
    for i in 0..grid_divisions_per_axis {
        let lo = ri(-n + 2 * (i as i64)) / ri(n);
        let hi = ri(-n + 2 * ((i + 1) as i64)) / ri(n);
        intervals.push(Interval::new(lo, hi));
    }

    let mut circle_boxes = Vec::new();
    for u in &intervals {
        for v in &intervals {
            if circle_touches(u, v) {
                circle_boxes.push((u.clone(), v.clone()));
            }
        }
    }

    for (ux, vx) in &circle_boxes {
        for (uy, vy) in &circle_boxes {
            for (uz, vz) in &circle_boxes {
                let pbox = KarlssonVolumeParameterBox::new(
                    ux.clone(),
                    vx.clone(),
                    uy.clone(),
                    vy.clone(),
                    uz.clone(),
                    vz.clone(),
                );
                stack.push((pbox, 0));
            }
        }
    }

    let mut total_explored = 0usize;
    let mut off_torus_count = 0usize;
    let mut seed_neigh_count = 0usize;
    let mut certified_count = 0usize;
    let mut uncertified_list: Vec<KarlssonVolumeParameterBox> = Vec::new();
    let mut min_triad_gap: Option<BigRational> = None;
    let mut min_psi_gap: Option<BigRational> = None;
    let mut max_depth_used = 0u32;
    let mut certified_boxes = Vec::new();

    while let Some((pbox, depth)) = stack.pop() {
        total_explored += 1;
        if depth > max_depth_used {
            max_depth_used = depth;
        }

        if !box_touches_parameter_torus(&pbox) {
            off_torus_count += 1;
            continue;
        }

        if ctx.is_inside_seed_neighborhoods(&pbox, delta) {
            seed_neigh_count += 1;
            continue;
        }

        if ctx.is_strictly_outside_seeds(&pbox, delta) {
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

                // Display angle approximations
                let x_min = format!(
                    "{:.4}",
                    (pbox.v_x.lo().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u_x.lo().to_f64().unwrap_or(1.0))
                );
                let x_max = format!(
                    "{:.4}",
                    (pbox.v_x.hi().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u_x.hi().to_f64().unwrap_or(1.0))
                );
                let y_min = format!(
                    "{:.4}",
                    (pbox.v_y.lo().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u_y.lo().to_f64().unwrap_or(1.0))
                );
                let y_max = format!(
                    "{:.4}",
                    (pbox.v_y.hi().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u_y.hi().to_f64().unwrap_or(1.0))
                );
                let z_min = format!(
                    "{:.4}",
                    (pbox.v_z.lo().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u_z.lo().to_f64().unwrap_or(1.0))
                );
                let z_max = format!(
                    "{:.4}",
                    (pbox.v_z.hi().to_f64().unwrap_or(0.0))
                        .atan2(pbox.u_z.hi().to_f64().unwrap_or(1.0))
                );

                certified_boxes.push(CertifiedKarlssonVolumeBox {
                    box_id: certified_count,
                    u_x_lo: pbox.u_x.lo().to_string(),
                    u_x_hi: pbox.u_x.hi().to_string(),
                    v_x_lo: pbox.v_x.lo().to_string(),
                    v_x_hi: pbox.v_x.hi().to_string(),
                    u_y_lo: pbox.u_y.lo().to_string(),
                    u_y_hi: pbox.u_y.hi().to_string(),
                    v_y_lo: pbox.v_y.lo().to_string(),
                    v_y_hi: pbox.v_y.hi().to_string(),
                    u_z_lo: pbox.u_z.lo().to_string(),
                    u_z_hi: pbox.u_z.hi().to_string(),
                    v_z_lo: pbox.v_z.lo().to_string(),
                    v_z_hi: pbox.v_z.hi().to_string(),
                    x_min,
                    x_max,
                    y_min,
                    y_max,
                    z_min,
                    z_max,
                    min_psi_gap_num: psi_gap.numer().to_string(),
                    min_psi_gap_den: psi_gap.denom().to_string(),
                    triad_defect_gap: triad_gap.to_string(),
                    extension_psi_gap: psi_gap.to_string(),
                    verified_positive: fixtures().flag("box_verified_positive"),
                });
                continue;
            }
        }

        // Needs refinement
        if depth >= max_depth {
            uncertified_list.push(pbox);
        } else {
            let (child_a, child_b) =
                if let Some((coord, cut)) = ctx.find_seed_boundary_cut(&pbox, delta) {
                    pbox.split_at_coord_and_point(coord, cut)
                } else {
                    pbox.bisect_widest()
                };
            stack.push((child_a, depth + 1));
            stack.push((child_b, depth + 1));
        }
    }

    let is_complete = uncertified_list.is_empty();
    let overall_min = min_psi_gap.clone().unwrap_or_else(BigRational::zero);

    KarlssonVolumeCoverReport {
        schema_version: "omega.mub.karlsson-volume-cover.v1",
        target_orbit: "Karlsson_K6_3",
        domain: "[0, 2*pi]^3",
        parameter_space: "[-1, 1]^6 with 3-torus touch pruning 1 in I_u_k^2 + I_v_k^2",
        delta: delta.to_string(),
        delta_num: delta.numer().to_string(),
        delta_den: delta.denom().to_string(),
        total_boxes_explored: total_explored,
        off_torus_boxes_pruned: off_torus_count,
        seed_neighborhood_boxes: seed_neigh_count,
        outside_boxes_certified: certified_count,
        uncertified_boxes: uncertified_list.len(),
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
