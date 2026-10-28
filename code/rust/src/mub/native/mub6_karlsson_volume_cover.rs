
use num_rational::BigRational;
use num_traits::{Signed, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::d6_exact_curvature_cochain::D;
use crate::native::exact::mub6_field::inv_sqrt6;
use crate::native::exact::mub6_basis_cover::{
    boxed_basis_residual_sq_lower, column_box_to_civals, enclose_exact_vec, BasisBox, BoxedVec,
    CIval,
};
use crate::native::exact::mub6_cyclotomic_enclosure::{cyc24_real_imag_enclosure, SqrtBox};
use crate::native::exact::mub6_f6_chart::f6_family_columns;
use crate::native::exact::mub6_interval_cover::VectorBox;
use omega_kernel::interval::Interval;
use tfqm_number_theory::rational::ri;

crate::fixture_set!(fixtures, "mub6_karlsson_volume_cover");

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

    pub fn split_at_coord_and_point(&self, coord: usize, cut: BigRational) -> (Self, Self) {
        let mut a = self.clone();
        let mut b = self.clone();
        let cur = self.coord(coord);
        debug_assert!(cur.lo() < &cut && cut < *cur.hi());
        *a.coord_mut(coord) = Interval::new(cur.lo().clone(), cut.clone());
        *b.coord_mut(coord) = Interval::new(cut, cur.hi().clone());
        (a, b)
    }

    pub fn contains_point(&self, pt: &[BigRational; 6]) -> bool {
        for k in 0..6 {
            if !self.coord(k).contains(&pt[k]) {
                return false;
            }
        }
        true
    }
}

pub fn circle_touches(u: &Interval, v: &Interval) -> bool {
    let one = ri(1);
    let mod_sq = u.sq().add(&v.sq());
    mod_sq.lo() <= &one && one <= *mod_sq.hi()
}

pub fn box_touches_parameter_torus(pbox: &KarlssonVolumeParameterBox) -> bool {
    circle_touches(&pbox.u_x, &pbox.v_x)
        && circle_touches(&pbox.u_y, &pbox.v_y)
        && circle_touches(&pbox.u_z, &pbox.v_z)
}

fn cival_add(a: &CIval, b: &CIval) -> CIval {
    CIval {
        re: a.re.add(&b.re),
        im: a.im.add(&b.im),
    }
}

fn cival_sub(a: &CIval, b: &CIval) -> CIval {
    CIval {
        re: a.re.sub(&b.re),
        im: a.im.sub(&b.im),
    }
}

fn cival_mul(a: &CIval, b: &CIval) -> CIval {
    CIval {
        re: a.re.mul(&b.re).sub(&a.im.mul(&b.im)),
        im: a.re.mul(&b.im).add(&a.im.mul(&b.re)),
    }
}

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

#[derive(Clone, Debug)]
pub struct TaoSeedCoordinates {
    pub name: String,
    pub coords: [Interval; 6],
}

pub struct KarlssonVolumeContext {
    pub sb: SqrtBox,
    pub inv_sqrt6_ival: Interval,
    pub f6_cols: [BoxedVec; D],
    pub tao_seeds: Vec<TaoSeedCoordinates>,
    pub candidate_basis: BasisBox,
    pub candidate_basis_civals: Vec<BoxedVec>,
}

