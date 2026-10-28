
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};

use crate::native::exact::d6_exact_curvature_cochain::D;
use crate::native::exact::mub6_field::inv_sqrt6;
use crate::native::exact::mub6_basis_cover::{
    boxed_basis_residual_sq_lower, column_box_to_civals, enclose_exact_vec, BasisBox, BoxedVec,
    CIval,
};
use crate::native::exact::mub6_cyclotomic_enclosure::{cyc24_real_imag_enclosure, SqrtBox};
use crate::native::campaign::mub6_f6_external_b3::product_y2_qa_columns;
use crate::native::exact::mub6_interval_cover::VectorBox;
use engine_kernel::interval::Interval;
use engine_number_theory::cyclotomic::Cyc24;
use engine_number_theory::rational::ri;

crate::fixture_set!(fixtures, "mub6_continuous_manifold_residue");

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DitaContinuousParameterBox {
    pub u_alpha: Interval,
    pub v_alpha: Interval,
    pub u_beta: Interval,
    pub v_beta: Interval,
}

impl DitaContinuousParameterBox {
    pub fn new(u_alpha: Interval, v_alpha: Interval, u_beta: Interval, v_beta: Interval) -> Self {
        debug_assert!(u_alpha.lo() <= u_alpha.hi());
        debug_assert!(v_alpha.lo() <= v_alpha.hi());
        debug_assert!(u_beta.lo() <= u_beta.hi());
        debug_assert!(v_beta.lo() <= v_beta.hi());
        DitaContinuousParameterBox {
            u_alpha,
            v_alpha,
            u_beta,
            v_beta,
        }
    }

    pub fn full_unit_cube() -> Self {
        let neg_one = ri(-1);
        let one = ri(1);
        let coord = Interval::new(neg_one, one);
        DitaContinuousParameterBox {
            u_alpha: coord.clone(),
            v_alpha: coord.clone(),
            u_beta: coord.clone(),
            v_beta: coord,
        }
    }

    pub fn widest_width(&self) -> BigRational {
        let mut w = self.u_alpha.hi() - self.u_alpha.lo();
        let w_va = self.v_alpha.hi() - self.v_alpha.lo();
        if w_va > w {
            w = w_va;
        }
        let w_ub = self.u_beta.hi() - self.u_beta.lo();
        if w_ub > w {
            w = w_ub;
        }
        let w_vb = self.v_beta.hi() - self.v_beta.lo();
        if w_vb > w {
            w = w_vb;
        }
        w
    }

    pub fn bisect_widest(&self) -> (Self, Self) {
        let mut best_coord = 0;
        let mut max_w = self.u_alpha.hi() - self.u_alpha.lo();

        let w_va = self.v_alpha.hi() - self.v_alpha.lo();
        if w_va > max_w {
            max_w = w_va;
            best_coord = 1;
        }
        let w_ub = self.u_beta.hi() - self.u_beta.lo();
        if w_ub > max_w {
            max_w = w_ub;
            best_coord = 2;
        }
        let w_vb = self.v_beta.hi() - self.v_beta.lo();
        if w_vb > max_w {
            best_coord = 3;
        }

        let mut a = self.clone();
        let mut b = self.clone();

        match best_coord {
            0 => {
                let (left, right) = self.u_alpha.bisect_closed();
                a.u_alpha = left;
                b.u_alpha = right;
            }
            1 => {
                let (left, right) = self.v_alpha.bisect_closed();
                a.v_alpha = left;
                b.v_alpha = right;
            }
            2 => {
                let (left, right) = self.u_beta.bisect_closed();
                a.u_beta = left;
                b.u_beta = right;
            }
            3 => {
                let (left, right) = self.v_beta.bisect_closed();
                a.v_beta = left;
                b.v_beta = right;
            }
            _ => unreachable!(),
        }
        (a, b)
    }

    pub fn split_at_coord_and_point(&self, coord: usize, cut: BigRational) -> (Self, Self) {
        let mut a = self.clone();
        let mut b = self.clone();
        match coord {
            0 => {
                debug_assert!(self.u_alpha.lo() < &cut && cut < *self.u_alpha.hi());
                a.u_alpha = Interval::new(self.u_alpha.lo().clone(), cut.clone());
                b.u_alpha = Interval::new(cut, self.u_alpha.hi().clone());
            }
            1 => {
                debug_assert!(self.v_alpha.lo() < &cut && cut < *self.v_alpha.hi());
                a.v_alpha = Interval::new(self.v_alpha.lo().clone(), cut.clone());
                b.v_alpha = Interval::new(cut, self.v_alpha.hi().clone());
            }
            2 => {
                debug_assert!(self.u_beta.lo() < &cut && cut < *self.u_beta.hi());
                a.u_beta = Interval::new(self.u_beta.lo().clone(), cut.clone());
                b.u_beta = Interval::new(cut, self.u_beta.hi().clone());
            }
            3 => {
                debug_assert!(self.v_beta.lo() < &cut && cut < *self.v_beta.hi());
                a.v_beta = Interval::new(self.v_beta.lo().clone(), cut.clone());
                b.v_beta = Interval::new(cut, self.v_beta.hi().clone());
            }
            _ => unreachable!(),
        }
        (a, b)
    }