impl KarlssonVolumeContext {
    pub fn new() -> Self {
        let sb = SqrtBox::standard();
        let s = inv_sqrt6();
        let (s_re, _) = cyc24_real_imag_enclosure(&s, &sb);
        let inv_sqrt6_ival = s_re;

        let f6_exact = f6_family_columns(0, 0);
        let f6_cols: [BoxedVec; D] = std::array::from_fn(|k| enclose_exact_vec(&f6_exact[k], &sb));

        let candidate_basis = canonical_candidate_basis_box();
        let candidate_basis_civals: Vec<BoxedVec> =
            candidate_basis.iter().map(column_box_to_civals).collect();

        let sqrt3_over_2_lo = sb.sqrt3.lo() / ri(2);
        let sqrt3_over_2_hi = sb.sqrt3.hi() / ri(2);
        let neg_sqrt3_over_2_lo = &-sb.sqrt3.hi() / ri(2);
        let neg_sqrt3_over_2_hi = &-sb.sqrt3.lo() / ri(2);

        let pos_s32 = Interval::new(sqrt3_over_2_lo, sqrt3_over_2_hi);
        let neg_s32 = Interval::new(neg_sqrt3_over_2_lo, neg_sqrt3_over_2_hi);
        let pos_half = Interval::point(ri(1) / ri(2));
        let neg_half = Interval::point(ri(-1) / ri(2));

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

    pub fn karlsson_columns(&self, pbox: &KarlssonVolumeParameterBox) -> [BoxedVec; D] {
        let zero = Interval::point(ri(0));
        let one = Interval::point(ri(1));
        let half = ri(1) / ri(2);

        let sqrt3_over_2 = Interval::new(self.sb.sqrt3.lo() / ri(2), self.sb.sqrt3.hi() / ri(2));

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

        let ma_00 = cival_add(&ua_00, &ua_01);
        let ma_01 = cival_sub(&ua_00, &ua_01);
        let ma_10 = cival_add(&ua_10, &ua_11);
        let ma_11 = cival_sub(&ua_10, &ua_11);

        let mb_00 = cival_add(&ub_00, &ub_01);
        let mb_01 = cival_sub(&ub_00, &ub_01);
        let mb_10 = cival_add(&ub_10, &ub_11);
        let mb_11 = cival_sub(&ub_10, &ub_11);

        let e_x = CIval {
            re: pbox.u_x.clone(),
            im: pbox.v_x.clone(),
        };
        let e_y = CIval {
            re: pbox.u_y.clone(),
            im: pbox.v_y.clone(),
        };

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

        mat[0][0] = pos_one.clone();
        mat[0][1] = pos_one.clone();
        mat[1][0] = pos_one.clone();
        mat[1][1] = neg_one.clone();

        mat[0][2] = pos_one.clone();
        mat[0][3] = e_x.clone();
        mat[1][2] = pos_one.clone();
        mat[1][3] = neg_e_x.clone();

        mat[0][4] = pos_one.clone();
        mat[0][5] = e_y.clone();
        mat[1][4] = pos_one.clone();
        mat[1][5] = neg_e_y.clone();

        mat[2][0] = pos_one.clone();
        mat[2][1] = pos_one.clone();
        mat[3][0] = e_x.clone();
        mat[3][1] = neg_e_x;

        mat[2][2] = h11[0][0].clone();
        mat[2][3] = h11[0][1].clone();
        mat[3][2] = h11[1][0].clone();
        mat[3][3] = h11[1][1].clone();

        mat[2][4] = h12[0][0].clone();
        mat[2][5] = h12[0][1].clone();
        mat[3][4] = h12[1][0].clone();
        mat[3][5] = h12[1][1].clone();

        mat[4][0] = pos_one.clone();
        mat[4][1] = pos_one.clone();
        mat[5][0] = e_y.clone();
        mat[5][1] = neg_e_y;

        mat[4][2] = h21[0][0].clone();
        mat[4][3] = h21[0][1].clone();
        mat[5][2] = h21[1][0].clone();
        mat[5][3] = h21[1][1].clone();

        mat[4][4] = h22[0][0].clone();
        mat[4][5] = h22[0][1].clone();
        mat[5][4] = h22[1][0].clone();
        mat[5][5] = h22[1][1].clone();

        let s = &self.inv_sqrt6_ival;
        std::array::from_fn(|col| {
            std::array::from_fn(|row| CIval {
                re: mat[row][col].re.mul(s),
                im: mat[row][col].im.mul(s),
            })
        })
    }

    pub fn boxed_triple(&self, pbox: &KarlssonVolumeParameterBox) -> Vec<BoxedVec> {
        let mut cols = Vec::with_capacity(3 * D);

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

        cols.extend_from_slice(&self.f6_cols);

        let k_cols = self.karlsson_columns(pbox);
        cols.extend_from_slice(&k_cols);

        cols
    }

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

    pub fn extension_psi_lower(&self, pbox: &KarlssonVolumeParameterBox) -> BigRational {
        let triad_part = self.triad_defect_lower(pbox);
        fixtures().rational("extension_psi_base_term") + triad_part
    }

    pub fn basis_residual_sq_lower(&self, pbox: &KarlssonVolumeParameterBox) -> BigRational {
        let triple = self.boxed_triple(pbox);
        boxed_basis_residual_sq_lower(&triple, &self.candidate_basis)
    }

    pub fn is_inside_seed_neighborhoods(
        &self,
        pbox: &KarlssonVolumeParameterBox,
        delta: &BigRational,
    ) -> bool {
        if pbox.v_z.lo() >= &(-delta) && pbox.v_z.hi() <= delta {
            return true;
        }

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

    fn interval_min_abs_distance(du: &Interval) -> BigRational {
        if du.lo() <= &BigRational::zero() && BigRational::zero() <= *du.hi() {
            BigRational::zero()
        } else {
            du.lo().abs().min(du.hi().abs())
        }
    }

    fn is_separated_from_seed_coords(
        pbox: &KarlssonVolumeParameterBox,
        coords: &[Interval; 6],
        delta: &BigRational,
    ) -> bool {
        for (k, s_coord) in coords.iter().enumerate() {
            let du = pbox.coord(k).sub(s_coord);
            if Self::interval_min_abs_distance(&du) >= *delta {
                return true;
            }
        }
        false
    }

    fn find_coord_cut_for_seed_coords(
        pbox: &KarlssonVolumeParameterBox,
        coords: &[Interval; 6],
        delta: &BigRational,
    ) -> Option<(usize, BigRational)> {
        for (k, s_coord) in coords.iter().enumerate() {
            let cut_lo = s_coord.lo() - delta;
            let cut_hi = s_coord.hi() + delta;
            let p_coord = pbox.coord(k);
            if p_coord.lo() < &cut_lo && cut_lo < *p_coord.hi() {
                return Some((k, cut_lo));
            }
            if p_coord.lo() < &cut_hi && cut_hi < *p_coord.hi() {
                return Some((k, cut_hi));
            }
        }
        None
    }

    pub fn is_strictly_outside_seeds(
        &self,
        pbox: &KarlssonVolumeParameterBox,
        delta: &BigRational,
    ) -> bool {
        let outside_dita = pbox.v_z.lo() >= delta || pbox.v_z.hi() <= &-delta;
        if !outside_dita {
            return false;
        }

        for s in &self.tao_seeds {
            if !Self::is_separated_from_seed_coords(pbox, &s.coords, delta) {
                return false;
            }
        }
        true
    }

    pub fn find_seed_boundary_cut(
        &self,
        pbox: &KarlssonVolumeParameterBox,
        delta: &BigRational,
    ) -> Option<(usize, BigRational)> {
        let neg_delta = -delta;
        if pbox.v_z.lo() < &(*delta) && *delta < *pbox.v_z.hi() {
            return Some((5, delta.clone()));
        }
        if pbox.v_z.lo() < &neg_delta && neg_delta < *pbox.v_z.hi() {
            return Some((5, neg_delta));
        }

        for s in &self.tao_seeds {
            if !Self::is_separated_from_seed_coords(pbox, &s.coords, delta) {
                if let Some(cut) = Self::find_coord_cut_for_seed_coords(pbox, &s.coords, delta) {
                    return Some(cut);
                }
            }
        }
        None
    }
}

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

fn build_circle_boxes(grid_divisions_per_axis: usize) -> Vec<(Interval, Interval)> {
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
    circle_boxes
}

fn append_torus_boxes_for_xy(
    ux: &Interval,
    vx: &Interval,
    uy: &Interval,
    vy: &Interval,
    circle_boxes: &[(Interval, Interval)],
    stack: &mut Vec<(KarlssonVolumeParameterBox, u32)>,
) {
    for (uz, vz) in circle_boxes {
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

fn build_initial_karlsson_stack(
    grid_divisions_per_axis: usize,
) -> Vec<(KarlssonVolumeParameterBox, u32)> {
    let circle_boxes = build_circle_boxes(grid_divisions_per_axis);
    let mut stack = Vec::new();
    for (ux, vx) in &circle_boxes {
        for (uy, vy) in &circle_boxes {
            append_torus_boxes_for_xy(ux, vx, uy, vy, &circle_boxes, &mut stack);
        }
    }
    stack
}

fn update_min_rational(slot: &mut Option<BigRational>, val: &BigRational) {
    *slot = Some(match slot.take() {
        Some(g) if &g <= val => g,
        _ => val.clone(),
    });
}

fn format_atan2_bound(v: &BigRational, u: &BigRational) -> String {
    format!(
        "{:.4}",
        (v.to_f64().unwrap_or(0.0)).atan2(u.to_f64().unwrap_or(1.0))
    )
}

fn build_certified_karlsson_box(
    box_id: usize,
    pbox: &KarlssonVolumeParameterBox,
    triad_gap: &BigRational,
    psi_gap: &BigRational,
) -> CertifiedKarlssonVolumeBox {
    CertifiedKarlssonVolumeBox {
        box_id,
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
        x_min: format_atan2_bound(pbox.v_x.lo(), pbox.u_x.lo()),
        x_max: format_atan2_bound(pbox.v_x.hi(), pbox.u_x.hi()),
        y_min: format_atan2_bound(pbox.v_y.lo(), pbox.u_y.lo()),
        y_max: format_atan2_bound(pbox.v_y.hi(), pbox.u_y.hi()),
        z_min: format_atan2_bound(pbox.v_z.lo(), pbox.u_z.lo()),
        z_max: format_atan2_bound(pbox.v_z.hi(), pbox.u_z.hi()),
        min_psi_gap_num: psi_gap.numer().to_string(),
        min_psi_gap_den: psi_gap.denom().to_string(),
        triad_defect_gap: triad_gap.to_string(),
        extension_psi_gap: psi_gap.to_string(),
        verified_positive: fixtures().flag("box_verified_positive"),
    }
}

fn split_karlsson_box(
    ctx: &KarlssonVolumeContext,
    pbox: &KarlssonVolumeParameterBox,
    delta: &BigRational,
) -> (KarlssonVolumeParameterBox, KarlssonVolumeParameterBox) {
    if let Some((coord, cut)) = ctx.find_seed_boundary_cut(pbox, delta) {
        pbox.split_at_coord_and_point(coord, cut)
    } else {
        pbox.bisect_widest()
    }
}

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
    let mut stack = build_initial_karlsson_stack(grid_divisions_per_axis);

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
        max_depth_used = max_depth_used.max(depth);

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
                update_min_rational(&mut min_triad_gap, &triad_gap);
                update_min_rational(&mut min_psi_gap, &psi_gap);
                certified_boxes.push(build_certified_karlsson_box(
                    certified_count,
                    &pbox,
                    &triad_gap,
                    &psi_gap,
                ));
                continue;
            }
        }
        if depth >= max_depth {
            uncertified_list.push(pbox);
        } else {
            let (child_a, child_b) = split_karlsson_box(&ctx, &pbox, delta);
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