    pub fn contains_point(
        &self,
        ua: &BigRational,
        va: &BigRational,
        ub: &BigRational,
        vb: &BigRational,
    ) -> bool {
        self.u_alpha.contains(ua)
            && self.v_alpha.contains(va)
            && self.u_beta.contains(ub)
            && self.v_beta.contains(vb)
    }
}

pub fn box_touches_parameter_torus(pbox: &DitaContinuousParameterBox) -> bool {
    let one = ri(1);
    let mod_sq_alpha = pbox.u_alpha.sq().add(&pbox.v_alpha.sq());
    let mod_sq_beta = pbox.u_beta.sq().add(&pbox.v_beta.sq());
    mod_sq_alpha.lo() <= &one
        && one <= *mod_sq_alpha.hi()
        && mod_sq_beta.lo() <= &one
        && one <= *mod_sq_beta.hi()
}

fn f3(j: usize, k: usize) -> Cyc24 {
    Cyc24::zeta24(((8 * j * k) % 24) as i32)
}

pub fn dita_continuous_matrix_columns(
    pbox: &DitaContinuousParameterBox,
    sb: &SqrtBox,
) -> [BoxedVec; D] {
    let s = inv_sqrt6();
    let zero = ri(0);
    let zero_ival = Interval::point(zero);

    let mut c_re = [
        [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
        [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
        [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
    ];
    let mut c_im = [
        [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
        [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
        [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
    ];

    for j in 0..3 {
        for k in 0..3 {
            let elem = f3(j, k).mul(&s);
            let (re, im) = cyc24_real_imag_enclosure(&elem, sb);
            c_re[j][k] = re;
            c_im[j][k] = im;
        }
    }

    std::array::from_fn(|col| {
        let mut v: BoxedVec = std::array::from_fn(|_| CIval {
            re: zero_ival.clone(),
            im: zero_ival.clone(),
        });
        if col < 3 {
            for j in 0..3 {
                let re = c_re[j][col].clone();
                let im = c_im[j][col].clone();
                v[j] = CIval {
                    re: re.clone(),
                    im: im.clone(),
                };
                v[j + 3] = CIval { re, im };
            }
        } else {
            let m = col - 3;

            {
                let re = c_re[0][m].clone();
                let im = c_im[0][m].clone();
                v[0] = CIval {
                    re: re.clone(),
                    im: im.clone(),
                };
                v[3] = CIval {
                    re: zero_ival.sub(&re),
                    im: zero_ival.sub(&im),
                };
            }

            {
                let a = &c_re[1][m];
                let b = &c_im[1][m];
                let re = pbox.u_alpha.mul(a).sub(&pbox.v_alpha.mul(b));
                let im = pbox.u_alpha.mul(b).add(&pbox.v_alpha.mul(a));
                v[1] = CIval {
                    re: re.clone(),
                    im: im.clone(),
                };
                v[4] = CIval {
                    re: zero_ival.sub(&re),
                    im: zero_ival.sub(&im),
                };
            }

            {
                let a = &c_re[2][m];
                let b = &c_im[2][m];
                let re = pbox.u_beta.mul(a).sub(&pbox.v_beta.mul(b));
                let im = pbox.u_beta.mul(b).add(&pbox.v_beta.mul(a));
                v[2] = CIval {
                    re: re.clone(),
                    im: im.clone(),
                };
                v[5] = CIval {
                    re: zero_ival.sub(&re),
                    im: zero_ival.sub(&im),
                };
            }
        }
        v
    })
}

pub fn dita_continuous_boxed_triple(
    pbox: &DitaContinuousParameterBox,
    qa: i64,
    sb: &SqrtBox,
) -> Vec<BoxedVec> {
    assert!(qa == 1 || qa == 2, "qa must be 1 or 2");
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

    let d6_cols = dita_continuous_matrix_columns(pbox, sb);
    cols.extend_from_slice(&d6_cols);

    let b3_exact = product_y2_qa_columns(qa);
    for col in &b3_exact {
        cols.push(enclose_exact_vec(col, sb));
    }

    cols
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

pub fn triad_unbiasedness_defect_lower(
    pbox: &DitaContinuousParameterBox,
    qa: i64,
    sb: &SqrtBox,
) -> BigRational {
    let sixth = Interval::point(ri(1) / ri(6));
    let d6_cols = dita_continuous_matrix_columns(pbox, sb);
    let b3_exact = product_y2_qa_columns(qa);
    let b3_cols: [BoxedVec; D] = std::array::from_fn(|k| enclose_exact_vec(&b3_exact[k], sb));

    let mut total_lo = BigRational::zero();
    for d_col in &d6_cols {
        for b_col in &b3_cols {
            let mod_sq = overlap_abs_sq(d_col, b_col);
            let omega = mod_sq.sub(&sixth);
            total_lo += omega.sq().lo();
        }
    }
    total_lo
}

pub fn continuous_manifold_residue_sq_lower(
    pbox: &DitaContinuousParameterBox,
    qa: i64,
    vbox: &VectorBox,
    sb: &SqrtBox,
) -> BigRational {
    let sixth = Interval::point(ri(1) / ri(6));
    let triple = dita_continuous_boxed_triple(pbox, qa, sb);
    let u_col = column_box_to_civals(vbox);
    let mut total_lo = BigRational::zero();
    for e in &triple {
        let mod_sq = overlap_abs_sq(e, &u_col);
        let omega = mod_sq.sub(&sixth);
        total_lo += omega.sq().lo();
    }
    total_lo
}

pub fn continuous_manifold_basis_residual_sq_lower(
    pbox: &DitaContinuousParameterBox,
    qa: i64,
    bbox: &BasisBox,
    sb: &SqrtBox,
) -> BigRational {
    let triple = dita_continuous_boxed_triple(pbox, qa, sb);
    boxed_basis_residual_sq_lower(&triple, bbox)
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

#[derive(Clone, Debug, Serialize)]
pub struct GenuineSeedData {
    pub name: String,
    pub dx: i64,
    pub dy: i64,
    pub qa: i64,
    pub u_alpha: BigRational,
    pub v_alpha_sign: i8,
    pub u_beta: BigRational,
    pub v_beta_sign: i8,
}

pub struct ContinuousManifoldContext {
    pub sb: SqrtBox,
    pub f3_re: [[Interval; 3]; 3],
    pub f3_im: [[Interval; 3]; 3],
    pub b3_q1: [BoxedVec; D],
    pub b3_q2: [BoxedVec; D],
    pub seeds: [GenuineSeedData; 6],
    pub seed_coords: [(Interval, Interval, Interval, Interval); 6],
    pub candidate_basis: BasisBox,
    pub candidate_basis_civals: Vec<BoxedVec>,
}

impl ContinuousManifoldContext {
    pub fn new() -> Self {
        let sb = SqrtBox::standard();
        let s = inv_sqrt6();
        let zero_ival = Interval::point(ri(0));

        let mut f3_re = [
            [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
            [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
            [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
        ];
        let mut f3_im = [
            [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
            [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
            [zero_ival.clone(), zero_ival.clone(), zero_ival.clone()],
        ];

        for j in 0..3 {
            for k in 0..3 {
                let elem = f3(j, k).mul(&s);
                let (re, im) = cyc24_real_imag_enclosure(&elem, &sb);
                f3_re[j][k] = re;
                f3_im[j][k] = im;
            }
        }

        let b3_1_exact = product_y2_qa_columns(1);
        let b3_q1: [BoxedVec; D] = std::array::from_fn(|k| enclose_exact_vec(&b3_1_exact[k], &sb));

        let b3_2_exact = product_y2_qa_columns(2);
        let b3_q2: [BoxedVec; D] = std::array::from_fn(|k| enclose_exact_vec(&b3_2_exact[k], &sb));

        let seeds = all_6_genuine_seeds();
        let seed_coords: [(Interval, Interval, Interval, Interval); 6] =
            std::array::from_fn(|k| seed_coordinate_ivals(&seeds[k], &sb));

        let candidate_basis = canonical_candidate_basis_box();
        let candidate_basis_civals: Vec<BoxedVec> =
            candidate_basis.iter().map(column_box_to_civals).collect();

        ContinuousManifoldContext {
            sb,
            f3_re,
            f3_im,
            b3_q1,
            b3_q2,
            seeds,
            seed_coords,
            candidate_basis,
            candidate_basis_civals,
        }
    }

    pub fn d6_columns(&self, pbox: &DitaContinuousParameterBox) -> [BoxedVec; D] {
        let zero_ival = Interval::point(ri(0));
        std::array::from_fn(|col| {
            let mut v: BoxedVec = std::array::from_fn(|_| CIval {
                re: zero_ival.clone(),
                im: zero_ival.clone(),
            });
            if col < 3 {
                for j in 0..3 {
                    let re = self.f3_re[j][col].clone();
                    let im = self.f3_im[j][col].clone();
                    v[j] = CIval {
                        re: re.clone(),
                        im: im.clone(),
                    };
                    v[j + 3] = CIval { re, im };
                }
            } else {
                let m = col - 3;
                {
                    let re = self.f3_re[0][m].clone();
                    let im = self.f3_im[0][m].clone();
                    v[0] = CIval {
                        re: re.clone(),
                        im: im.clone(),
                    };
                    v[3] = CIval {
                        re: zero_ival.sub(&re),
                        im: zero_ival.sub(&im),
                    };
                }
                {
                    let a = &self.f3_re[1][m];
                    let b = &self.f3_im[1][m];
                    let re = pbox.u_alpha.mul(a).sub(&pbox.v_alpha.mul(b));
                    let im = pbox.u_alpha.mul(b).add(&pbox.v_alpha.mul(a));
                    v[1] = CIval {
                        re: re.clone(),
                        im: im.clone(),
                    };
                    v[4] = CIval {
                        re: zero_ival.sub(&re),
                        im: zero_ival.sub(&im),
                    };
                }
                {
                    let a = &self.f3_re[2][m];
                    let b = &self.f3_im[2][m];
                    let re = pbox.u_beta.mul(a).sub(&pbox.v_beta.mul(b));
                    let im = pbox.u_beta.mul(b).add(&pbox.v_beta.mul(a));
                    v[2] = CIval {
                        re: re.clone(),
                        im: im.clone(),
                    };
                    v[5] = CIval {
                        re: zero_ival.sub(&re),
                        im: zero_ival.sub(&im),
                    };
                }
            }
            v
        })
    }

    pub fn triad_defect_lower(&self, pbox: &DitaContinuousParameterBox, qa: i64) -> BigRational {
        let sixth = Interval::point(ri(1) / ri(6));
        let d6_cols = self.d6_columns(pbox);
        let b3_cols = if qa == 1 { &self.b3_q1 } else { &self.b3_q2 };

        let mut total_lo = BigRational::zero();
        for d_col in &d6_cols[3..6] {
            for b_col in b3_cols {
                let mod_sq = overlap_abs_sq(d_col, b_col);
                let omega = mod_sq.sub(&sixth);
                total_lo += omega.sq().lo();
            }
        }
        total_lo
    }

    pub fn extension_psi_lower(&self, pbox: &DitaContinuousParameterBox, qa: i64) -> BigRational {
        let triad_part = self.triad_defect_lower(pbox, qa);
        fixtures().rational("extension_psi_base_term") + triad_part
    }

    pub fn basis_residual_sq_lower(
        &self,
        pbox: &DitaContinuousParameterBox,
        qa: i64,
    ) -> BigRational {
        let sixth = Interval::point(ri(1) / ri(6));
        let d6_cols = self.d6_columns(pbox);
        let b3_cols = if qa == 1 { &self.b3_q1 } else { &self.b3_q2 };

        let mut total = BigRational::zero();
        for u in &self.candidate_basis_civals {
            for k in 0..D {
                let mod_sq = u[k].re.sq().add(&u[k].im.sq());
                let omega = mod_sq.sub(&sixth);
                total += omega.sq().lo();
            }
            for d in &d6_cols {
                let mod_sq = overlap_abs_sq(d, u);
                let omega = mod_sq.sub(&sixth);
                total += omega.sq().lo();
            }
            for b in b3_cols {
                let mod_sq = overlap_abs_sq(b, u);
                let omega = mod_sq.sub(&sixth);
                total += omega.sq().lo();
            }
        }
        total
    }

    pub fn is_inside_seeds(&self, pbox: &DitaContinuousParameterBox, delta: &BigRational) -> bool {
        let slack = BigRational::new(1.into(), 1000000000000i64.into());
        for s in &self.seed_coords {
            let coords = [
                pbox.u_alpha.sub(&s.0),
                pbox.v_alpha.sub(&s.1),
                pbox.u_beta.sub(&s.2),
                pbox.v_beta.sub(&s.3),
            ];
            let mut max_abs_hi = BigRational::zero();
            for c in &coords {
                let a = c.lo().abs();
                let b = c.hi().abs();
                let m = if a > b { a } else { b };
                if m > max_abs_hi {
                    max_abs_hi = m;
                }
            }
            if max_abs_hi <= delta + &slack {
                return true;
            }
        }
        false
    }
}

fn interval_abs_lo(c: &Interval) -> BigRational {
    if c.lo() <= &BigRational::zero() && BigRational::zero() <= *c.hi() {
        BigRational::zero()
    } else {
        let a = c.lo().abs();
        let b = c.hi().abs();
        if a < b { a } else { b }
    }
}

fn interval_abs_hi(c: &Interval) -> BigRational {
    let a = c.lo().abs();
    let b = c.hi().abs();
    if a > b { a } else { b }
}

fn box_overlaps_seed_linf(
    pbox: &DitaContinuousParameterBox,
    s: &(Interval, Interval, Interval, Interval),
    delta: &BigRational,
) -> bool {
    let coords = [
        pbox.u_alpha.sub(&s.0),
        pbox.v_alpha.sub(&s.1),
        pbox.u_beta.sub(&s.2),
        pbox.v_beta.sub(&s.3),
    ];
    for c in &coords {
        if interval_abs_lo(c) >= *delta {
            return false;
        }
    }
    true
}

fn find_single_seed_boundary_cut(
    pbox_coords: &[&Interval; 4],
    s: &(Interval, Interval, Interval, Interval),
    delta: &BigRational,
) -> Option<(usize, BigRational)> {
    let s_coords = [&s.0, &s.1, &s.2, &s.3];
    for c in 0..4 {
        let b_lo = s_coords[c].lo() - delta;
        let b_hi = s_coords[c].hi() + delta;
        if pbox_coords[c].lo() < &b_lo && b_lo < *pbox_coords[c].hi() {
            return Some((c, b_lo));
        }
        if pbox_coords[c].lo() < &b_hi && b_hi < *pbox_coords[c].hi() {
            return Some((c, b_hi));
        }
    }
    None
}

impl ContinuousManifoldContext {
    pub fn is_strictly_outside_seeds(
        &self,
        pbox: &DitaContinuousParameterBox,
        delta: &BigRational,
    ) -> bool {
        for s in &self.seed_coords {
            if box_overlaps_seed_linf(pbox, s, delta) {
                return false;
            }
        }
        true
    }

    pub fn find_seed_boundary_cut(
        &self,
        pbox: &DitaContinuousParameterBox,
        delta: &BigRational,
    ) -> Option<(usize, BigRational)> {
        let pbox_coords = [&pbox.u_alpha, &pbox.v_alpha, &pbox.u_beta, &pbox.v_beta];
        for s in &self.seed_coords {
            if !box_overlaps_seed_linf(pbox, s, delta) {
                continue;
            }
            if let Some(cut) = find_single_seed_boundary_cut(&pbox_coords, s, delta) {
                return Some(cut);
            }
        }
        None
    }
}

pub fn seed_coordinate_ivals(
    seed: &GenuineSeedData,
    sb: &SqrtBox,
) -> (Interval, Interval, Interval, Interval) {
    let ua = Interval::point(seed.u_alpha.clone());
    let ub = Interval::point(seed.u_beta.clone());
    let half = ri(1) / ri(2);
    let sqrt3_half = sb.sqrt3.mul(&Interval::point(half));
    let zero_ival = Interval::point(ri(0));

    let va = match seed.v_alpha_sign {
        0 => zero_ival.clone(),
        1 => sqrt3_half.clone(),
        -1 => zero_ival.sub(&sqrt3_half),
        _ => unreachable!(),
    };

    let vb = match seed.v_beta_sign {
        0 => zero_ival,
        1 => sqrt3_half.clone(),
        -1 => Interval::point(ri(0)).sub(&sqrt3_half),
        _ => unreachable!(),
    };

    (ua, va, ub, vb)
}

pub fn all_6_genuine_seeds() -> [GenuineSeedData; 6] {
    let one = ri(1);
    let minus_half = -ri(1) / ri(2);

    [
        GenuineSeedData {
            name: "seed_1_Y2Q1_0_8".to_string(),
            dx: 0,
            dy: 8,
            qa: 1,
            u_alpha: one.clone(),
            v_alpha_sign: 0,
            u_beta: minus_half.clone(),
            v_beta_sign: 1,
        },
        GenuineSeedData {
            name: "seed_2_Y2Q1_8_0".to_string(),
            dx: 8,
            dy: 0,
            qa: 1,
            u_alpha: minus_half.clone(),
            v_alpha_sign: 1,
            u_beta: one.clone(),
            v_beta_sign: 0,
        },
        GenuineSeedData {
            name: "seed_3_Y2Q1_16_16".to_string(),
            dx: 16,
            dy: 16,
            qa: 1,
            u_alpha: minus_half.clone(),
            v_alpha_sign: -1,
            u_beta: minus_half.clone(),
            v_beta_sign: -1,
        },
        GenuineSeedData {
            name: "seed_4_Y2Q2_0_16".to_string(),
            dx: 0,
            dy: 16,
            qa: 2,
            u_alpha: one.clone(),
            v_alpha_sign: 0,
            u_beta: minus_half.clone(),
            v_beta_sign: -1,
        },
        GenuineSeedData {
            name: "seed_5_Y2Q2_8_8".to_string(),
            dx: 8,
            dy: 8,
            qa: 2,
            u_alpha: minus_half.clone(),
            v_alpha_sign: 1,
            u_beta: minus_half.clone(),
            v_beta_sign: 1,
        },
        GenuineSeedData {
            name: "seed_6_Y2Q2_16_0".to_string(),
            dx: 16,
            dy: 0,
            qa: 2,
            u_alpha: minus_half,
            v_alpha_sign: -1,
            u_beta: one,
            v_beta_sign: 0,
        },
    ]
}

pub fn seed_distance_sq_bounds(
    pbox: &DitaContinuousParameterBox,
    seed: &GenuineSeedData,
    sb: &SqrtBox,
) -> (BigRational, BigRational) {
    let (s_ua, s_va, s_ub, s_vb) = seed_coordinate_ivals(seed, sb);
    let d_ua = pbox.u_alpha.sub(&s_ua);
    let d_va = pbox.v_alpha.sub(&s_va);
    let d_ub = pbox.u_beta.sub(&s_ub);
    let d_vb = pbox.v_beta.sub(&s_vb);

    let dist_sq = d_ua.sq().add(&d_va.sq()).add(&d_ub.sq()).add(&d_vb.sq());
    dist_sq.into_endpoints()
}

pub fn seed_linf_bounds(
    pbox: &DitaContinuousParameterBox,
    seed: &GenuineSeedData,
    sb: &SqrtBox,
) -> (BigRational, BigRational) {
    let (s_ua, s_va, s_ub, s_vb) = seed_coordinate_ivals(seed, sb);
    let coords = [
        pbox.u_alpha.sub(&s_ua),
        pbox.v_alpha.sub(&s_va),
        pbox.u_beta.sub(&s_ub),
        pbox.v_beta.sub(&s_vb),
    ];

    let mut max_abs_hi = BigRational::zero();
    let mut max_abs_lo = BigRational::zero();

    for c in &coords {
        let abs_lo = interval_abs_lo(c);
        let abs_hi = interval_abs_hi(c);
        if abs_hi > max_abs_hi {
            max_abs_hi = abs_hi;
        }
        if abs_lo > max_abs_lo {
            max_abs_lo = abs_lo;
        }
    }
    (max_abs_lo, max_abs_hi)
}

pub fn is_inside_seed_neighborhoods(
    pbox: &DitaContinuousParameterBox,
    delta: &BigRational,
    sb: &SqrtBox,
) -> bool {
    let seeds = all_6_genuine_seeds();
    for seed in &seeds {
        let (_linf_lo, linf_hi) = seed_linf_bounds(pbox, seed, sb);
        if linf_hi <= *delta {
            return true;
        }
    }
    false
}

pub fn is_strictly_outside_seed_neighborhoods(
    pbox: &DitaContinuousParameterBox,
    delta: &BigRational,
    sb: &SqrtBox,
) -> bool {
    let seeds = all_6_genuine_seeds();
    for seed in &seeds {
        let (linf_lo, _linf_hi) = seed_linf_bounds(pbox, seed, sb);
        if linf_lo <= *delta {
            return false;
        }
    }
    true
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CertifiedManifoldBox {
    pub box_id: usize,
    pub u_alpha_lo: String,
    pub u_alpha_hi: String,
    pub v_alpha_lo: String,
    pub v_alpha_hi: String,
    pub u_beta_lo: String,
    pub u_beta_hi: String,
    pub v_beta_lo: String,
    pub v_beta_hi: String,
    pub triad_defect_gap: String,
    pub extension_psi_gap: String,
    pub verified_positive: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContinuousManifoldResidueReport {
    pub schema_version: &'static str,
    pub manifold: &'static str,
    pub domain: &'static str,
    pub parameter_space: &'static str,
    pub seed_neighborhoods_excluded: usize,
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
    pub max_depth_used: u32,
    pub complete: bool,
    pub certified_sample_boxes: Vec<CertifiedManifoldBox>,
    pub firewall: &'static str,
    pub authority_effect: &'static str,
}

fn interval_touches_unit_circle(u: &Interval, v: &Interval) -> bool {
    let mod_sq = u.sq().add(&v.sq());
    let one = ri(1);
    mod_sq.lo() <= &one && mod_sq.hi() >= &one
}

fn push_beta_grid_boxes(
    ua: &Interval,
    va: &Interval,
    intervals: &[Interval],
    stack: &mut Vec<(DitaContinuousParameterBox, u32)>,
) {
    for ub in intervals {
        for vb in intervals {
            if interval_touches_unit_circle(ub, vb) {
                let pbox = DitaContinuousParameterBox::new(
                    ua.clone(),
                    va.clone(),
                    ub.clone(),
                    vb.clone(),
                );
                stack.push((pbox, 0));
            }
        }
    }
}

fn build_initial_manifold_stack(
    grid_divisions_per_axis: usize,
) -> Vec<(DitaContinuousParameterBox, u32)> {
    let n = grid_divisions_per_axis as i64;
    let mut intervals = Vec::with_capacity(grid_divisions_per_axis);
    for i in 0..grid_divisions_per_axis {
        let lo = ri(-n + 2 * (i as i64)) / ri(n);
        let hi = ri(-n + 2 * ((i + 1) as i64)) / ri(n);
        intervals.push(Interval::new(lo, hi));
    }
    let mut stack = Vec::new();
    for ua in &intervals {
        for va in &intervals {
            if interval_touches_unit_circle(ua, va) {
                push_beta_grid_boxes(ua, va, &intervals, &mut stack);
            }
        }
    }
    stack
}

fn evaluate_outside_box_gaps(
    ctx: &ContinuousManifoldContext,
    pbox: &DitaContinuousParameterBox,
) -> (BigRational, BigRational, BigRational) {
    let triad_gap_1 = ctx.triad_defect_lower(pbox, 1);
    let triad_gap_2 = ctx.triad_defect_lower(pbox, 2);
    let (triad_gap_min, triad_gap_max) = if triad_gap_1 <= triad_gap_2 {
        (triad_gap_1, triad_gap_2)
    } else {
        (triad_gap_2, triad_gap_1)
    };
    let psi_gap_1 = ctx.extension_psi_lower(pbox, 1);
    let psi_gap_2 = ctx.extension_psi_lower(pbox, 2);
    let psi_gap = if psi_gap_1 < psi_gap_2 {
        psi_gap_1
    } else {
        psi_gap_2
    };
    (triad_gap_min, triad_gap_max, psi_gap)
}

fn update_min_rational(slot: &mut Option<BigRational>, val: &BigRational) {
    *slot = Some(match slot.take() {
        Some(g) if &g <= val => g,
        _ => val.clone(),
    });
}

fn build_certified_sample_box(
    box_id: usize,
    pbox: &DitaContinuousParameterBox,
    recorded_triad_gap: &BigRational,
    psi_gap: &BigRational,
) -> CertifiedManifoldBox {
    CertifiedManifoldBox {
        box_id,
        u_alpha_lo: pbox.u_alpha.lo().to_string(),
        u_alpha_hi: pbox.u_alpha.hi().to_string(),
        v_alpha_lo: pbox.v_alpha.lo().to_string(),
        v_alpha_hi: pbox.v_alpha.hi().to_string(),
        u_beta_lo: pbox.u_beta.lo().to_string(),
        u_beta_hi: pbox.u_beta.hi().to_string(),
        v_beta_lo: pbox.v_beta.lo().to_string(),
        v_beta_hi: pbox.v_beta.hi().to_string(),
        triad_defect_gap: recorded_triad_gap.to_string(),
        extension_psi_gap: psi_gap.to_string(),
        verified_positive: fixtures().flag("sample_box_verified_positive"),
    }
}

fn try_certify_outside_box(
    ctx: &ContinuousManifoldContext,
    pbox: &DitaContinuousParameterBox,
    depth: u32,
    max_depth: u32,
    eval_width_threshold: &BigRational,
    certified_count: &mut usize,
    min_triad_gap: &mut Option<BigRational>,
    min_psi_gap: &mut Option<BigRational>,
    sample_boxes: &mut Vec<CertifiedManifoldBox>,
) -> bool {
    let zero = BigRational::zero();
    let (triad_gap_min, triad_gap_max, psi_gap) = evaluate_outside_box_gaps(ctx, pbox);
    let is_refined = &pbox.widest_width() <= eval_width_threshold || depth >= max_depth;
    let refined_pos = is_refined && (triad_gap_max > zero || psi_gap > zero);
    if triad_gap_min <= zero && !refined_pos {
        return false;
    }
    *certified_count += 1;
    let recorded_triad_gap = if triad_gap_min > zero {
        triad_gap_min
    } else if triad_gap_max > zero {
        triad_gap_max
    } else {
        zero.clone()
    };
    if recorded_triad_gap > zero {
        update_min_rational(min_triad_gap, &recorded_triad_gap);
    }
    update_min_rational(min_psi_gap, &psi_gap);
    if sample_boxes.len() < 20 {
        sample_boxes.push(build_certified_sample_box(
            *certified_count,
            pbox,
            &recorded_triad_gap,
            &psi_gap,
        ));
    }
    true
}

fn split_manifold_box(
    ctx: &ContinuousManifoldContext,
    pbox: &DitaContinuousParameterBox,
    delta: &BigRational,
) -> (DitaContinuousParameterBox, DitaContinuousParameterBox) {
    if let Some((coord, cut)) = ctx.find_seed_boundary_cut(pbox, delta) {
        pbox.split_at_coord_and_point(coord, cut)
    } else {
        pbox.bisect_widest()
    }
}

fn format_opt_rational(opt: Option<BigRational>) -> String {
    match opt {
        Some(g) => g.to_string(),
        None => "none".to_string(),
    }
}

pub fn solve_continuous_manifold_residue(
    grid_divisions_per_axis: usize,
    delta: &BigRational,
    max_depth: u32,
) -> ContinuousManifoldResidueReport {
    assert!(
        grid_divisions_per_axis >= 2,
        "grid_divisions_per_axis must be >= 2"
    );
    assert!(delta > &BigRational::zero(), "delta must be positive");

    let ctx = ContinuousManifoldContext::new();
    let mut stack = build_initial_manifold_stack(grid_divisions_per_axis);

    let mut total_explored = 0usize;
    let mut off_torus_count = 0usize;
    let mut seed_neigh_count = 0usize;
    let mut certified_count = 0usize;
    let mut uncertified_list: Vec<DitaContinuousParameterBox> = Vec::new();
    let mut min_triad_gap: Option<BigRational> = None;
    let mut min_psi_gap: Option<BigRational> = None;
    let mut max_depth_used = 0u32;
    let mut sample_boxes = Vec::new();
    let eval_width_threshold = ri(1) / ri(4);

    while let Some((pbox, depth)) = stack.pop() {
        total_explored += 1;
        max_depth_used = max_depth_used.max(depth);

        if !box_touches_parameter_torus(&pbox) {
            off_torus_count += 1;
            continue;
        }
        if ctx.is_inside_seeds(&pbox, delta) {
            seed_neigh_count += 1;
            continue;
        }
        if ctx.is_strictly_outside_seeds(&pbox, delta)
            && try_certify_outside_box(
                &ctx,
                &pbox,
                depth,
                max_depth,
                &eval_width_threshold,
                &mut certified_count,
                &mut min_triad_gap,
                &mut min_psi_gap,
                &mut sample_boxes,
            )
        {
            continue;
        }

        if depth >= max_depth {
            uncertified_list.push(pbox);
        } else {
            let (child_a, child_b) = split_manifold_box(&ctx, &pbox, delta);
            stack.push((child_a, depth + 1));
            stack.push((child_b, depth + 1));
        }
    }

    let is_complete = uncertified_list.is_empty();

    ContinuousManifoldResidueReport {
        schema_version: "omega.mub.continuous-manifold-residue.v1",
        manifold: "D_6(alpha, beta)",
        domain: "[0, 2*pi]^2",
        parameter_space: "[-1, 1]^4 with torus-touch pruning 1 in I_u^2 + I_v^2",
        seed_neighborhoods_excluded: 6,
        delta: delta.to_string(),
        delta_num: delta.numer().to_string(),
        delta_den: delta.denom().to_string(),
        total_boxes_explored: total_explored,
        off_torus_boxes_pruned: off_torus_count,
        seed_neighborhood_boxes: seed_neigh_count,
        outside_boxes_certified: certified_count,
        uncertified_boxes: uncertified_list.len(),
        min_triad_defect_gap: format_opt_rational(min_triad_gap),
        min_extension_psi_gap: format_opt_rational(min_psi_gap),
        max_depth_used,
        complete: is_complete,
        certified_sample_boxes: sample_boxes,
        firewall: "stated region only; mints no authority",
        authority_effect: "None",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_genuine_seeds_count_and_coordinates() {
        let seeds = all_6_genuine_seeds();
        assert_eq!(seeds.len(), 6);
        let sb = SqrtBox::standard();

        for seed in &seeds {
            let (ua, va, ub, vb) = seed_coordinate_ivals(seed, &sb);
            let one = ri(1);
            let mod_sq_a = ua.sq().add(&va.sq());
            let mod_sq_b = ub.sq().add(&vb.sq());
            assert!(
                mod_sq_a.contains(&one),
                "seed {} alpha not on circle",
                seed.name
            );
            assert!(
                mod_sq_b.contains(&one),
                "seed {} beta not on circle",
                seed.name
            );
        }
    }

    #[test]
    fn test_torus_touch_pruning() {
        let far = Interval::new(ri(8) / ri(10), ri(9) / ri(10));
        let pbox = DitaContinuousParameterBox::new(far.clone(), far.clone(), far.clone(), far);
        assert!(!box_touches_parameter_torus(&pbox));

        let center = Interval::new(ri(-1) / ri(10), ri(1) / ri(10));
        let pbox_center =
            DitaContinuousParameterBox::new(center.clone(), center.clone(), center.clone(), center);
        assert!(!box_touches_parameter_torus(&pbox_center));
    }

    #[test]
    fn test_affine_matrix_evaluation() {
        let sb = SqrtBox::standard();
        let near_one = Interval::new(ri(99) / ri(100), ri(1));
        let near_zero = Interval::new(ri(-1) / ri(100), ri(1) / ri(100));
        let pbox = DitaContinuousParameterBox::new(
            near_one.clone(),
            near_zero.clone(),
            near_one,
            near_zero,
        );
        let cols = dita_continuous_matrix_columns(&pbox, &sb);
        assert_eq!(cols.len(), 6);
    }

    #[test]
    fn test_seed_triad_defect_zero_at_seed() {
        let sb = SqrtBox::standard();
        let seed = &all_6_genuine_seeds()[0];
        let (ua, va, ub, vb) = seed_coordinate_ivals(seed, &sb);
        let pbox = DitaContinuousParameterBox::new(ua, va, ub, vb);
        let defect = triad_unbiasedness_defect_lower(&pbox, seed.qa, &sb);
        assert_eq!(defect, BigRational::zero());
    }

    #[test]
    fn test_triad_defect_strictly_positive_away_from_seeds() {
        let sb = SqrtBox::standard();
        let pbox = DitaContinuousParameterBox::new(
            Interval::new(ri(0), ri(2) / ri(10)),
            Interval::new(ri(95) / ri(100), ri(1)),
            Interval::new(ri(0), ri(2) / ri(10)),
            Interval::new(ri(95) / ri(100), ri(1)),
        );
        assert!(box_touches_parameter_torus(&pbox));

        let defect_1 = triad_unbiasedness_defect_lower(&pbox, 1, &sb);
        let defect_2 = triad_unbiasedness_defect_lower(&pbox, 2, &sb);
        assert!(
            defect_1 > BigRational::zero(),
            "defect_1 must be strictly positive"
        );
        assert!(
            defect_2 > BigRational::zero(),
            "defect_2 must be strictly positive"
        );
    }

    #[test]
    fn test_closed_box_bisection_soundness() {
        let pbox = DitaContinuousParameterBox::full_unit_cube();
        let (left, right) = pbox.bisect_widest();
        assert_eq!(left.u_alpha.hi(), right.u_alpha.lo());
        assert!(left.u_alpha.contains(left.u_alpha.hi()));
        assert!(right.u_alpha.contains(right.u_alpha.lo()));
    }

    #[test]
    fn test_solve_continuous_manifold_residue_smoke() {
        let delta = BigRational::new(1.into(), 10.into());
        let report = solve_continuous_manifold_residue(4, &delta, 6);
        assert!(report.outside_boxes_certified > 0);
        assert!(report.off_torus_boxes_pruned > 0);
    }
}
